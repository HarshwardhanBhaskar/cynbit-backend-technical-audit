# Backend Reference Implementation

> **Notice:** This is an engineering reference implementation demonstrating backend architecture, security controls, and data integrity practices proposed for Cynbit Technologies. It is **not** Cynbit's proprietary codebase.

---

## 1. Stack Overview

- **Language:** Python 3.12+
- **Web Framework:** FastAPI (Async ASGI)
- **Data Validation:** Pydantic v2
- **ORM & Database:** SQLAlchemy 2.0 (Async Engine), PostgreSQL (Development/Production), aiosqlite (Hermetic Unit Testing)
- **Security:** bcrypt password hashing, Python-JOSE JWT Bearer authentication, Security Headers Middleware, Sliding Window Rate Limiting
- **Containerization:** Docker & Docker Compose

---

## 2. Directory Layout

```
backend-reference/
├── app/
│   ├── main.py                    # ASGI Application factory & lifespan
│   ├── config.py                  # Pydantic Settings configuration
│   ├── database.py                # Async session management
│   ├── models/                    # SQLAlchemy ORM entities
│   │   ├── applicant.py
│   │   ├── qualification.py
│   │   ├── application.py
│   │   ├── contact.py
│   │   └── audit.py
│   ├── schemas/                   # Pydantic request/response DTOs
│   │   ├── applicant.py
│   │   ├── application.py
│   │   ├── contact.py
│   │   └── auth.py
│   ├── services/                  # Business logic & transactions
│   │   ├── application_service.py
│   │   └── contact_service.py
│   ├── middleware/                # Defense-in-depth pipeline
│   │   ├── security_headers.py
│   │   ├── rate_limiter.py
│   │   ├── exception_handlers.py
│   │   └── logging_middleware.py
│   └── routers/                   # API routes
│       ├── health.py
│       ├── applications.py
│       ├── contacts.py
│       └── auth.py
├── tests/                         # Automated test suite (pytest)
├── Dockerfile                     # Multi-stage secure container build
├── docker-compose.yml             # Local cluster (App + Postgres + Redis)
└── requirements.txt
```

---

## 3. Running Locally

### 3.1 Prerequisites
- Python 3.12+ (or Docker Engine)
- Virtual environment tool (`venv`)

### 3.2 Setup & Execution (Virtual Environment)

```bash
# 1. Navigate to backend reference directory
cd backend-reference

# 2. Create and activate a virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the development server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3.3 Running via Docker Compose

```bash
docker compose up --build -d
```
Access the interactive OpenAPI documentation at: `http://localhost:8000/docs`

---

## 4. Running Automated Tests

The test suite runs against an isolated in-memory asynchronous SQLite database (`sqlite+aiosqlite:///:memory:`):

```bash
# Run all tests with pytest
pytest -v
```
All test cases execute hermetically with zero external database dependencies.
