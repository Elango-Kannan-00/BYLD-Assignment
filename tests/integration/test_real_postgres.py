from __future__ import annotations

import os
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from app.core.constants import RiskProfile, TransactionType
from app.models import Holding, Portfolio, Transaction
from app.models.base import Base
from app.schemas.dividend import DividendCreateRequest
from app.schemas.transaction import TransactionCreateRequest
from app.services.dividend_service import DividendService
from app.services.transaction_service import TransactionService

DATABASE_URL = os.getenv("INTEGRATION_DATABASE_URL")
if not DATABASE_URL:
    pytest.skip("INTEGRATION_DATABASE_URL is not set; integration tests require a real PostgreSQL database", allow_module_level=True)


pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def engine():
    db_engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    Base.metadata.drop_all(db_engine)
    with db_engine.begin() as connection:
        connection.exec_driver_sql("DROP TYPE IF EXISTS risk_profile CASCADE")
        connection.exec_driver_sql("DROP TYPE IF EXISTS transaction_type CASCADE")
    Base.metadata.create_all(db_engine)
    yield db_engine
    Base.metadata.drop_all(db_engine)
    with db_engine.begin() as connection:
        connection.exec_driver_sql("DROP TYPE IF EXISTS risk_profile CASCADE")
        connection.exec_driver_sql("DROP TYPE IF EXISTS transaction_type CASCADE")
    db_engine.dispose()


@pytest.fixture()
def session(engine) -> Session:
    session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    db_session = session_local()
    try:
        yield db_session
    finally:
        db_session.close()


def _seed_portfolio(session: Session) -> Portfolio:
    portfolio = Portfolio(
        id=uuid4(),
        client_name="Aarav Mehta",
        risk_profile=RiskProfile.balanced,
        cash_balance=Decimal("0.0000"),
    )
    session.add(portfolio)
    session.commit()
    return portfolio


def test_buy_updates_weighted_average_against_real_postgres(session: Session) -> None:
    portfolio = _seed_portfolio(session)
    service = TransactionService(session)

    first_buy = TransactionCreateRequest.model_validate({"symbol": "aapl", "quantity": 10, "price": "100.0000"})
    second_buy = TransactionCreateRequest.model_validate({"symbol": "AAPL", "quantity": 5, "price": "120.0000"})

    service.buy(portfolio.id, first_buy)
    result = service.buy(portfolio.id, second_buy)

    holding = session.scalars(
        select(Holding).where(Holding.portfolio_id == portfolio.id, Holding.symbol == "AAPL")
    ).one()

    assert holding.quantity == 15
    assert holding.weighted_average_cost == Decimal("106.6667")
    assert result.total_amount == Decimal("600.0000")


def test_dividend_uses_holdings_as_of_record_date(session: Session) -> None:
    portfolio = _seed_portfolio(session)

    session.add_all(
        [
            Transaction(
                id=uuid4(),
                portfolio_id=portfolio.id,
                symbol="AAPL",
                transaction_type=TransactionType.buy,
                quantity=10,
                price=Decimal("100.0000"),
                total_amount=Decimal("1000.0000"),
                transacted_at=datetime(2026, 4, 24, 10, tzinfo=timezone.utc),
            ),
            Transaction(
                id=uuid4(),
                portfolio_id=portfolio.id,
                symbol="AAPL",
                transaction_type=TransactionType.sell,
                quantity=4,
                price=Decimal("100.0000"),
                total_amount=Decimal("400.0000"),
                transacted_at=datetime(2026, 4, 26, 10, tzinfo=timezone.utc),
            ),
        ]
    )
    session.commit()

    service = DividendService(session)
    payload = DividendCreateRequest.model_validate(
        {"symbol": "aapl", "perShareAmount": "1.5000", "recordDate": "2026-04-25"}
    )

    result = service.record_dividend(portfolio.id, payload)
    session.refresh(portfolio)

    assert result.quantity_held == 10
    assert result.payout == Decimal("15.0000")
    assert portfolio.cash_balance == Decimal("15.0000")
