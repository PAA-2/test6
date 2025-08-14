from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from ...database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True)
    actor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    org_id = Column(UUID(as_uuid=True), nullable=True)
    action = Column(String, nullable=False)
    target_type = Column(String, nullable=True)
    target_id = Column(UUID(as_uuid=True), nullable=True)
    ip = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    success = Column(Boolean, default=True)
    details = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
