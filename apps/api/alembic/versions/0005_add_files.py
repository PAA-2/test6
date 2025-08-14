"""add files table

Revision ID: 0005
Revises: 0004
Create Date: 2024-07-22
"""

from alembic import op
import sqlalchemy as sa

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "files",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("original_name", sa.String, nullable=False),
        sa.Column("stored_name", sa.String, nullable=False),
        sa.Column("mime_type", sa.String, nullable=False),
        sa.Column("size_bytes", sa.Integer, nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )


def downgrade():
    op.drop_table("files")
