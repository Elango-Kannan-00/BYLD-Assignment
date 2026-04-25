from decimal import Decimal
from uuid import uuid4

from app.core.constants import RiskProfile
from app.models.holding import Holding
from app.services.portfolio_service import PortfolioService


class FakeSession:
    def __init__(self) -> None:
        self.committed = False

    def commit(self):
        self.committed = True

    def refresh(self, obj):
        return None


def test_portfolio_service_returns_holdings_summary():
    portfolio_id = uuid4()

    class FakePortfolio:
        id = portfolio_id
        client_name = "Aarav Mehta"
        risk_profile = RiskProfile.balanced
        cash_balance = Decimal("0.00")

    class FakePortfolioRepository:
        def __init__(self, session):
            self.session = session

        def get_by_id(self, _portfolio_id):
            return FakePortfolio()

    class FakeHoldingRepository:
        def __init__(self, session):
            self.session = session

        def list_by_portfolio(self, _portfolio_id):
            return [
                Holding(
                    portfolio_id=portfolio_id,
                    symbol="AAPL",
                    quantity=10,
                    weighted_average_cost=Decimal("100"),
                ),
                Holding(
                    portfolio_id=portfolio_id,
                    symbol="MSFT",
                    quantity=3,
                    weighted_average_cost=Decimal("200"),
                ),
            ]

    session = FakeSession()
    service = PortfolioService(session)
    service.repository = FakePortfolioRepository(session)
    service.holding_repository = FakeHoldingRepository(session)

    result = service.get_holdings(portfolio_id)

    assert [item.symbol for item in result] == ["AAPL", "MSFT"]
    assert result[0].weighted_average_cost == Decimal("100")
    assert result[1].quantity == 3
