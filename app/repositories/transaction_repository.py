from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.transaction import Transaction


class TransactionRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, transaction: Transaction) -> Transaction:
        self.session.add(transaction)
        self.session.flush()
        return transaction

    def list_by_portfolio(self, portfolio_id: UUID) -> list[Transaction]:
        statement = select(Transaction).where(Transaction.portfolio_id == portfolio_id).order_by(
            Transaction.symbol.asc(),
            Transaction.transacted_at.asc(),
        )
        return list(self.session.scalars(statement).all())
