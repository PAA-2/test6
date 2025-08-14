from __future__ import annotations

import secrets
import hashlib
from typing import List
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.api_key import ApiKey


def _hash_key(salt: str, key: str) -> str:
    return hashlib.sha256((salt + key).encode()).hexdigest()


def create_api_key(
    db: Session, org_id: str, name: str, scopes: List[str]
) -> tuple[ApiKey, str]:
    prefix = secrets.token_hex(4)
    secret = secrets.token_urlsafe(18)
    key_plain = f"paa_live_{prefix}_{secret}"
    salt = secrets.token_hex(8)
    hashed = _hash_key(salt, key_plain)
    api_key = ApiKey(
        org_id=org_id,
        name=name,
        prefix=prefix,
        hashed_key=hashed,
        salt=salt,
        scopes=scopes,
    )
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    return api_key, key_plain


def list_api_keys(db: Session, org_id: str) -> List[ApiKey]:
    return db.query(ApiKey).filter(ApiKey.org_id == org_id).all()


def get_api_key_by_prefix(db: Session, prefix: str) -> ApiKey | None:
    return db.query(ApiKey).filter(ApiKey.prefix == prefix).first()


def verify_api_key(db: Session, key: str) -> ApiKey | None:
    try:
        prefix = key.split("_")[2]
    except IndexError:
        return None
    api_key = get_api_key_by_prefix(db, prefix)
    if not api_key or not api_key.active:
        return None
    hashed = _hash_key(api_key.salt, key)
    if hashed != api_key.hashed_key:
        return None
    api_key.last_used_at = datetime.utcnow()
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    return api_key


def revoke_api_key(db: Session, api_key: ApiKey) -> None:
    api_key.active = False
    api_key.revoked_at = datetime.utcnow()
    db.add(api_key)
    db.commit()
