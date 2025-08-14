import time
from typing import Callable

from fastapi import APIRouter, Request, Response
from prometheus_client import Counter, Histogram, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware

REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "path", "status"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Latency of HTTP requests in seconds",
    ["method", "path"],
)

router = APIRouter()


@router.get("/metrics")
async def metrics() -> Response:
    data = generate_latest()
    return Response(data, media_type="text/plain; version=0.0.4")


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        REQUEST_COUNT.labels(
            request.method, request.url.path, response.status_code
        ).inc()
        REQUEST_LATENCY.labels(request.method, request.url.path).observe(duration)
        return response
