from uuid import UUID

from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.portfolio import Portfolio
from app.schemas.portfolio import PortfolioCreateRequest


class PortfolioRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, data: PortfolioCreateRequest) -> Portfolio:
        portfolio = Portfolio(
            client_name=data.client_name,
            risk_profile=data.risk_profile,
            cash_balance=Decimal("0.00"),
        )
        self.session.add(portfolio)
        self.session.flush()
        return portfolio

    def get_by_id(self, portfolio_id: UUID) -> Portfolio | None:
        return self.session.get(Portfolio, portfolio_id)
