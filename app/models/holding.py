from decimal import Decimal
from uuid import UUID as PyUUID, uuid4

from sqlalchemy import ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Holding(Base):
    __tablename__ = "holdings"
    __table_args__ = (UniqueConstraint("portfolio_id", "symbol", name="uq_holding_portfolio_symbol"),)

    id: Mapped[PyUUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    portfolio_id: Mapped[PyUUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("portfolios.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    symbol: Mapped[str] = mapped_column(String(32), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    weighted_average_cost: Mapped[Decimal] = mapped_column(
        Numeric(18, 6, asdecimal=True),
        nullable=False,
        default=Decimal("0"),
    )

    portfolio = relationship("Portfolio", back_populates="holdings")
