"""updated bookings columns

Revision ID: 988d3d11939f
Revises: 03caccb7bd10
Create Date: 2025-09-18 14:52:30.506421

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "988d3d11939f"
down_revision: Union[str, Sequence[str], None] = "03caccb7bd10"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "bookings",
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
    )
    op.alter_column(
        "bookings",
        "date_from",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        type_=sa.Date(),
        existing_nullable=False,
    )
    op.alter_column(
        "bookings",
        "date_to",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        type_=sa.Date(),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "bookings",
        "date_to",
        existing_type=sa.Date(),
        type_=postgresql.TIMESTAMP(timezone=True),
        existing_nullable=False,
    )
    op.alter_column(
        "bookings",
        "date_from",
        existing_type=sa.Date(),
        type_=postgresql.TIMESTAMP(timezone=True),
        existing_nullable=False,
    )
    op.drop_column("bookings", "created_at")
