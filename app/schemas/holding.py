from decimal import Decimal
from uuid import UUID

from pydantic import Field, field_validator

from app.schemas.common import APIModel


class HoldingSummaryResponse(APIModel):
    symbol: str
    quantity: int
    weighted_average_cost: Decimal = Field(alias="weightedAverageCostBasis")


class HoldingUpsertRequest(APIModel):
    symbol: str
    quantity: int = Field(gt=0)
    price: Decimal = Field(gt=0)

    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, value: str) -> str:
        value = value.strip().upper()
        if not value:
            raise ValueError("symbol must not be empty")
        return value


HoldingSummaryResponse.model_rebuild()
