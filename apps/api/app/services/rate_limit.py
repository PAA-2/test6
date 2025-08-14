from __future__ import annotations

import time
from typing import Tuple
from fastapi import HTTPException

from app.jobs.queue import redis_conn
from app.core.config import settings


def check_rate_limit(prefix: str) -> Tuple[int, int, int]:
    limit = getattr(settings, "API_RATE_LIMIT_PER_MINUTE", 60)
    window = int(time.time() // 60)
    key = f"ratelimit:{prefix}:{window}"
    count = redis_conn.incr(key)
    if count == 1:
        redis_conn.expire(key, 60)
    remaining = limit - count
    reset = window * 60 + 60
    if remaining < 0:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    return limit, remaining, reset
