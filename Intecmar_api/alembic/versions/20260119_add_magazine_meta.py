"""add selected_ids and meta columns to magazines

Revision ID: 20260119_add_magazine_meta
Revises: 54be63374743_add_flows_table
Create Date: 2026-01-19

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260119_add_magazine_meta"
down_revision = "54be63374743_add_flows_table"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("magazines", sa.Column("selected_ids", sa.JSON(), nullable=True))
    op.add_column("magazines", sa.Column("meta", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column("magazines", "meta")
    op.drop_column("magazines", "selected_ids")
