from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.core.constants import RiskProfile


class APIModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        use_enum_values=True,
    )


class ErrorDetail(APIModel):
    field: str | None = None
    message: str


class ErrorResponse(APIModel):
    error: str
    details: list[ErrorDetail] | None = None


class UUIDResponse(APIModel):
    id: UUID


class DateTimeResponse(APIModel):
    created_at: datetime = Field(alias="createdAt")


class DateResponse(APIModel):
    record_date: date = Field(alias="recordDate")


class DecimalResponse(APIModel):
    value: Decimal
