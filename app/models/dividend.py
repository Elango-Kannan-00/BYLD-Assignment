from datetime import date, datetime
from decimal import Decimal
from uuid import UUID as PyUUID, uuid4

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Dividend(Base):
    __tablename__ = "dividends"

    id: Mapped[PyUUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    portfolio_id: Mapped[PyUUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("portfolios.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    symbol: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    quantity_held: Mapped[int] = mapped_column(Integer, nullable=False)
    per_share_amount: Mapped[Decimal] = mapped_column(Numeric(19, 4, asdecimal=True), nullable=False)
    payout: Mapped[Decimal] = mapped_column(Numeric(19, 4, asdecimal=True), nullable=False)
    record_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    portfolio = relationship("Portfolio", back_populates="dividends")
