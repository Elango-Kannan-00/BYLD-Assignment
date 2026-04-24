from datetime import datetime
from decimal import Decimal
from uuid import UUID as PyUUID, uuid4

from sqlalchemy import DateTime, Enum as SAEnum, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import RiskProfile
from app.models.base import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id: Mapped[PyUUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    client_name: Mapped[str] = mapped_column(String(255), nullable=False)
    risk_profile: Mapped[RiskProfile] = mapped_column(SAEnum(RiskProfile, name="risk_profile"), nullable=False)
    cash_balance: Mapped[Decimal] = mapped_column(
        Numeric(18, 2, asdecimal=True),
        nullable=False,
        default=Decimal("0.00"),
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
