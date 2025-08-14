from datetime import datetime
from typing import Literal, List, Optional, Dict

from pydantic import BaseModel, Field, validator


class SearchQuery(BaseModel):
    q: Optional[str] = None
    type: Literal["project", "file", "all"] = "all"
    status: Optional[List[str]] = None
    mime: Optional[List[str]] = None
    owner: Literal["me", "all"] = "all"
    created_from: Optional[datetime] = Field(None, alias="created_from")
    created_to: Optional[datetime] = Field(None, alias="created_to")
    sort: Literal["score", "created_at", "name"] = "score"
    order: Literal["asc", "desc"] = "desc"
    page: int = 1
    page_size: int = 10

    @validator("page", "page_size")
    def positive(cls, v):
        if v < 1:
            raise ValueError("must be positive")
        return v


class SearchItem(BaseModel):
    entity: Literal["project", "file"]
    id: str
    score: float
    title: str
    snippet: str
    status: Optional[str] = None
    mime: Optional[str] = None
    owner_id: int
    created_at: datetime


class SearchResponse(BaseModel):
    items: List[SearchItem]
    page: int
    page_size: int
    total: int


class FacetsResponse(BaseModel):
    projects_by_status: Dict[str, int]
    files_by_mime: List[Dict[str, object]]


class SuggestionItem(BaseModel):
    entity: Literal["project", "file"]
    title: str


class SavedSearchCreate(BaseModel):
    name: str
    params: Dict[str, object]


class SavedSearchOut(SavedSearchCreate):
    id: str
    created_at: datetime


class SavedSearchList(BaseModel):
    items: List[SavedSearchOut]
    page: int
    page_size: int
    total: int
