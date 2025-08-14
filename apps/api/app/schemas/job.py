from __future__ import annotations

from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class JobStatus(BaseModel):
    id: str
    type: str = Field(..., alias="type")
    status: str
    started_at: datetime | None = None
    finished_at: datetime | None = None
    error_text: str | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class JobList(BaseModel):
    items: List[JobStatus]
    page: int
    page_size: int
    total: int


class JobEnqueueResponse(BaseModel):
    task_id: str
