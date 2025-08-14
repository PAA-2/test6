from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from redis import Redis
from fastapi.responses import JSONResponse

from ...database import get_db
from ...core.config import settings
from ...services.cache_headers import (
    compute_etag,
    check_not_modified,
    apply_cache_headers,
)

router = APIRouter()


@router.get("/healthz")
async def healthz(request: Request, db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        Redis.from_url(settings.REDIS_URL).ping()
    except Exception:
        body = JSONResponse({"status": "error"})
    else:
        body = JSONResponse({"status": "ok"})
    etag = compute_etag(body.body)
    not_modified = check_not_modified(request, etag=etag, last_modified=None)
    if not_modified:
        return not_modified
    apply_cache_headers(body, etag=etag)
    return body
