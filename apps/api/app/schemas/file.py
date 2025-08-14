from datetime import datetime
from pydantic import BaseModel


class FileRead(BaseModel):
    id: str
    owner_id: int
    original_name: str
    mime_type: str
    size_bytes: int
    created_at: datetime

    class Config:
        orm_mode = True
