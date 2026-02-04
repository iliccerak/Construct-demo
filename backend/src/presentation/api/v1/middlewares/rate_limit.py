import time
from collections import defaultdict, deque
from typing import Deque, DefaultDict

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from infrastructure.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self._requests: DefaultDict[str, Deque[float]] = defaultdict(deque)

    def _limit_for_path(self, path: str) -> int:
        if path.startswith("/api/v1/auth"):
            return settings.auth_rate_limit_max_requests
        return settings.rate_limit_max_requests

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        limit = self._limit_for_path(request.url.path)
        now = time.time()
        window = settings.rate_limit_window_seconds

        queue = self._requests[client_ip]
        while queue and queue[0] <= now - window:
            queue.popleft()

        if len(queue) >= limit:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"},
            )

        queue.append(now)
        return await call_next(request)
