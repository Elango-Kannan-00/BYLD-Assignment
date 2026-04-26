from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app.core.constants import TransactionType
from app.exceptions.portfolio import PortfolioNotFoundError
from app.exceptions.transaction import InsufficientHoldingError
from app.models.holding import Holding
from app.models.transaction import Transaction
from app.repositories.holding_repository import HoldingRepository
from app.repositories.portfolio_repository import PortfolioRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction import TransactionCreateRequest, TransactionResponse
from app.utils.money import money_mul, to_money


class TransactionService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.portfolio_repository = PortfolioRepository(session)
        self.holding_repository = HoldingRepository(session)
        self.transaction_repository = TransactionRepository(session)

    def buy(self, portfolio_id: UUID, data: TransactionCreateRequest) -> TransactionResponse:
        portfolio = self._get_portfolio(portfolio_id)
        holding = self.holding_repository.get_by_portfolio_and_symbol(portfolio_id, data.symbol)

        quantity = data.quantity
        price = data.price
        total_amount = money_mul(quantity, price)

        if holding is None:
            holding = Holding(
                id=uuid4(),
                portfolio_id=portfolio_id,
                symbol=data.symbol,
                quantity=quantity,
                weighted_average_cost=to_money(price),
            )
            self.session.add(holding)
        else:
            existing_quantity = holding.quantity
            new_quantity = existing_quantity + quantity
            existing_cost = money_mul(existing_quantity, holding.weighted_average_cost)
            holding.weighted_average_cost = to_money((existing_cost + total_amount) / Decimal(new_quantity))
            holding.quantity = new_quantity

        transaction = Transaction(
            id=uuid4(),
            portfolio_id=portfolio.id,
            symbol=data.symbol,
            transaction_type=TransactionType.buy,
            quantity=quantity,
            price=to_money(price),
            total_amount=total_amount,
        )
        self.transaction_repository.create(transaction)
        self.session.commit()
        return self._to_response(transaction, "Purchased the stock")

    def sell(self, portfolio_id: UUID, data: TransactionCreateRequest) -> TransactionResponse:
        portfolio = self._get_portfolio(portfolio_id)
        holding = self.holding_repository.get_by_portfolio_and_symbol(portfolio_id, data.symbol)
        if holding is None or holding.quantity < data.quantity:
            raise InsufficientHoldingError()

        holding.quantity = holding.quantity - data.quantity
        if holding.quantity == 0:
            self.session.delete(holding)

        transaction = Transaction(
            id=uuid4(),
            portfolio_id=portfolio.id,
            symbol=data.symbol,
            transaction_type=TransactionType.sell,
            quantity=data.quantity,
            price=to_money(data.price),
            total_amount=money_mul(data.quantity, data.price),
        )
        self.transaction_repository.create(transaction)
        self.session.commit()
        return self._to_response(transaction, "Sold the stock")

    def _get_portfolio(self, portfolio_id: UUID):
        portfolio = self.portfolio_repository.get_by_id(portfolio_id)
        if portfolio is None:
            raise PortfolioNotFoundError()
        return portfolio

    def _to_response(self, transaction: Transaction, message: str) -> TransactionResponse:
        return TransactionResponse(
            id=transaction.id,
            portfolioId=transaction.portfolio_id,
            symbol=transaction.symbol,
            transactionType=transaction.transaction_type,
            quantity=transaction.quantity,
            price=transaction.price,
            totalAmount=transaction.total_amount,
            message=message,
        )
