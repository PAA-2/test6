from sqlalchemy import Column, DateTime, Enum, ForeignKey, String
import uuid

from app.database import Base


class OrgInvite(Base):
    __tablename__ = "org_invites"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    org_id = Column(ForeignKey("organizations.id"), nullable=False)
    email = Column(String, nullable=False)
    role = Column(
        Enum("owner", "admin", "member", "viewer", name="org_invite_role"),
        nullable=False,
    )
    token = Column(
        String, unique=True, nullable=False, default=lambda: str(uuid.uuid4())
    )
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_by = Column(ForeignKey("users.id"), nullable=False)
    accepted_at = Column(DateTime(timezone=True), nullable=True)
