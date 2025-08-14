from sqlalchemy import Column, DateTime, Enum, Integer, String, func, ForeignKey
from sqlalchemy import Boolean

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(
        Enum("admin", "editor", "viewer", name="user_role"),
        nullable=False,
        server_default="viewer",
    )
    email_notifications = Column(Boolean, server_default="1", nullable=False)
    last_selected_org_id = Column(ForeignKey("organizations.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
