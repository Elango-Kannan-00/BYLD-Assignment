from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.dividend import Dividend


class DividendRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, dividend: Dividend) -> Dividend:
        self.session.add(dividend)
        self.session.flush()
        return dividend

    def list_by_portfolio(self, portfolio_id: UUID) -> list[Dividend]:
        statement = select(Dividend).where(Dividend.portfolio_id == portfolio_id).order_by(
            Dividend.symbol.asc(),
            Dividend.record_date.asc(),
        )
        return list(self.session.scalars(statement).all())
