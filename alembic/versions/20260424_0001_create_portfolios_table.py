"""create portfolios table

Revision ID: 20260424_0001
Revises: 
Create Date: 2026-04-24 00:01:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "20260424_0001"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


risk_profile_enum = postgresql.ENUM(
    "conservative",
    "balanced",
    "aggressive",
    name="risk_profile",
    create_type=False,
)


def upgrade() -> None:
    bind = op.get_bind()
    risk_profile_enum.create(bind, checkfirst=True)

    op.create_table(
        "portfolios",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("client_name", sa.String(length=255), nullable=False),
        sa.Column("risk_profile", risk_profile_enum, nullable=False),
        sa.Column("cash_balance", sa.Numeric(18, 2, asdecimal=True), nullable=False, server_default=sa.text("0.00")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("portfolios")
    risk_profile_enum.drop(op.get_bind(), checkfirst=True)
