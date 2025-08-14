from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
import uuid

from app.database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(ForeignKey("users.id"), nullable=False)
    original_name = Column(String, nullable=False)
    stored_name = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)
    size_bytes = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
