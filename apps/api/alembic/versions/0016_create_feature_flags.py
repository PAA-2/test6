from alembic import op
import sqlalchemy as sa

revision = "0016_create_feature_flags"
down_revision = "0015_create_audit_log"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "feature_flags",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("key", sa.String(), unique=True, nullable=False),
        sa.Column("enabled", sa.Boolean(), default=False),
        sa.Column("audience", sa.JSON()),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )


def downgrade() -> None:
    op.drop_table("feature_flags")
