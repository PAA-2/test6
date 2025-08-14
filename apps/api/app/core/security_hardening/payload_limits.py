from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class PayloadLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_body: int):
        super().__init__(app)
        self.max_body = max_body

    async def dispatch(self, request, call_next):
        length = request.headers.get("content-length")
        if length and int(length) > self.max_body:
            return Response(status_code=413)
        return await call_next(request)
