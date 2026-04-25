from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import Field, field_validator

from app.schemas.common import APIModel


class DividendCreateRequest(APIModel):
    symbol: str
    per_share_amount: Decimal = Field(alias="perShareAmount", gt=0)
    record_date: date = Field(alias="recordDate")

    @field_validator("symbol")
    @classmethod
    def normalize_symbol(cls, value: str) -> str:
        value = value.strip().upper()
        if not value:
            raise ValueError("symbol must not be empty")
        return value


class DividendResponse(APIModel):
    id: UUID
    portfolio_id: UUID = Field(alias="portfolioId")
    symbol: str
    quantity_held: int = Field(alias="quantityHeld")
    per_share_amount: Decimal = Field(alias="perShareAmount")
    payout: Decimal
    record_date: date = Field(alias="recordDate")


class DividendGroupResponse(APIModel):
    symbol: str
    total_dividend: Decimal = Field(alias="totalDividend")
    dividends: list[DividendResponse]
