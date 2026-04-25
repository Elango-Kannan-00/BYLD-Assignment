from decimal import Decimal
from uuid import UUID

from pydantic import Field, field_validator

from app.schemas.common import APIModel, RiskProfile


class PortfolioCreateRequest(APIModel):
    client_name: str = Field(alias="clientName", min_length=1)
    risk_profile: RiskProfile = Field(alias="riskProfile")

    @field_validator("client_name")
    @classmethod
    def validate_client_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("clientName must not be empty")
        return value


class PortfolioResponse(APIModel):
    id: UUID
    client_name: str = Field(alias="clientName")
    risk_profile: RiskProfile = Field(alias="riskProfile")
    cash_balance: Decimal = Field(alias="cashBalance")


class PortfolioSummaryResponse(APIModel):
    id: UUID
    client_name: str = Field(alias="clientName")
    risk_profile: RiskProfile = Field(alias="riskProfile")
    cash_balance: Decimal = Field(alias="cashBalance")
    holdings: list["HoldingSummaryResponse"] = Field(default_factory=list)


from app.schemas.holding import HoldingSummaryResponse  # noqa: E402

PortfolioSummaryResponse.model_rebuild()
