from alembic import op
import sqlalchemy as sa

revision = "0015_create_audit_log"
down_revision = "0014_create_webhook_deliveries"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("actor_id", sa.dialects.postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("org_id", sa.dialects.postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("action", sa.String(), nullable=False),
        sa.Column("target_type", sa.String(), nullable=True),
        sa.Column(
            "target_id", sa.dialects.postgresql.UUID(as_uuid=True), nullable=True
        ),
        sa.Column("ip", sa.String(), nullable=True),
        sa.Column("user_agent", sa.String(), nullable=True),
        sa.Column("success", sa.Boolean(), default=True),
        sa.Column("details", sa.JSON()),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )


def downgrade() -> None:
    op.drop_table("audit_logs")
