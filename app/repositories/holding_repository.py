from datetime import date
from uuid import UUID

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.models.holding import Holding
from app.models.transaction import Transaction
from app.core.constants import TransactionType


class HoldingRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_portfolio_and_symbol(self, portfolio_id: UUID, symbol: str) -> Holding | None:
        statement = select(Holding).where(Holding.portfolio_id == portfolio_id, Holding.symbol == symbol)
        return self.session.scalars(statement).first()

    def list_by_portfolio(self, portfolio_id: UUID) -> list[Holding]:
        statement = select(Holding).where(Holding.portfolio_id == portfolio_id).order_by(Holding.symbol.asc())
        return list(self.session.scalars(statement).all())

    def get_quantity_as_of(self, portfolio_id: UUID, symbol: str, record_date: date) -> int:
        transaction_effect = case(
            (Transaction.transaction_type == TransactionType.buy, Transaction.quantity),
            else_=-Transaction.quantity,
        )
        statement = (
            select(func.coalesce(func.sum(transaction_effect), 0))
            .where(
                Transaction.portfolio_id == portfolio_id,
                Transaction.symbol == symbol,
                func.date(Transaction.transacted_at) <= record_date,
            )
        )
        return int(self.session.scalar(statement) or 0)
