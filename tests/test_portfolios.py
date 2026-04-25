from decimal import Decimal
from uuid import uuid4

import pytest

from app.api.v1.routers import portfolios as portfolios_router
from app.core.constants import RiskProfile
from app.models.portfolio import Portfolio
from app.main import app
from app.repositories.portfolio_repository import PortfolioRepository
from app.schemas.portfolio import BalanceAddRequest, PortfolioCreateRequest, PortfolioResponse
from app.services.portfolio_service import PortfolioService


def test_create_portfolio_returns_201_and_location_header(client, monkeypatch):
    portfolio_id = uuid4()

    class FakeService:
        def __init__(self, session):
            self.session = session

        def create_portfolio(self, data):
            return PortfolioResponse(
                id=portfolio_id,
                clientName=data.client_name,
                riskProfile=data.risk_profile,
                cashBalance=Decimal("0.00"),
                message="Portfolio created",
            )

    monkeypatch.setattr(portfolios_router, "PortfolioService", FakeService)
    app.dependency_overrides.clear()

    response = client.post(
        "/v1/portfolios",
        json={"clientName": "Aarav Mehta", "riskProfile": "balanced"},
    )

    assert response.status_code == 201
    assert response.headers["location"] == f"/v1/portfolios/{portfolio_id}"
    assert response.json() == {
        "id": str(portfolio_id),
        "clientName": "Aarav Mehta",
        "riskProfile": "balanced",
        "cashBalance": "0.00",
        "message": "Portfolio created",
    }


@pytest.mark.parametrize(
    ("payload", "expected_field"),
    [
        ({}, "clientName"),
        ({"clientName": "", "riskProfile": "balanced"}, "clientName"),
        ({"clientName": "Aarav Mehta"}, "riskProfile"),
    ],
)
def test_create_portfolio_validation_errors(client, payload, expected_field):
    response = client.post("/v1/portfolios", json=payload)

    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "validation_error"
    assert any(detail["field"] == expected_field for detail in body["details"])


def test_portfolio_create_schema_strips_client_name():
    payload = PortfolioCreateRequest.model_validate(
        {"clientName": "  Aarav Mehta  ", "riskProfile": "balanced"}
    )

    assert payload.client_name == "Aarav Mehta"
    assert payload.risk_profile == RiskProfile.balanced


def test_portfolio_repository_create_sets_zero_cash_balance():
    class FakeSession:
        def __init__(self):
            self.added = None
            self.flushed = False

        def add(self, obj):
            self.added = obj

        def flush(self):
            self.flushed = True

    session = FakeSession()
    repository = PortfolioRepository(session)
    payload = PortfolioCreateRequest.model_validate(
        {"clientName": "Aarav Mehta", "riskProfile": "balanced"}
    )

    portfolio = repository.create(payload)

    assert session.added is portfolio
    assert session.flushed is True
    assert isinstance(portfolio, Portfolio)
    assert portfolio.client_name == "Aarav Mehta"
    assert portfolio.risk_profile == RiskProfile.balanced
    assert portfolio.cash_balance == Decimal("0.00")


def test_portfolio_service_commits_and_returns_dto():
    class FakePortfolio:
        id = uuid4()
        client_name = "Aarav Mehta"
        risk_profile = RiskProfile.balanced
        cash_balance = Decimal("0.00")

    class FakeRepository:
        def __init__(self, session):
            self.session = session
            self.called_with = None

        def create(self, data):
            self.called_with = data
            return FakePortfolio()

    class FakeSession:
        def __init__(self):
            self.committed = False
            self.refreshed = None

        def commit(self):
            self.committed = True

        def refresh(self, obj):
            self.refreshed = obj

    session = FakeSession()
    service = PortfolioService(session)
    service.repository = FakeRepository(session)
    payload = PortfolioCreateRequest.model_validate(
        {"clientName": "Aarav Mehta", "riskProfile": "balanced"}
    )

    result = service.create_portfolio(payload)

    assert session.committed is True
    assert session.refreshed is None
    assert result.model_dump(mode="json", by_alias=True) == {
        "id": str(FakePortfolio.id),
        "clientName": "Aarav Mehta",
        "riskProfile": "balanced",
        "cashBalance": "0.00",
        "message": "Portfolio created",
    }


def test_add_balance_updates_cash_balance_and_returns_dto():
    portfolio_id = uuid4()

    class FakePortfolio:
        id = portfolio_id
        client_name = "Aarav Mehta"
        risk_profile = RiskProfile.balanced
        cash_balance = Decimal("100.00")

    class FakeRepository:
        def __init__(self, session):
            self.session = session

        def get_by_id(self, _portfolio_id):
            return FakePortfolio()

    class FakeSession:
        def __init__(self):
            self.committed = False

        def commit(self):
            self.committed = True

    session = FakeSession()
    service = PortfolioService(session)
    service.repository = FakeRepository(session)
    payload = BalanceAddRequest.model_validate({"amount": "25.00"})

    result = service.add_balance(portfolio_id, payload)

    assert session.committed is True
    assert result.model_dump(mode="json", by_alias=True) == {
        "id": str(portfolio_id),
        "clientName": "Aarav Mehta",
        "riskProfile": "balanced",
        "cashBalance": "125.00",
        "message": "Balance added",
    }


def test_add_balance_returns_200_and_updated_payload(client, monkeypatch):
    portfolio_id = uuid4()

    class FakeService:
        def __init__(self, session):
            self.session = session

        def add_balance(self, _portfolio_id, data):
            return PortfolioResponse(
                id=portfolio_id,
                clientName="Aarav Mehta",
                riskProfile=RiskProfile.balanced,
                cashBalance=Decimal("125.00"),
                message="Balance added",
            )

    monkeypatch.setattr(portfolios_router, "PortfolioService", FakeService)
    app.dependency_overrides.clear()

    response = client.post(f"/v1/portfolios/{portfolio_id}/balance", json={"amount": "25.00"})

    assert response.status_code == 200
    assert response.json() == {
        "id": str(portfolio_id),
        "clientName": "Aarav Mehta",
        "riskProfile": "balanced",
        "cashBalance": "125.00",
        "message": "Balance added",
    }
