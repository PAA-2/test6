from alembic import op
import sqlalchemy as sa

revision = "0014_create_webhook_deliveries"
down_revision = "0013_create_webhook_endpoints"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "webhook_deliveries",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column(
            "endpoint_id",
            sa.String(),
            sa.ForeignKey("webhook_endpoints.id"),
            nullable=False,
        ),
        sa.Column("event", sa.String(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(), nullable=False, server_default="pending"),
        sa.Column("response_code", sa.Integer()),
        sa.Column("attempts", sa.Integer(), server_default="0"),
        sa.Column("next_retry_at", sa.DateTime(timezone=True)),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )


def downgrade() -> None:
    op.drop_table("webhook_deliveries")
