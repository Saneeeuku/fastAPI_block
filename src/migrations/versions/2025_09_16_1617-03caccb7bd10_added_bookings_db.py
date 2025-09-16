"""added bookings db

Revision ID: 03caccb7bd10
Revises: 11e7d0df8de0
Create Date: 2025-09-16 16:17:49.436818

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "03caccb7bd10"
down_revision: Union[str, Sequence[str], None] = "11e7d0df8de0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("date_from", sa.DateTime(timezone=True), nullable=False),
        sa.Column("date_to", sa.DateTime(timezone=True), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("bookings")
