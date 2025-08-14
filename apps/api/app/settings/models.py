from sqlalchemy import Column, DateTime, String, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from ..database import Base


class AppSetting(Base):
    __tablename__ = "app_settings"

    id = Column(UUID(as_uuid=True), primary_key=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
