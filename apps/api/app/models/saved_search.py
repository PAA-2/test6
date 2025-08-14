from sqlalchemy import Column, DateTime, ForeignKey, String, JSON, func
import uuid

from app.database import Base


class SavedSearch(Base):
    __tablename__ = "saved_searches"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    params = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
