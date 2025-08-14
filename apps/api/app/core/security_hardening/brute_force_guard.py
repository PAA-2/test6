from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Tuple

import redis

from ..config import settings


@dataclass
class BruteForceGuard:
    redis: redis.Redis
    limit: int = settings.LOGIN_BRUTE_LIMIT_PER_MIN
    ban_minutes: int = settings.LOGIN_BRUTE_BAN_MINUTES

    def _keys(self, ip: str, email: str) -> Tuple[str, str]:
        base = f"login:{ip}:{email}"
        return base, f"{base}:banned"

    def allow(self, ip: str, email: str) -> bool:
        attempts_key, ban_key = self._keys(ip, email)
        if self.redis.get(ban_key):
            return False
        attempts = self.redis.incr(attempts_key)
        if attempts == 1:
            self.redis.expire(attempts_key, 60)
        if attempts > self.limit:
            self.redis.setex(ban_key, timedelta(minutes=self.ban_minutes), 1)
            return False
        return True
