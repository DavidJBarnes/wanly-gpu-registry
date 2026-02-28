"""add gpu_stats column to workers

Revision ID: 002
Revises: 001
Create Date: 2026-02-28
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("workers", sa.Column("gpu_stats", JSONB, nullable=True))


def downgrade() -> None:
    op.drop_column("workers", "gpu_stats")
