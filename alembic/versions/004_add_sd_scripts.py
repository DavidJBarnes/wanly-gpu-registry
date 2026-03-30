"""add sd_scripts column to workers

Revision ID: 004
Revises: 003
Create Date: 2026-03-30
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = "004"
down_revision = "003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("workers", sa.Column("sd_scripts", JSONB, nullable=True))


def downgrade() -> None:
    op.drop_column("workers", "sd_scripts")
