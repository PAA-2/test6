from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.user import User
from .models import FeatureFlag
from .services import set_flag

router = APIRouter(prefix="/feature-flags", tags=["feature-flags"])


class FlagUpdate(BaseModel):
    enabled: bool


@router.get("/")
async def list_flags(db: Session = Depends(get_db)):
    flags = db.query(FeatureFlag).all()
    return [{"key": f.key, "enabled": f.enabled} for f in flags]


@router.patch("/{key}")
async def update_flag(
    key: str,
    data: FlagUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="forbidden")
    flag = set_flag(db, key, data.enabled)
    return {"key": flag.key, "enabled": flag.enabled}
