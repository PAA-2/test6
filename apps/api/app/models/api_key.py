from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, JSON, func
import uuid

from app.database import Base


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    org_id = Column(ForeignKey("organizations.id"), nullable=False)
    name = Column(String, nullable=False)
    prefix = Column(String, unique=True, index=True, nullable=False)
    hashed_key = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    scopes = Column(JSON, nullable=False, default=list)
    active = Column(Boolean, default=True)
    last_used_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    revoked_at = Column(DateTime(timezone=True), nullable=True)
