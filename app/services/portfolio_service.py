from uuid import UUID

from sqlalchemy.orm import Session

from app.exceptions.portfolio import PortfolioNotFoundError
from app.repositories.holding_repository import HoldingRepository
from app.repositories.portfolio_repository import PortfolioRepository
from app.schemas.holding import HoldingSummaryResponse
from app.schemas.portfolio import BalanceAddRequest, PortfolioCreateRequest, PortfolioResponse, PortfolioSummaryResponse
from app.utils.money import to_money


class PortfolioService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = PortfolioRepository(session)
        self.holding_repository = HoldingRepository(session)

    def create_portfolio(self, data: PortfolioCreateRequest) -> PortfolioResponse:
        portfolio = self.repository.create(data)
        self.session.commit()
        return PortfolioResponse(
            id=portfolio.id,
            clientName=portfolio.client_name,
            riskProfile=portfolio.risk_profile,
            cashBalance=to_money(portfolio.cash_balance),
            message="Portfolio created",
        )

    def add_balance(self, portfolio_id: UUID, data: BalanceAddRequest) -> PortfolioResponse:
        portfolio = self.repository.get_by_id(portfolio_id)
        if portfolio is None:
            raise PortfolioNotFoundError()

        portfolio.cash_balance = to_money(portfolio.cash_balance + data.amount)
        self.session.commit()
        return PortfolioResponse(
            id=portfolio.id,
            clientName=portfolio.client_name,
            riskProfile=portfolio.risk_profile,
            cashBalance=to_money(portfolio.cash_balance),
            message="Balance added",
        )

    def get_portfolio_summary(self, portfolio_id: UUID) -> PortfolioSummaryResponse:
        portfolio = self.repository.get_by_id(portfolio_id)
        if portfolio is None:
            raise PortfolioNotFoundError()

        holdings = self.holding_repository.list_by_portfolio(portfolio_id)
        return PortfolioSummaryResponse(
            id=portfolio.id,
            clientName=portfolio.client_name,
            riskProfile=portfolio.risk_profile,
            cashBalance=portfolio.cash_balance,
            holdings=[
                HoldingSummaryResponse(
                    symbol=holding.symbol,
                    quantity=holding.quantity,
                    weightedAverageCostBasis=to_money(holding.weighted_average_cost),
                )
                for holding in holdings
            ],
        )

    def get_holdings(self, portfolio_id: UUID) -> list[HoldingSummaryResponse]:
        portfolio = self.repository.get_by_id(portfolio_id)
        if portfolio is None:
            raise PortfolioNotFoundError()

        holdings = self.holding_repository.list_by_portfolio(portfolio_id)
        return [
            HoldingSummaryResponse(
                symbol=holding.symbol,
                quantity=holding.quantity,
                weightedAverageCostBasis=to_money(holding.weighted_average_cost),
            )
            for holding in holdings
        ]
