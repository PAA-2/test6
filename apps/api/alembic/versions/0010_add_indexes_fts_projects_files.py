from alembic import op

# revision identifiers, used by Alembic.
revision = "0010_add_indexes_fts_projects_files"
down_revision = "0009_enable_pg_trgm"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_projects_fts ON projects USING GIN (
            to_tsvector('simple', coalesce(name,'') || ' ' || coalesce(description,''))
        );
        CREATE INDEX IF NOT EXISTS idx_files_fts ON files USING GIN (
            to_tsvector('simple', coalesce(original_name,'') || ' ' || coalesce(mime_type,''))
        );
        CREATE INDEX IF NOT EXISTS idx_projects_name_trgm ON projects USING GIN (name gin_trgm_ops);
        CREATE INDEX IF NOT EXISTS idx_files_name_trgm ON files USING GIN (original_name gin_trgm_ops);
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP INDEX IF EXISTS idx_projects_fts;
        DROP INDEX IF EXISTS idx_files_fts;
        DROP INDEX IF EXISTS idx_projects_name_trgm;
        DROP INDEX IF EXISTS idx_files_name_trgm;
        """
    )
