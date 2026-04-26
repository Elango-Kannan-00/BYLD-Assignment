"""set money precision to 19.4

Revision ID: 20260426_0004
Revises: 20260425_0003
Create Date: 2026-04-26 00:04:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260426_0004"
down_revision: str | None = "20260425_0003"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        "portfolios",
        "cash_balance",
        type_=sa.Numeric(19, 4, asdecimal=True),
        existing_nullable=False,
        existing_server_default=sa.text("0.0000"),
        postgresql_using="cash_balance::numeric(19,4)",
    )

    op.alter_column(
        "holdings",
        "weighted_average_cost",
        type_=sa.Numeric(19, 4, asdecimal=True),
        existing_nullable=False,
        existing_server_default=sa.text("0.0000"),
        postgresql_using="weighted_average_cost::numeric(19,4)",
    )

    op.alter_column(
        "transactions",
        "price",
        type_=sa.Numeric(19, 4, asdecimal=True),
        existing_nullable=False,
        postgresql_using="price::numeric(19,4)",
    )

    op.alter_column(
        "transactions",
        "total_amount",
        type_=sa.Numeric(19, 4, asdecimal=True),
        existing_nullable=False,
        postgresql_using="total_amount::numeric(19,4)",
    )

    op.alter_column(
        "dividends",
        "per_share_amount",
        type_=sa.Numeric(19, 4, asdecimal=True),
        existing_nullable=False,
        postgresql_using="per_share_amount::numeric(19,4)",
    )

    op.alter_column(
        "dividends",
        "payout",
        type_=sa.Numeric(19, 4, asdecimal=True),
        existing_nullable=False,
        postgresql_using="payout::numeric(19,4)",
    )


def downgrade() -> None:
    op.alter_column(
        "dividends",
        "payout",
        type_=sa.Numeric(18, 6, asdecimal=True),
        existing_nullable=False,
        postgresql_using="payout::numeric(18,6)",
    )

    op.alter_column(
        "dividends",
        "per_share_amount",
        type_=sa.Numeric(18, 6, asdecimal=True),
        existing_nullable=False,
        postgresql_using="per_share_amount::numeric(18,6)",
    )

    op.alter_column(
        "transactions",
        "total_amount",
        type_=sa.Numeric(18, 6, asdecimal=True),
        existing_nullable=False,
        postgresql_using="total_amount::numeric(18,6)",
    )

    op.alter_column(
        "transactions",
        "price",
        type_=sa.Numeric(18, 6, asdecimal=True),
        existing_nullable=False,
        postgresql_using="price::numeric(18,6)",
    )

    op.alter_column(
        "holdings",
        "weighted_average_cost",
        type_=sa.Numeric(18, 6, asdecimal=True),
        existing_nullable=False,
        existing_server_default=sa.text("0.0000"),
        postgresql_using="weighted_average_cost::numeric(18,6)",
    )

    op.alter_column(
        "portfolios",
        "cash_balance",
        type_=sa.Numeric(18, 2, asdecimal=True),
        existing_nullable=False,
        existing_server_default=sa.text("0.00"),
        postgresql_using="cash_balance::numeric(18,2)",
    )
