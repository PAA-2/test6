from sqlalchemy import Boolean, Column, DateTime, String, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from ..database import Base


class FeatureFlag(Base):
    __tablename__ = "feature_flags"

    id = Column(UUID(as_uuid=True), primary_key=True)
    key = Column(String, unique=True, nullable=False)
    enabled = Column(Boolean, default=False)
    audience = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
