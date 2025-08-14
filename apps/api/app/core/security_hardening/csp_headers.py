from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from ..config import settings


class CSPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers.setdefault("Content-Security-Policy", settings.CSP_DEFAULT_SRC)
        return response
