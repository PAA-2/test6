from typing import Dict
from uuid import uuid4

from sqlalchemy.orm import Session

from .models import FeatureFlag

_cache: Dict[str, bool] = {}


def get_flag(db: Session, key: str) -> bool:
    if key in _cache:
        return _cache[key]
    flag = db.query(FeatureFlag).filter(FeatureFlag.key == key).first()
    _cache[key] = flag.enabled if flag else False
    return _cache[key]


def set_flag(db: Session, key: str, enabled: bool) -> FeatureFlag:
    flag = db.query(FeatureFlag).filter(FeatureFlag.key == key).first()
    if flag:
        flag.enabled = enabled
    else:
        flag = FeatureFlag(id=uuid4(), key=key, enabled=enabled)
        db.add(flag)
    db.commit()
    _cache[key] = enabled
    return flag
