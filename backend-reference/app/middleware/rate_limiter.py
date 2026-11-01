"""
Rate Limiter Middleware & Dependency
====================================
Implements sliding-window rate limiting to safeguard sensitive endpoints
against abuse and denial-of-service attempts.
"""

import time
from collections import defaultdict
from typing import Dict, List
from fastapi import HTTPException, Request, status


class SlidingWindowRateLimiter:
    def __init__(self, limit: int = 60, window_seconds: int = 60):
        self.limit = limit
        self.window_seconds = window_seconds
        self.history: Dict[str, List[float]] = defaultdict(list)

    def _get_client_ip(self, request: Request) -> str:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "127.0.0.1"

    def check(self, request: Request) -> None:
        client_ip = self._get_client_ip(request)
        now = time.time()
        cutoff = now - self.window_seconds

        # Clean timestamps older than window
        self.history[client_ip] = [ts for ts in self.history[client_ip] if ts > cutoff]

        if len(self.history[client_ip]) >= self.limit:
            retry_after = int(self.history[client_ip][0] + self.window_seconds - now)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Maximum {self.limit} requests per {self.window_seconds}s.",
                headers={"Retry-After": str(max(1, retry_after))},
            )

        self.history[client_ip].append(now)


# Pre-configured instances
global_rate_limiter = SlidingWindowRateLimiter(limit=60, window_seconds=60)
application_rate_limiter = SlidingWindowRateLimiter(limit=5, window_seconds=3600)
contact_rate_limiter = SlidingWindowRateLimiter(limit=5, window_seconds=3600)
auth_rate_limiter = SlidingWindowRateLimiter(limit=5, window_seconds=900)
