from decimal import Decimal
from uuid import UUID

from pydantic import Field, field_validator

from app.core.constants import TransactionType
from app.schemas.common import APIModel


class TransactionCreateRequest(APIModel):
    symbol: str
    quantity: int = Field(gt=0)
    price: Decimal = Field(gt=0)

    @field_validator("symbol")
    @classmethod
    def normalize_symbol(cls, value: str) -> str:
        value = value.strip().upper()
        if not value:
            raise ValueError("symbol must not be empty")
        return value


class TransactionResponse(APIModel):
    id: UUID
    portfolio_id: UUID = Field(alias="portfolioId")
    symbol: str
    transaction_type: TransactionType = Field(alias="transactionType")
    quantity: int
    price: Decimal
    total_amount: Decimal = Field(alias="totalAmount")
