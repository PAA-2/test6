from alembic import op
import sqlalchemy as sa

revision = "0017_create_app_settings"
down_revision = "0016_create_feature_flags"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "app_settings",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("key", sa.String(), unique=True, nullable=False),
        sa.Column("value", sa.JSON()),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )


def downgrade() -> None:
    op.drop_table("app_settings")
