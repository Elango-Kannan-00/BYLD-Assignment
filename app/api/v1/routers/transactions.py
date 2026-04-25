from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.transaction import TransactionCreateRequest, TransactionResponse
from app.services.transaction_service import TransactionService

router = APIRouter(prefix="/v1/portfolios/{portfolio_id}/transactions", tags=["transactions"])


@router.post("/buy", response_model=TransactionResponse, response_model_by_alias=True, status_code=status.HTTP_201_CREATED)
def buy_transaction(
    portfolio_id: UUID,
    payload: TransactionCreateRequest,
    db: Session = Depends(get_db),
) -> TransactionResponse:
    service = TransactionService(db)
    return service.buy(portfolio_id, payload)


@router.post("/sell", response_model=TransactionResponse, response_model_by_alias=True, status_code=status.HTTP_201_CREATED)
def sell_transaction(
    portfolio_id: UUID,
    payload: TransactionCreateRequest,
    db: Session = Depends(get_db),
) -> TransactionResponse:
    service = TransactionService(db)
    return service.sell(portfolio_id, payload)
