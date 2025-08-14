from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, JSON, func
import uuid

from app.database import Base


class WebhookEndpoint(Base):
    __tablename__ = "webhook_endpoints"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    org_id = Column(ForeignKey("organizations.id"), nullable=False)
    url = Column(String, nullable=False)
    secret = Column(String, nullable=False)
    events = Column(JSON, nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
