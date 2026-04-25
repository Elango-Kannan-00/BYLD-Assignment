from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.dividend import DividendCreateRequest, DividendGroupResponse, DividendResponse
from app.services.dividend_service import DividendService

router = APIRouter(prefix="/v1/portfolios/{portfolio_id}/dividends", tags=["dividends"])


@router.post("", response_model=DividendResponse, response_model_by_alias=True, status_code=status.HTTP_201_CREATED)
def create_dividend(
    portfolio_id: UUID,
    payload: DividendCreateRequest,
    db: Session = Depends(get_db),
) -> DividendResponse:
    service = DividendService(db)
    return service.record_dividend(portfolio_id, payload)


@router.get("", response_model=list[DividendGroupResponse], response_model_by_alias=True)
def list_dividends(
    portfolio_id: UUID,
    db: Session = Depends(get_db),
) -> list[DividendGroupResponse]:
    service = DividendService(db)
    return service.list_dividends(portfolio_id)
