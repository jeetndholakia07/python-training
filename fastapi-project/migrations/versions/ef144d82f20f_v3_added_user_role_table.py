"""v3_added_user_role_table

Revision ID: ef144d82f20f
Revises: 67fb8fe14d75
Create Date: 2026-04-15 15:59:21.152823

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from schemas.user_schema import Role

# revision identifiers, used by Alembic.
revision: str = "ef144d82f20f"
down_revision: Union[str, Sequence[str], None] = "67fb8fe14d75"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table("admin", "user")
    op.add_column(
        "user",
        sa.Column("role", sa.Enum(Role), nullable=False),
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("user", "role")
    op.rename_table(
        "user",
        "admin",
    )
    pass