# System Architecture & Flow Diagrams

> **Architecture Document:** Cynbit Backend Reference Architecture  
> **Visual Modeling:** Mermaid Specification  

---

## 1. End-to-End System Architecture

```mermaid
graph TB
    subgraph "Clients"
        A1[Web Browser / Applicant]
        A2[Admin / HR Reviewer]
    end

    subgraph "Perimeter & Edge Protection"
        B1[Cloudflare CDN & DDoS Protection]
        B2[Web Application Firewall - WAF]
        B3[TLS 1.3 Termination]
    end

    subgraph "API Gateway & Reverse Proxy"
        C1[Nginx / Traefik Ingress]
        C2[Global Rate Limiter]
        C3[Security Headers Injector]
    end

    subgraph "FastAPI Application Cluster"
        D1[FastAPI Worker 1]
        D2[FastAPI Worker 2]
        D3[FastAPI Worker N]
        
        subgraph "Application Internal Pipeline"
            E1[Request ID & Logging Middleware]
            E2[Pydantic Validation Layer]
            E3[Authentication & RBAC Guard]
            E4[Business Service Layer]
        end
    end

    subgraph "Data & State Storage"
        F1[(Primary PostgreSQL 16+)]
        F2[(Read Replica PostgreSQL)]
        F3[(Redis Cluster - Cache & Rate Limit)]
    end

    subgraph "Asynchronous Infrastructure"
        G1[Redis Streams Message Broker]
        G2[Background Worker Pods - ARQ/Celery]
        G3[External S3 / Cloudflare R2 - File Storage]
        G4[Transactional Email Service - SES/SendGrid]
        G5[Log Aggregator - Loki/CloudWatch]
    end

    A1 --> B1
    A2 --> B1
    B1 --> B2 --> B3 --> C1
    C1 --> C2 --> C3
    C3 --> D1
    C3 --> D2
    C3 --> D3

    D1 --> E1 --> E2 --> E3 --> E4
    E4 --> F1
    E4 --> F3
    E4 --> G1

    F1 -.->|Streaming Replication| F2
    G1 --> G2
    G2 --> G4
    G2 --> G3
    D1 -.-> G5
```

---

## 2. Career Application Submission Sequence Flow

This diagram illustrates the atomic transactional flow when a candidate submits the career application:

```mermaid
sequenceDiagram
    autonumber
    actor Candidate as Candidate Browser
    participant Gateway as API Gateway / Middleware
    participant Val as Pydantic Validation Layer
    participant Service as Application Service
    participant DB as PostgreSQL Database
    participant Cache as Redis (Rate Limit & Idempotency)
    participant Broker as Redis Queue
    participant Worker as Background Task Worker
    participant Email as Email Service (SES)

    Candidate->>Gateway: POST /api/v1/applications (JSON Body)
    Gateway->>Cache: Check Rate Limit (IP & Endpoint)
    alt Rate Limit Exceeded
        Cache-->>Gateway: Exceeded (Limit: 5/hr)
        Gateway-->>Candidate: 429 Too Many Requests
    end
    Cache-->>Gateway: Allowed

    Gateway->>Val: Deserialize & Validate Schema
    alt Validation Failure (e.g. invalid phone or terms unaccepted)
        Val-->>Gateway: Raise RequestValidationError
        Gateway-->>Candidate: 422 Unprocessable Entity (Structured details)
    end
    Val-->>Service: Validated ApplicationCreateDTO

    Service->>DB: BEGIN TRANSACTION
    Service->>DB: UPSERT applicant (email, phone, dob, gender, terms)
    Service->>DB: INSERT qualifications (bulk insert)
    Service->>DB: INSERT application_submissions (status = 'PENDING')
    Service->>DB: INSERT audit_events (action = 'APPLICATION_SUBMITTED')
    DB-->>Service: COMMIT TRANSACTION (All records persisted)

    Service->>Broker: Enqueue Job: send_candidate_acknowledgment
    Service-->>Gateway: ApplicationResponseDTO
    Gateway-->>Candidate: 201 Created (JSON Response with application_id)

    Note over Broker,Worker: Asynchronous Non-Blocking Processing
    Broker->>Worker: Consume Job
    Worker->>Email: Dispatch Acknowledgment Email to Candidate
    Email-->>Worker: 200 Sent
```

---

## 3. JWT Authentication & Refresh Token Rotation Flow

```mermaid
sequenceDiagram
    autonumber
    actor User as Admin / Client
    participant Auth as Auth Router (/api/v1/auth/token)
    participant Crypt as Password Verifier (bcrypt/Argon2id)
    participant Token as JWT Service
    participant Redis as Redis Token Store

    User->>Auth: POST credentials (email, password)
    Auth->>Crypt: verify_password(plain, stored_hash)
    alt Credentials Invalid
        Crypt-->>Auth: False
        Auth-->>User: 401 Unauthorized
    end
    Crypt-->>Auth: True

    Auth->>Token: create_access_token(sub, role, exp=30m)
    Auth->>Token: create_refresh_token(sub, family_id, exp=7d)
    Token->>Redis: Store active refresh_token_id (family_id)
    Auth-->>User: Return Access Token + Refresh Cookie (HttpOnly)

    Note over User,Auth: Subsequent Authenticated Requests
    User->>Auth: GET /api/v1/applications (Header: Bearer <AccessToken>)
    Auth->>Token: decode_and_verify(token)
    Token-->>Auth: Valid (sub, role)
    Auth-->>User: 200 OK (Protected Data)

    Note over User,Auth: Token Refresh Cycle
    User->>Auth: POST /api/v1/auth/refresh (Cookie: RefreshToken)
    Auth->>Redis: Verify refresh_token_id active
    alt Already used / revoked
        Redis-->>Auth: Invalid! Potential Replay Attack
        Auth->>Redis: Revoke entire family_id
        Auth-->>User: 401 Unauthorized (Force re-login)
    end
    Auth->>Redis: Revoke old token, Issue new access + refresh pair
    Auth-->>User: 200 OK (Rotated tokens)
```
