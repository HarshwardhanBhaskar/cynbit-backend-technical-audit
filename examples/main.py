"""
Main FastAPI Application
========================
Assembles all example modules into a runnable reference application.

This is a RECOMMENDATION and reference implementation —
not a claim about Cynbit's actual backend.

Run with:
    uvicorn main:app --reload --port 8000
"""

import os
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request

# Local imports
from authentication.auth import (
    LoginRequest,
    TokenResponse,
    create_access_token,
    create_refresh_token,
    get_current_user,
    hash_password,
    require_role,
    verify_password,
    TokenPayload,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from rate_limiting.limiter import InMemoryRateLimiter, create_rate_limit_middleware
from security.security_utils import (
    configure_cors,
    register_exception_handlers,
    request_id_middleware,
    security_headers_middleware,
    logger,
    NotFoundError,
)
from validation.models import ContactFormRequest, ContactFormResponse


# --- Simulated user store (replace with real DB in production) ---

DEMO_USERS = {
    "admin@example.com": {
        "password_hash": hash_password("AdminP@ss2026!"),
        "role": "admin",
        "name": "Admin User",
    },
    "user@example.com": {
        "password_hash": hash_password("UserP@ss2026!"),
        "role": "user",
        "name": "Regular User",
    },
}


# --- App lifecycle ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up", environment=os.getenv("ENVIRONMENT", "dev"))
    yield
    logger.info("Application shutting down")


# --- Create app ---

app = FastAPI(
    title="Cynbit Backend Audit — Reference API",
    description=(
        "Reference FastAPI implementation demonstrating backend security patterns. "
        "This is NOT Cynbit's actual backend."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Middleware
configure_cors(app)
app.middleware("http")(request_id_middleware)
app.middleware("http")(security_headers_middleware)

# Rate limiters
global_limiter = InMemoryRateLimiter(max_requests=60, window_seconds=60)
contact_limiter = InMemoryRateLimiter(max_requests=5, window_seconds=300)
auth_limiter = InMemoryRateLimiter(max_requests=5, window_seconds=900)

app.middleware("http")(create_rate_limit_middleware(global_limiter))

# Exception handlers
register_exception_handlers(app)


# ============================================================
# ROUTES
# ============================================================

@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {"status": "healthy", "service": "cynbit-audit-reference-api"}


@app.post("/api/contact", response_model=ContactFormResponse, status_code=201)
async def submit_contact(
    request: Request,
    form: ContactFormRequest,
):
    """
    Contact form submission endpoint.

    Demonstrates:
    - Pydantic input validation
    - Per-endpoint rate limiting
    - Structured response
    """
    # Additional rate limit for contact endpoint
    contact_limiter.check(request)

    logger.info(
        "Contact form submitted",
        email_domain=form.email.split("@")[1],  # Log domain only, not full email
        has_company=form.company is not None,
        has_industry=form.industry is not None,
    )

    # In production: save to database, send notification email
    return ContactFormResponse(
        data={
            "inquiry_id": "inq_demo_123",
            "message": "Your inquiry has been submitted successfully.",
            "estimated_response": "24 hours",
        }
    )


@app.post("/api/auth/login", response_model=TokenResponse)
async def login(request: Request, credentials: LoginRequest):
    """
    Login endpoint demonstrating JWT authentication.

    Demonstrates:
    - Rate limiting on auth endpoints
    - Password verification with bcrypt
    - JWT token generation
    """
    auth_limiter.check(request)

    user = DEMO_USERS.get(credentials.email)
    if not user or not verify_password(credentials.password, user["password_hash"]):
        # Intentionally vague error — don't reveal which field is wrong
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        subject=credentials.email,
        role=user["role"],
    )
    refresh_token = create_refresh_token(subject=credentials.email)

    logger.info("User logged in", role=user["role"])

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@app.get("/api/profile")
async def get_profile(user: TokenPayload = Depends(get_current_user)):
    """
    Protected endpoint — requires valid JWT.

    Demonstrates:
    - JWT validation dependency
    - Role-based response
    """
    demo_user = DEMO_USERS.get(user.sub)
    if not demo_user:
        raise NotFoundError("User", user.sub)

    return {
        "success": True,
        "data": {
            "email": user.sub,
            "name": demo_user["name"],
            "role": user.role,
        },
    }


@app.get(
    "/api/admin/dashboard",
    dependencies=[Depends(require_role("admin"))],
)
async def admin_dashboard():
    """
    Admin-only endpoint — requires admin role.

    Demonstrates:
    - Role-based access control (RBAC)
    """
    return {
        "success": True,
        "data": {
            "message": "Welcome to the admin dashboard",
            "total_inquiries": 42,
            "pending_responses": 3,
        },
    }


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
