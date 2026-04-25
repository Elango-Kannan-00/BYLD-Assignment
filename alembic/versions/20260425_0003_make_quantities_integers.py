"""make quantities integers

Revision ID: 20260425_0003
Revises: 20260425_0002
Create Date: 2026-04-25 00:03:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260425_0003"
down_revision: str | None = "20260425_0002"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        "holdings",
        "quantity",
        existing_type=sa.Numeric(18, 6, asdecimal=True),
        type_=sa.Integer(),
        existing_nullable=False,
        postgresql_using="quantity::integer",
        existing_server_default=sa.text("0"),
    )

    op.alter_column(
        "transactions",
        "quantity",
        existing_type=sa.Numeric(18, 6, asdecimal=True),
        type_=sa.Integer(),
        existing_nullable=False,
        postgresql_using="quantity::integer",
    )

    op.alter_column(
        "dividends",
        "quantity_held",
        existing_type=sa.Numeric(18, 6, asdecimal=True),
        type_=sa.Integer(),
        existing_nullable=False,
        postgresql_using="quantity_held::integer",
    )


def downgrade() -> None:
    op.alter_column(
        "dividends",
        "quantity_held",
        existing_type=sa.Integer(),
        type_=sa.Numeric(18, 6, asdecimal=True),
        existing_nullable=False,
        postgresql_using="quantity_held::numeric(18,6)",
    )

    op.alter_column(
        "transactions",
        "quantity",
        existing_type=sa.Integer(),
        type_=sa.Numeric(18, 6, asdecimal=True),
        existing_nullable=False,
        postgresql_using="quantity::numeric(18,6)",
    )

    op.alter_column(
        "holdings",
        "quantity",
        existing_type=sa.Integer(),
        type_=sa.Numeric(18, 6, asdecimal=True),
        existing_nullable=False,
        postgresql_using="quantity::numeric(18,6)",
    )
