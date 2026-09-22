"""initial expense schema

Revision ID: b20547a6e8be
Revises:
Create Date: 2026-09-22
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b20547a6e8be"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "expenses",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("amount", sa.Float(), nullable=True),
        sa.Column("category", sa.String(), nullable=True),
        sa.Column("date", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id")
    )


def downgrade():
    op.drop_table("expenses")