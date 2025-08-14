import json
import logging
import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("paa")


def configure_logging() -> None:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        request_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
        request.state.request_id = request_id
        response = await call_next(request)
        duration = (time.time() - start) * 1000
        record = {
            "ts": time.time(),
            "level": "info",
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "duration_ms": round(duration, 2),
            "user_id": getattr(request.state, "user_id", None),
            "org_id": getattr(request.state, "org_id", None),
        }
        logger.info(json.dumps(record))
        return response
