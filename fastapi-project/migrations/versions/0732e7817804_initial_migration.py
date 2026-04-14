"""initial migration

Revision ID: 0732e7817804
Revises:
Create Date: 2026-04-14 10:51:58.669409

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import relationship


# revision identifiers, used by Alembic.
revision: str = "0732e7817804"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """Upgrade schema."""
    op.create_table(
        "company",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement="auto", index=True),
        sa.Column("guid", sa.String(36), nullable=False),
        sa.Column("companyName", sa.String(30), nullable=False),
        sa.Column("description", sa.String(50)),
        sa.Column("status", sa.Enum("A", "D"), default="A"),
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
        relationship("Employee", back_populates="company", lazy="selectin"),
    )

    op.create_table(
        "employee",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement="auto", index=True),
        sa.Column("guid", sa.String(36), nullable=False),
        sa.Column("employeeName", sa.String(50), nullable=False),
        sa.Column("designation", sa.String(30)),
        sa.Column("salary", sa.Numeric(10,2)),
        sa.Column("status", sa.Enum("A", "D"), default="A"),
        sa.Column("companyId", sa.Integer, sa.ForeignKey("company.id")),
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
        relationship("Company", back_populates="employees", lazy="selectin")
    )

def downgrade():
    """Downgrade schema."""
    op.drop_table("employee")
    op.drop_table("company")
    pass
