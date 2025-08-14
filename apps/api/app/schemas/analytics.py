from pydantic import BaseModel
from typing import Dict, List


class FileMimeStat(BaseModel):
    mime: str
    count: int


class AnalyticsSummary(BaseModel):
    projects_total: int
    projects_by_status: Dict[str, int]
    files_total: int
    files_bytes_total: int
    files_top_mime: List[FileMimeStat]
    notifications_unread: int


class ProjectPerDay(BaseModel):
    date: str
    count: int


class TopUser(BaseModel):
    user_id: int
    email: str
    projects_count: int
