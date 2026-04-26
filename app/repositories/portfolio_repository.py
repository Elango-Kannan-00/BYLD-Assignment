from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app.models.portfolio import Portfolio
from app.schemas.portfolio import PortfolioCreateRequest
from app.utils.money import to_money


class PortfolioRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, data: PortfolioCreateRequest) -> Portfolio:
        portfolio = Portfolio(
            id=uuid4(),
            client_name=data.client_name,
            risk_profile=data.risk_profile,
            cash_balance=to_money(Decimal("0")),
        )
        self.session.add(portfolio)
        self.session.flush()
        return portfolio

    def get_by_id(self, portfolio_id: UUID) -> Portfolio | None:
        return self.session.get(Portfolio, portfolio_id)
