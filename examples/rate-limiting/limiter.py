"""
Rate Limiting Example
=====================
Reference implementation demonstrating API rate limiting
using slowapi (built on top of limits library).

This is a RECOMMENDATION — not a claim about Cynbit's implementation.
"""

import os
import time
from collections import defaultdict
from typing import Callable

from fastapi import FastAPI, HTTPException, Request, Response, status


# === Approach 1: Simple in-memory rate limiter (for demonstration) ===

class InMemoryRateLimiter:
    """
    Simple in-memory rate limiter using a sliding window approach.

    For production, use Redis-backed rate limiting (see Approach 2).
    This implementation is suitable for single-instance deployments only.
    """

    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, list[float]] = defaultdict(list)

    def _get_client_id(self, request: Request) -> str:
        """Extract client identifier from request."""
        # Use X-Forwarded-For if behind a proxy, otherwise use client host
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

    def _cleanup(self, client_id: str) -> None:
        """Remove expired timestamps from the window."""
        cutoff = time.time() - self.window_seconds
        self.requests[client_id] = [
            ts for ts in self.requests[client_id] if ts > cutoff
        ]

    def check(self, request: Request) -> dict:
        """
        Check if a request is within rate limits.

        Returns:
            dict with rate limit info (remaining, reset_at)

        Raises:
            HTTPException 429 if rate limit exceeded
        """
        client_id = self._get_client_id(request)
        self._cleanup(client_id)

        current_count = len(self.requests[client_id])

        if current_count >= self.max_requests:
            reset_at = int(self.requests[client_id][0] + self.window_seconds)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Rate limit exceeded",
                    "message": f"Maximum {self.max_requests} requests per {self.window_seconds} seconds",
                    "retry_after": reset_at - int(time.time()),
                },
                headers={
                    "Retry-After": str(reset_at - int(time.time())),
                    "X-RateLimit-Limit": str(self.max_requests),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(reset_at),
                },
            )

        self.requests[client_id].append(time.time())

        return {
            "limit": self.max_requests,
            "remaining": self.max_requests - current_count - 1,
            "window": self.window_seconds,
        }


# === Approach 2: Redis-backed rate limiter (production-ready) ===

class RedisRateLimiter:
    """
    Redis-backed rate limiter using sliding window.

    Requires: redis-py (pip install redis)

    This approach supports distributed deployments where
    multiple app instances share rate limit state.
    """

    def __init__(
        self,
        redis_url: str = None,
        max_requests: int = 10,
        window_seconds: int = 60,
        key_prefix: str = "ratelimit",
    ):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.key_prefix = key_prefix
        self.redis_url = redis_url or os.getenv("REDIS_URL", "redis://localhost:6379")

        # Note: In production, initialize the Redis client at app startup
        # import redis.asyncio as redis
        # self.redis = redis.from_url(self.redis_url)

    def _get_key(self, client_id: str, endpoint: str) -> str:
        """Generate a rate limit key combining client and endpoint."""
        return f"{self.key_prefix}:{endpoint}:{client_id}"

    # async def check(self, request: Request) -> dict:
    #     """
    #     Production implementation would use Redis MULTI/EXEC:
    #
    #     key = self._get_key(client_id, request.url.path)
    #     pipe = self.redis.pipeline()
    #     now = time.time()
    #     pipe.zremrangebyscore(key, 0, now - self.window_seconds)
    #     pipe.zadd(key, {str(now): now})
    #     pipe.zcard(key)
    #     pipe.expire(key, self.window_seconds)
    #     results = await pipe.execute()
    #     request_count = results[2]
    #     ...
    #     """
    #     pass


# === FastAPI middleware for rate limiting ===

def create_rate_limit_middleware(limiter: InMemoryRateLimiter) -> Callable:
    """
    Create a FastAPI middleware that applies rate limiting.

    Usage:
        limiter = InMemoryRateLimiter(max_requests=30, window_seconds=60)
        app.middleware("http")(create_rate_limit_middleware(limiter))
    """
    async def rate_limit_middleware(request: Request, call_next) -> Response:
        # Skip rate limiting for health checks
        if request.url.path in ("/health", "/health/ready"):
            return await call_next(request)

        rate_info = limiter.check(request)

        response = await call_next(request)

        # Add rate limit headers to all responses
        response.headers["X-RateLimit-Limit"] = str(rate_info["limit"])
        response.headers["X-RateLimit-Remaining"] = str(rate_info["remaining"])

        return response

    return rate_limit_middleware


# === Per-endpoint rate limiting ===

# Different endpoints may need different rate limits
contact_limiter = InMemoryRateLimiter(max_requests=5, window_seconds=300)  # 5 per 5 min
api_limiter = InMemoryRateLimiter(max_requests=60, window_seconds=60)  # 60 per min
auth_limiter = InMemoryRateLimiter(max_requests=5, window_seconds=900)  # 5 per 15 min


# === Example FastAPI app ===

if __name__ == "__main__":
    app = FastAPI(title="Rate Limiting Demo")

    global_limiter = InMemoryRateLimiter(max_requests=30, window_seconds=60)

    @app.middleware("http")
    async def rate_limit(request: Request, call_next):
        middleware = create_rate_limit_middleware(global_limiter)
        return await middleware(request, call_next)

    @app.post("/api/contact")
    async def submit_contact(request: Request):
        # Additional per-endpoint rate limit
        contact_limiter.check(request)
        return {"message": "Contact form submitted"}

    @app.post("/api/auth/login")
    async def login(request: Request):
        # Stricter rate limit for auth endpoints
        auth_limiter.check(request)
        return {"message": "Login endpoint"}

    print("Rate limiting example configured.")
    print("- Global: 30 req/min")
    print("- Contact form: 5 req/5min")
    print("- Auth: 5 req/15min")
