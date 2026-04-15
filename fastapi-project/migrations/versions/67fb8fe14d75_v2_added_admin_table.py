"""v2_added_admin_table

Revision ID: 67fb8fe14d75
Revises: 0732e7817804
Create Date: 2026-04-14 18:05:31.826622

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "67fb8fe14d75"
down_revision: Union[str, Sequence[str], None] = "0732e7817804"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "admin",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement="auto", index=True),
        sa.Column("guid", sa.String(36), nullable=False),
        sa.Column("username", sa.String(30), nullable=False),
        sa.Column("email", sa.String(100), nullable=False),
        sa.Column("password_hash", sa.String(100), nullable=False),
        sa.Column(
            "createdAt", sa.TIMESTAMP, server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updatedAt",
            sa.TIMESTAMP,
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("admin")