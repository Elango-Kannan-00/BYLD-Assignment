from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.holding import HoldingSummaryResponse
from app.schemas.portfolio import PortfolioCreateRequest, PortfolioResponse, PortfolioSummaryResponse
from app.services.portfolio_service import PortfolioService

router = APIRouter(prefix="/v1/portfolios", tags=["portfolios"])


@router.post("", response_model=PortfolioResponse, response_model_by_alias=True, status_code=status.HTTP_201_CREATED)
def create_portfolio(
    payload: PortfolioCreateRequest,
    response: Response,
    db: Session = Depends(get_db),
) -> PortfolioResponse:
    service = PortfolioService(db)
    created = service.create_portfolio(payload)
    response.headers["Location"] = f"/v1/portfolios/{created.id}"
    return created


@router.get("/{portfolio_id}", response_model=PortfolioSummaryResponse, response_model_by_alias=True)
def get_portfolio_summary(portfolio_id: UUID, db: Session = Depends(get_db)) -> PortfolioSummaryResponse:
    service = PortfolioService(db)
    return service.get_portfolio_summary(portfolio_id)


@router.get("/{portfolio_id}/holdings", response_model=list[HoldingSummaryResponse], response_model_by_alias=True)
def get_holdings(portfolio_id: UUID, db: Session = Depends(get_db)) -> list[HoldingSummaryResponse]:
    service = PortfolioService(db)
    return service.get_holdings(portfolio_id)
