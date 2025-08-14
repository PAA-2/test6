"""add role to users

Revision ID: 0002
Revises: 0001
Create Date: 2024-07-22
"""

from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.Enum("admin", "editor", "viewer", name="user_role"),
            nullable=False,
            server_default="viewer",
        ),
    )


def downgrade():
    op.drop_column("users", "role")
    op.execute("DROP TYPE user_role")
