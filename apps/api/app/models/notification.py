from sqlalchemy import Column, DateTime, ForeignKey, Boolean, String, JSON, func
import uuid

from app.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(ForeignKey("users.id"), nullable=False)
    type = Column(String, nullable=False)
    message = Column(String, nullable=False)
    data = Column(JSON, nullable=True)
    read = Column(Boolean, nullable=False, server_default="0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
