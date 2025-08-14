"""add indexes for analytics"""

from alembic import op

revision = "0007"
down_revision = "0006"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index("ix_projects_status", "projects", ["status"])
    op.create_index("ix_projects_created_at", "projects", ["created_at"])
    op.create_index("ix_files_owner_id", "files", ["owner_id"])
    op.create_index("ix_files_mime_type", "files", ["mime_type"])
    op.create_index("ix_notifications_user_read", "notifications", ["user_id", "read"])


def downgrade():
    op.drop_index("ix_notifications_user_read", table_name="notifications")
    op.drop_index("ix_files_mime_type", table_name="files")
    op.drop_index("ix_files_owner_id", table_name="files")
    op.drop_index("ix_projects_created_at", table_name="projects")
    op.drop_index("ix_projects_status", table_name="projects")
