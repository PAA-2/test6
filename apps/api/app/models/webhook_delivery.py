from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Integer, func
import uuid
from sqlalchemy.orm import relationship

from app.database import Base


class WebhookDelivery(Base):
    __tablename__ = "webhook_deliveries"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    endpoint_id = Column(ForeignKey("webhook_endpoints.id"), nullable=False)
    event = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    status = Column(String, default="pending")
    response_code = Column(Integer, nullable=True)
    attempts = Column(Integer, default=0)
    next_retry_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    endpoint = relationship("WebhookEndpoint")
