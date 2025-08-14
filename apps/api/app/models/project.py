from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Integer,
    JSON,
    Text,
    func,
)
from sqlalchemy.orm import relationship
import uuid

from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(80), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(
        Enum("draft", "active", "archived", name="project_status"), nullable=False
    )
    owner_id = Column(ForeignKey("users.id"), nullable=False)
    org_id = Column(ForeignKey("organizations.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    owner = relationship("User")


class ProjectAudit(Base):
    __tablename__ = "project_audit"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(ForeignKey("projects.id"), nullable=False)
    action = Column(String, nullable=False)
    actor_id = Column(ForeignKey("users.id"), nullable=False)
    at = Column(DateTime(timezone=True), server_default=func.now())
    diff = Column(JSON, nullable=True)
