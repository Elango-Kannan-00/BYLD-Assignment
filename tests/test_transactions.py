from decimal import Decimal
from uuid import uuid4

import pytest

from app.core.constants import RiskProfile
from app.exceptions.transaction import InsufficientHoldingError
from app.models.holding import Holding
from app.services.transaction_service import TransactionService
from app.schemas.transaction import TransactionCreateRequest


class FakeSession:
    def __init__(self) -> None:
        self.added = []
        self.deleted = []
        self.committed = False
        self.refreshed = None
        self.flushed = False

    def add(self, obj):
        self.added.append(obj)

    def delete(self, obj):
        self.deleted.append(obj)

    def commit(self):
        self.committed = True

    def refresh(self, obj):
        self.refreshed = obj

    def flush(self):
        self.flushed = True


def test_buy_updates_weighted_average_correctly():
    portfolio_id = uuid4()
    holding = Holding(
        portfolio_id=portfolio_id,
        symbol="AAPL",
        quantity=10,
        weighted_average_cost=Decimal("100"),
    )

    class FakePortfolio:
        id = portfolio_id
        client_name = "Aarav Mehta"
        risk_profile = RiskProfile.balanced
        cash_balance = Decimal("0.0000")

    class FakePortfolioRepository:
        def __init__(self, session):
            self.session = session

        def get_by_id(self, _portfolio_id):
            return FakePortfolio()

    class FakeHoldingRepository:
        def __init__(self, session):
            self.session = session

        def get_by_portfolio_and_symbol(self, _portfolio_id, _symbol):
            return holding

    session = FakeSession()
    service = TransactionService(session)
    service.portfolio_repository = FakePortfolioRepository(session)
    service.holding_repository = FakeHoldingRepository(session)

    payload = TransactionCreateRequest.model_validate(
        {"symbol": "aapl", "quantity": 5, "price": "120"}
    )

    result = service.buy(portfolio_id, payload)

    assert holding.quantity == 15
    assert holding.weighted_average_cost == Decimal("106.6667")
    assert session.committed is True
    assert result.symbol == "AAPL"
    assert result.transaction_type == "buy"
    assert result.quantity == 5
    assert result.price == Decimal("120")
    assert result.message == "Purchased the stock"


def test_sell_reduces_holding_and_returns_message():
    portfolio_id = uuid4()
    holding = Holding(
        portfolio_id=portfolio_id,
        symbol="AAPL",
        quantity=8,
        weighted_average_cost=Decimal("100"),
    )

    class FakePortfolio:
        id = portfolio_id

    class FakePortfolioRepository:
        def __init__(self, session):
            self.session = session

        def get_by_id(self, _portfolio_id):
            return FakePortfolio()

    class FakeHoldingRepository:
        def __init__(self, session):
            self.session = session

        def get_by_portfolio_and_symbol(self, _portfolio_id, _symbol):
            return holding

    session = FakeSession()
    service = TransactionService(session)
    service.portfolio_repository = FakePortfolioRepository(session)
    service.holding_repository = FakeHoldingRepository(session)

    payload = TransactionCreateRequest.model_validate(
        {"symbol": "AAPL", "quantity": 3, "price": "120"}
    )

    result = service.sell(portfolio_id, payload)

    assert holding.quantity == 5
    assert session.committed is True
    assert result.transaction_type == "sell"
    assert result.message == "Sold the stock"


def test_sell_rejects_when_quantity_exceeds_holdings():
    portfolio_id = uuid4()
    holding = Holding(
        portfolio_id=portfolio_id,
        symbol="AAPL",
        quantity=5,
        weighted_average_cost=Decimal("100"),
    )

    class FakePortfolio:
        id = portfolio_id

    class FakePortfolioRepository:
        def __init__(self, session):
            self.session = session

        def get_by_id(self, _portfolio_id):
            return FakePortfolio()

    class FakeHoldingRepository:
        def __init__(self, session):
            self.session = session

        def get_by_portfolio_and_symbol(self, _portfolio_id, _symbol):
            return holding

    session = FakeSession()
    service = TransactionService(session)
    service.portfolio_repository = FakePortfolioRepository(session)
    service.holding_repository = FakeHoldingRepository(session)

    payload = TransactionCreateRequest.model_validate(
        {"symbol": "AAPL", "quantity": 6, "price": "120"}
    )

    with pytest.raises(InsufficientHoldingError) as exc_info:
        service.sell(portfolio_id, payload)

    assert exc_info.value.status_code == 409
    assert session.committed is False
