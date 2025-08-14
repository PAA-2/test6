import hashlib
from datetime import datetime
from typing import Optional

from fastapi import Request
from starlette.responses import Response


def compute_etag(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()  # noqa: S324


def check_not_modified(
    request: Request, *, etag: str, last_modified: Optional[datetime]
) -> Optional[Response]:
    if request.headers.get("if-none-match") == etag:
        return Response(status_code=304)
    if last_modified:
        if_modified_since = request.headers.get("if-modified-since")
        if if_modified_since and if_modified_since == last_modified.strftime(
            "%a, %d %b %Y %H:%M:%S GMT"
        ):
            return Response(status_code=304)
    return None


def apply_cache_headers(
    response: Response, *, etag: str, last_modified: Optional[datetime] = None
) -> None:
    response.headers["ETag"] = etag
    if last_modified:
        response.headers["Last-Modified"] = last_modified.strftime(
            "%a, %d %b %Y %H:%M:%S GMT"
        )
