from __future__ import annotations

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, ForeignKey

from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(String, nullable=False)
    args = Column(JSON, nullable=True)
    status = Column(String, nullable=False, default="queued")
    owner_id = Column(ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    error_text = Column(String, nullable=True)
