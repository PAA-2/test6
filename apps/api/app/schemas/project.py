from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    description: Optional[str] = Field(None, max_length=5000)
    status: str = Field(..., pattern="^(draft|active|archived)$")


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=80)
    description: Optional[str] = Field(None, max_length=5000)
    status: Optional[str] = Field(None, pattern="^(draft|active|archived)$")


class ProjectRead(ProjectBase):
    id: str
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectAuditRead(BaseModel):
    id: int
    project_id: str
    action: str
    actor_id: int
    at: datetime
    diff: Optional[dict]

    class Config:
        from_attributes = True
