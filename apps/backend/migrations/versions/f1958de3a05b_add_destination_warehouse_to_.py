"""add destination warehouse to transactions

Revision ID: f1958de3a05b
Revises: 63473f7b13d0
Create Date: 2026-09-11 14:02:53.584241

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f1958de3a05b"
down_revision: str | Sequence[str] | None = "63473f7b13d0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "transactions",
        sa.Column("destination_warehouse_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        None,
        "transactions",
        "warehouses",
        ["destination_warehouse_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(None, "transactions", type_="foreignkey")
    op.drop_column("transactions", "destination_warehouse_id")
