from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, func
import uuid

from app.database import Base


class OrgMembership(Base):
    __tablename__ = "org_memberships"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    org_id = Column(ForeignKey("organizations.id"), nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    role = Column(
        Enum("owner", "admin", "member", "viewer", name="org_role"),
        nullable=False,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
