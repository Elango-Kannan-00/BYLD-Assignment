from sqlalchemy.orm import Session

from app.repositories.portfolio_repository import PortfolioRepository
from app.schemas.portfolio import PortfolioCreateRequest, PortfolioResponse


class PortfolioService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = PortfolioRepository(session)

    def create_portfolio(self, data: PortfolioCreateRequest) -> PortfolioResponse:
        portfolio = self.repository.create(data)
        self.session.commit()
        self.session.refresh(portfolio)
        return PortfolioResponse.model_validate(portfolio)
