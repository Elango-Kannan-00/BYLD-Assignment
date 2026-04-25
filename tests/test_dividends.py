from decimal import Decimal
from uuid import uuid4

from app.core.constants import RiskProfile
from app.models.dividend import Dividend
from app.services.dividend_service import DividendService
from app.schemas.dividend import DividendCreateRequest


class FakeSession:
    def __init__(self) -> None:
        self.committed = False
        self.refreshed = None
        self.added = []

    def add(self, obj):
        self.added.append(obj)

    def commit(self):
        self.committed = True

    def refresh(self, obj):
        self.refreshed = obj

    def flush(self):
        return None


def test_dividend_correctly_credits_cash_balance():
    portfolio_id = uuid4()

    class FakePortfolio:
        id = portfolio_id
        client_name = "Aarav Mehta"
        risk_profile = RiskProfile.balanced
        cash_balance = Decimal("100.00")

    class FakePortfolioRepository:
        def __init__(self, session):
            self.session = session
            self.portfolio = FakePortfolio()

        def get_by_id(self, _portfolio_id):
            return self.portfolio

    class FakeHoldingRepository:
        def __init__(self, session):
            self.session = session

        def get_quantity_as_of(self, _portfolio_id, _symbol, _record_date):
            return 12

    class FakeDividendRepository:
        def __init__(self, session):
            self.session = session

        def create(self, dividend):
            self.session.add(dividend)
            return dividend

        def list_by_portfolio(self, _portfolio_id):
            return []

    session = FakeSession()
    service = DividendService(session)
    service.portfolio_repository = FakePortfolioRepository(session)
    service.holding_repository = FakeHoldingRepository(session)
    service.dividend_repository = FakeDividendRepository(session)

    payload = DividendCreateRequest.model_validate(
        {"symbol": "aapl", "perShareAmount": "1.50", "recordDate": "2026-04-25"}
    )

    result = service.record_dividend(portfolio_id, payload)

    assert service.portfolio_repository.portfolio.cash_balance == Decimal("118.00")
    assert result.symbol == "AAPL"
    assert result.quantity_held == 12
    assert result.per_share_amount == Decimal("1.50")
    assert result.payout == Decimal("18.00")
    assert result.message == "Dividend recorded"
    assert session.committed is True
