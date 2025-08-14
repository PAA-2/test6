from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.user import User
from .models import AppSetting

router = APIRouter(prefix="/app-settings", tags=["app-settings"])


class SettingUpdate(BaseModel):
    value: dict


@router.get("/")
async def list_settings(db: Session = Depends(get_db)):
    settings = db.query(AppSetting).all()
    return [{"key": s.key, "value": s.value} for s in settings]


@router.patch("/{key}")
async def update_setting(
    key: str,
    data: SettingUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="forbidden")
    setting = db.query(AppSetting).filter(AppSetting.key == key).first()
    if setting:
        setting.value = data.value
    else:
        setting = AppSetting(id=uuid4(), key=key, value=data.value)
        db.add(setting)
    db.commit()
    return {"key": setting.key, "value": setting.value}
