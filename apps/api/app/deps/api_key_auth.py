from __future__ import annotations

from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.api_keys import verify_api_key
from app.services.rate_limit import check_rate_limit
from app.models.api_key import ApiKey


class ApiKeyContext:
    def __init__(self, key: ApiKey, limit: int, remaining: int, reset: int):
        self.key = key
        self.limit = limit
        self.remaining = remaining
        self.reset = reset


def api_key_auth(
    db: Session = Depends(get_db),
    x_api_key: str | None = Header(None),
    authorization: str | None = Header(None),
) -> ApiKeyContext:
    key = None
    if x_api_key:
        key = x_api_key
    elif authorization and authorization.startswith("Bearer "):
        key = authorization.split(" ", 1)[1]
    if not key:
        raise HTTPException(status_code=401, detail="API key required")
    api_key = verify_api_key(db, key)
    if not api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    limit, remaining, reset = check_rate_limit(api_key.prefix)
    return ApiKeyContext(api_key, limit, remaining, reset)
