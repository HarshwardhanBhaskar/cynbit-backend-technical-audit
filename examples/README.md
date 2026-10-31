# Reference API Examples

> **These are recommended patterns and reference implementations — NOT claims about Cynbit's actual backend.**

## Overview

This directory contains production-oriented FastAPI examples demonstrating backend security best practices relevant to the audit findings.

## Structure

```
examples/
├── main.py                     ← Full API assembly
├── requirements.txt            ← Python dependencies
│
├── authentication/
│   └── auth.py                 ← Password hashing + JWT + RBAC
│
├── validation/
│   └── models.py               ← Pydantic input validation
│
├── rate-limiting/
│   └── limiter.py              ← In-memory + Redis rate limiting
│
└── security/
    └── security_utils.py       ← Headers, CORS, logging, error handling
```

## Quick Start

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/macOS

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables (optional — defaults provided for demo)
set JWT_SECRET_KEY=your-strong-secret-key-here
set ENVIRONMENT=development

# 4. Run the server
uvicorn main:app --reload --port 8000

# 5. Open API docs
# Navigate to http://localhost:8000/docs
```

## Available Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/health` | No | Health check |
| POST | `/api/contact` | No | Contact form (rate limited) |
| POST | `/api/auth/login` | No | JWT login (rate limited) |
| GET | `/api/profile` | JWT | User profile (protected) |
| GET | `/api/admin/dashboard` | JWT + Admin | Admin dashboard (RBAC) |

## Demo Credentials

| Email | Password | Role |
|---|---|---|
| `admin@example.com` | `AdminP@ss2026!` | admin |
| `user@example.com` | `UserP@ss2026!` | user |

## What Each Module Demonstrates

### `authentication/auth.py`
- bcrypt password hashing with configurable cost factor
- JWT access + refresh token generation
- Token decode and validation
- FastAPI dependency injection for protected routes
- Role-based access control (RBAC) factory

### `validation/models.py`
- Pydantic v2 models with field validators
- Email format validation
- Input sanitization (HTML stripping)
- Structured error responses
- Enum-based field validation

### `rate-limiting/limiter.py`
- In-memory sliding window rate limiter
- Redis-backed approach (conceptual)
- Per-endpoint rate limit configuration
- Rate limit response headers (X-RateLimit-*)

### `security/security_utils.py`
- HTTP security headers middleware
- Centralized exception handling (AppError hierarchy)
- Structured JSON logging (never logs secrets)
- Request ID correlation
- CORS configuration
- Safe database query patterns
