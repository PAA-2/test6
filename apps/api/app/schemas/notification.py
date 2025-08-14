from pydantic import BaseModel
from typing import Any, Dict
from datetime import datetime


class NotificationRead(BaseModel):
    id: str
    type: str
    message: str
    data: Dict[str, Any] | None = None
    read: bool
    created_at: datetime

    class Config:
        orm_mode = True
