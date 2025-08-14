"""add project audit table

Revision ID: 0004
Revises: 0003
Create Date: 2024-07-22
"""

from alembic import op
import sqlalchemy as sa

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "project_audit",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "project_id", sa.String, sa.ForeignKey("projects.id"), nullable=False
        ),
        sa.Column("action", sa.String, nullable=False),
        sa.Column("actor_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("diff", sa.JSON, nullable=True),
    )


def downgrade():
    op.drop_table("project_audit")
