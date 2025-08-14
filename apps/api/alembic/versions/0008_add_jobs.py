"""add jobs table

Revision ID: 0008
Revises: 0007_add_indexes_for_analytics
Create Date: 2024-07-22
"""

from alembic import op
import sqlalchemy as sa

revision = "0008"
down_revision = "0007_add_indexes_for_analytics"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "jobs",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("type", sa.String, nullable=False),
        sa.Column("args", sa.JSON, nullable=True),
        sa.Column("status", sa.String, nullable=False),
        sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id"), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_text", sa.String, nullable=True),
    )


def downgrade():
    op.drop_table("jobs")
