from alembic import op

revision = "0018_add_indexes_perf"
down_revision = "0017_create_app_settings"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index("ix_projects_created_at", "projects", ["created_at"])
    op.create_index("ix_files_created_at", "files", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_projects_created_at", table_name="projects")
    op.drop_index("ix_files_created_at", table_name="files")
