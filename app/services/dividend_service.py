from collections import defaultdict
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app.exceptions.portfolio import PortfolioNotFoundError
from app.models.dividend import Dividend
from app.repositories.dividend_repository import DividendRepository
from app.repositories.holding_repository import HoldingRepository
from app.repositories.portfolio_repository import PortfolioRepository
from app.schemas.dividend import DividendCreateRequest, DividendGroupResponse, DividendResponse


class DividendService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.portfolio_repository = PortfolioRepository(session)
        self.holding_repository = HoldingRepository(session)
        self.dividend_repository = DividendRepository(session)

    def record_dividend(self, portfolio_id: UUID, data: DividendCreateRequest) -> DividendResponse:
        portfolio = self._get_portfolio(portfolio_id)
        quantity_held = self.holding_repository.get_quantity_as_of(portfolio_id, data.symbol, data.record_date)
        payout = Decimal(quantity_held) * data.per_share_amount

        dividend = Dividend(
            id=uuid4(),
            portfolio_id=portfolio.id,
            symbol=data.symbol,
            quantity_held=quantity_held,
            per_share_amount=data.per_share_amount,
            payout=payout,
            record_date=data.record_date,
        )
        self.dividend_repository.create(dividend)
        portfolio.cash_balance = portfolio.cash_balance + payout
        self.session.commit()
        return DividendResponse(
            id=dividend.id,
            portfolioId=dividend.portfolio_id,
            symbol=dividend.symbol,
            quantityHeld=dividend.quantity_held,
            perShareAmount=dividend.per_share_amount,
            payout=dividend.payout,
            recordDate=dividend.record_date,
            message="Dividend recorded",
        )

    def list_dividends(self, portfolio_id: UUID) -> list[DividendGroupResponse]:
        portfolio = self._get_portfolio(portfolio_id)
        _ = portfolio
        dividends = self.dividend_repository.list_by_portfolio(portfolio_id)
        grouped: dict[str, list[DividendResponse]] = defaultdict(list)
        totals: dict[str, Decimal] = defaultdict(lambda: Decimal("0"))

        for dividend in dividends:
            response = DividendResponse.model_validate(dividend)
            grouped[dividend.symbol].append(response)
            totals[dividend.symbol] += dividend.payout

        return [
            DividendGroupResponse(
                symbol=symbol,
                totalDividend=totals[symbol],
                dividends=records,
            )
            for symbol, records in grouped.items()
        ]

    def _get_portfolio(self, portfolio_id: UUID):
        portfolio = self.portfolio_repository.get_by_id(portfolio_id)
        if portfolio is None:
            raise PortfolioNotFoundError()
        return portfolio
