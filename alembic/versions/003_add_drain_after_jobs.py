"""add drain_after_jobs column to workers

Revision ID: 003
Revises: 002
Create Date: 2026-03-12
"""

from alembic import op
import sqlalchemy as sa

revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("workers", sa.Column("drain_after_jobs", sa.Integer, nullable=True))


def downgrade() -> None:
    op.drop_column("workers", "drain_after_jobs")
