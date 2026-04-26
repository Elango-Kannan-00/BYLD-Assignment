"""add portfolio related tables

Revision ID: 20260425_0002
Revises: 20260424_0001
Create Date: 2026-04-25 00:02:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "20260425_0002"
down_revision: str | None = "20260424_0001"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


transaction_type_enum = postgresql.ENUM(
    "buy",
    "sell",
    name="transaction_type",
    create_type=False,
)


def upgrade() -> None:
    bind = op.get_bind()
    transaction_type_enum.create(bind, checkfirst=True)

    op.create_table(
        "holdings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("portfolio_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False),
        sa.Column("symbol", sa.String(length=32), nullable=False),
        sa.Column("quantity", sa.Numeric(18, 6, asdecimal=True), nullable=False, server_default=sa.text("0")),
        sa.Column("weighted_average_cost", sa.Numeric(19, 4, asdecimal=True), nullable=False, server_default=sa.text("0.0000")),
        sa.UniqueConstraint("portfolio_id", "symbol", name="uq_holding_portfolio_symbol"),
    )
    op.create_index(op.f("ix_holdings_portfolio_id"), "holdings", ["portfolio_id"], unique=False)

    op.create_table(
        "transactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("portfolio_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False),
        sa.Column("symbol", sa.String(length=32), nullable=False),
        sa.Column("transaction_type", transaction_type_enum, nullable=False),
        sa.Column("quantity", sa.Numeric(18, 6, asdecimal=True), nullable=False),
        sa.Column("price", sa.Numeric(19, 4, asdecimal=True), nullable=False),
        sa.Column("total_amount", sa.Numeric(19, 4, asdecimal=True), nullable=False),
        sa.Column("transacted_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index(op.f("ix_transactions_portfolio_id"), "transactions", ["portfolio_id"], unique=False)
    op.create_index(op.f("ix_transactions_symbol"), "transactions", ["symbol"], unique=False)

    op.create_table(
        "dividends",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("portfolio_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False),
        sa.Column("symbol", sa.String(length=32), nullable=False),
        sa.Column("quantity_held", sa.Numeric(18, 6, asdecimal=True), nullable=False),
        sa.Column("per_share_amount", sa.Numeric(19, 4, asdecimal=True), nullable=False),
        sa.Column("payout", sa.Numeric(19, 4, asdecimal=True), nullable=False),
        sa.Column("record_date", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index(op.f("ix_dividends_portfolio_id"), "dividends", ["portfolio_id"], unique=False)
    op.create_index(op.f("ix_dividends_symbol"), "dividends", ["symbol"], unique=False)
    op.create_index(op.f("ix_dividends_record_date"), "dividends", ["record_date"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_dividends_record_date"), table_name="dividends")
    op.drop_index(op.f("ix_dividends_symbol"), table_name="dividends")
    op.drop_index(op.f("ix_dividends_portfolio_id"), table_name="dividends")
    op.drop_table("dividends")

    op.drop_index(op.f("ix_transactions_symbol"), table_name="transactions")
    op.drop_index(op.f("ix_transactions_portfolio_id"), table_name="transactions")
    op.drop_table("transactions")

    op.drop_index(op.f("ix_holdings_portfolio_id"), table_name="holdings")
    op.drop_table("holdings")

    transaction_type_enum.drop(op.get_bind(), checkfirst=True)
