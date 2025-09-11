"""added users table

Revision ID: 11e7d0df8de0
Revises: 05166ac8eb4e
Create Date: 2025-09-11 12:21:41.846260

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "11e7d0df8de0"
down_revision: Union[str, Sequence[str], None] = "05166ac8eb4e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("hashed_password", sa.String(length=100), nullable=False),
        sa.Column("nickname", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
