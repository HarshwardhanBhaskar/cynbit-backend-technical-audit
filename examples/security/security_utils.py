"""
Security Utilities & Centralized Exception Handling
====================================================
Reference implementation demonstrating:
- HTTP security headers middleware
- Centralized exception handling
- Structured logging
- Safe database query patterns
- CORS configuration

This is a RECOMMENDATION — not a claim about Cynbit's implementation.
"""

import logging
import os
import sys
import traceback
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel


# ============================================================
# 1. STRUCTURED LOGGING
# ============================================================

class StructuredLogger:
    """
    JSON-based structured logger.

    Outputs machine-parseable log lines for easy aggregation
    and search in logging platforms (ELK, CloudWatch, etc.).
    """

    def __init__(self, service_name: str = "cynbit-api"):
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)
        self.logger.setLevel(logging.INFO)

        # JSON formatter
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(handler)

    def _format(
        self,
        level: str,
        message: str,
        **kwargs: Any,
    ) -> dict:
        """Create a structured log entry."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": level,
            "service": self.service_name,
            "message": message,
        }
        # Add extra fields but NEVER log sensitive data
        safe_kwargs = {
            k: v for k, v in kwargs.items()
            if k not in ("password", "token", "secret", "authorization", "cookie")
        }
        entry.update(safe_kwargs)
        return entry

    def info(self, message: str, **kwargs: Any) -> None:
        import json
        self.logger.info(json.dumps(self._format("INFO", message, **kwargs)))

    def warning(self, message: str, **kwargs: Any) -> None:
        import json
        self.logger.warning(json.dumps(self._format("WARNING", message, **kwargs)))

    def error(self, message: str, **kwargs: Any) -> None:
        import json
        self.logger.error(json.dumps(self._format("ERROR", message, **kwargs)))


logger = StructuredLogger()


# ============================================================
# 2. CENTRALIZED EXCEPTION HANDLING
# ============================================================

class AppError(Exception):
    """Base application error with structured response."""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: list[dict] | None = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or []
        super().__init__(message)


class ValidationError(AppError):
    def __init__(self, message: str, details: list[dict] | None = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=422,
            details=details,
        )


class AuthenticationError(AppError):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(
            message=message,
            code="AUTHENTICATION_ERROR",
            status_code=401,
        )


class AuthorizationError(AppError):
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            message=message,
            code="AUTHORIZATION_ERROR",
            status_code=403,
        )


class NotFoundError(AppError):
    def __init__(self, resource: str, identifier: str):
        super().__init__(
            message=f"{resource} not found: {identifier}",
            code="NOT_FOUND",
            status_code=404,
        )


class RateLimitError(AppError):
    def __init__(self, retry_after: int = 60):
        super().__init__(
            message="Rate limit exceeded",
            code="RATE_LIMIT_EXCEEDED",
            status_code=429,
            details=[{"retry_after": retry_after}],
        )


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register centralized exception handlers on the FastAPI app.

    This ensures ALL exceptions return consistent, safe JSON responses.
    """

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "unknown")

        logger.warning(
            f"Application error: {exc.code}",
            request_id=request_id,
            error_code=exc.code,
            path=str(request.url.path),
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": exc.details,
                    "request_id": request_id,
                },
            },
        )

    @app.exception_handler(HTTPException)
    async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "unknown")

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": f"HTTP_{exc.status_code}",
                    "message": exc.detail,
                    "request_id": request_id,
                },
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """
        Catch-all handler — NEVER expose stack traces to the client.
        Log the full error server-side for debugging.
        """
        request_id = getattr(request.state, "request_id", "unknown")

        # Log full details server-side
        logger.error(
            "Unhandled exception",
            request_id=request_id,
            path=str(request.url.path),
            error_type=type(exc).__name__,
            error_message=str(exc),
            traceback=traceback.format_exc(),
        )

        # Return safe response to client — no internals leaked
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred. Please try again later.",
                    "request_id": request_id,
                },
            },
        )


# ============================================================
# 3. SECURITY HEADERS MIDDLEWARE
# ============================================================

async def security_headers_middleware(request: Request, call_next):
    """
    Add security headers to every response.
    """
    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://www.googletagmanager.com; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "connect-src 'self' https://www.google-analytics.com"
    )

    return response


# ============================================================
# 4. REQUEST ID MIDDLEWARE
# ============================================================

async def request_id_middleware(request: Request, call_next):
    """Attach a unique request ID for tracing."""
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request.state.request_id = request_id

    logger.info(
        "Request started",
        request_id=request_id,
        method=request.method,
        path=str(request.url.path),
    )

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id

    logger.info(
        "Request completed",
        request_id=request_id,
        status_code=response.status_code,
    )

    return response


# ============================================================
# 5. SAFE DATABASE QUERIES
# ============================================================

class SafeQueryExample:
    """
    Demonstrates parameterized queries to prevent SQL injection.

    NEVER use string formatting/concatenation in SQL queries.
    """

    @staticmethod
    def safe_query_example():
        """
        Example using parameterized queries.

        SAFE — parameters are bound separately from the query:
            cursor.execute(
                "SELECT * FROM users WHERE email = %s AND active = %s",
                (email, True)
            )

        UNSAFE — string formatting allows injection:
            cursor.execute(
                f"SELECT * FROM users WHERE email = '{email}'"  # NEVER DO THIS
            )
        """
        pass

    @staticmethod
    def sqlalchemy_example():
        """
        Example using SQLAlchemy ORM (parameterized by default).

        from sqlalchemy import select
        from models import User

        # ORM query — automatically parameterized
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        """
        pass

    @staticmethod
    def async_example():
        """
        Example using asyncpg (async PostgreSQL driver).

        # asyncpg uses $1, $2, etc. for parameters
        row = await conn.fetchrow(
            "SELECT id, email, role FROM users WHERE email = $1",
            email
        )
        """
        pass


# ============================================================
# 6. CORS CONFIGURATION
# ============================================================

def configure_cors(app: FastAPI) -> None:
    """
    Configure CORS with least-privilege approach.

    Only allow specific origins — never use wildcard '*' in production
    with credentials.
    """
    allowed_origins = os.getenv(
        "CORS_ORIGINS",
        "https://cynbit.in,https://www.cynbit.in"
    ).split(",")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
        expose_headers=["X-Request-ID", "X-RateLimit-Remaining"],
        max_age=600,  # Cache preflight for 10 minutes
    )


# ============================================================
# 7. FULL APP ASSEMBLY
# ============================================================

def create_app() -> FastAPI:
    """
    Factory function demonstrating how all security components
    come together in a production FastAPI application.
    """
    app = FastAPI(
        title="Secure API Example",
        description="Reference implementation for backend security patterns",
        version="1.0.0",
        docs_url="/docs" if os.getenv("ENVIRONMENT") != "production" else None,
        redoc_url=None,
    )

    # 1. CORS
    configure_cors(app)

    # 2. Middleware (order matters — outermost first)
    app.middleware("http")(request_id_middleware)
    app.middleware("http")(security_headers_middleware)

    # 3. Exception handlers
    register_exception_handlers(app)

    # 4. Health check
    @app.get("/health")
    async def health():
        return {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    return app


if __name__ == "__main__":
    print("Security utilities module loaded.")
    print("Components available:")
    print("  - StructuredLogger")
    print("  - Centralized exception handlers (AppError hierarchy)")
    print("  - Security headers middleware")
    print("  - Request ID middleware")
    print("  - CORS configuration")
    print("  - Safe query patterns")
    print("\nSee create_app() for full assembly example.")
