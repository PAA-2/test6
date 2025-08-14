"""add notifications table and email pref

Revision ID: 0006
Revises: 0005
Create Date: 2024-07-22
"""

from alembic import op
import sqlalchemy as sa

revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users",
        sa.Column(
            "email_notifications", sa.Boolean(), server_default="1", nullable=False
        ),
    )
    op.create_table(
        "notifications",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("type", sa.String, nullable=False),
        sa.Column("message", sa.String, nullable=False),
        sa.Column("data", sa.JSON, nullable=True),
        sa.Column("read", sa.Boolean, server_default="0", nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )


def downgrade():
    op.drop_table("notifications")
    op.drop_column("users", "email_notifications")
