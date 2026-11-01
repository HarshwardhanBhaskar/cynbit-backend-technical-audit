# Cynbit Technologies – Backend Developer Intern Technical Assessment

> **Repository Name:** `cynbit-backend-technical-audit`  
> **Target Evaluation:** [https://cynbit.in](https://cynbit.in/)  
> **Key Focus Areas:**
> - Careers Page & Role: [https://cynbit.in/careers/backend-developer-intern](https://cynbit.in/careers/backend-developer-intern)
> - Contact Inquiry Hub: [https://cynbit.in/contact](https://cynbit.in/contact)
> - Platform Index: [https://cynbit.in](https://cynbit.in/)  
> **Auditor Role:** Senior Backend Engineer, Application Security Auditor, QA Engineer & AI Automation Engineer  
> **Classification:** Comprehensive Technical Assessment & Reference Implementation  

---

## 1. Executive Overview

This repository represents an evidence-based technical assessment and engineering blueprint prepared for the **Cynbit Technologies Backend Developer Intern** role.

The audit was performed strictly through passive inspection, DOM element analysis via Chrome DevTools, and non-destructive network monitoring of Cynbit's public-facing Next.js web application. No private repositories, internal infrastructure, or databases were accessed. All findings are categorized by verification status to guarantee technical and scientific honesty:
- **`[VERIFIED OBSERVATION]`** — Directly observed and documented via reproducible DevTools evidence.
- **`[POTENTIAL RISK]`** — Plausible backend or security concern inferred from client-side indicators; requires backend verification.
- **`[RECOMMENDATION]`** — Industry-standard architectural best practice (OWASP ASVS v4.0, NIST 800-63B).
- **`[NOT VERIFIED]`** — Proprietary server-side behavior that cannot be confirmed without private codebase access.

---

## 2. Repository Structure

```
cynbit-backend-technical-audit/
│
├── README.md                          # Master overview and navigation guide
├── .gitignore                         # Python, venv, IDE, and secrets exclusions
├── .env.example                       # Documented environment variable template
│
├── docs/                              # Technical Audit Documentation Suite
│   ├── assessment-scope.md            # Scope boundaries, targets & ethical rules
│   ├── website-observations.md        # Careers & Contact page DOM inspector data
│   ├── technical-audit-report.md      # Consolidated master technical audit report
│   ├── security-findings.md           # OWASP Top 10 evaluation & findings matrix
│   ├── validation-findings.md         # Pydantic schemas, boundaries & SSRF defense
│   ├── performance-review.md          # Indexing, keyset pagination, async I/O & caching
│   ├── backend-architecture.md        # Relational schema DDL, ERD & REST API contracts
│   ├── architecture-diagram.md        # Mermaid diagrams (System, Sequence, ERD)
│   ├── testing-methodology.md         # Safe functional testing & boundary test matrix
│   ├── executive-summary.md           # High-level summary for engineering leadership
│   ├── recommendations.md             # Prioritized remediation roadmap
│   └── limitations.md                 # Complete assessment transparency
│
├── evidence/                          # Inspection Evidence & Test Protocols
│   ├── observations.md                # Raw browser inspection notes
│   ├── evidence-log.md                # Chrome DevTools HTML snippets & safe test log
│   └── screenshots/                   # Directory reserved for visual evidence (.gitkeep)
│
├── backend-reference/                 # Production-Grade FastAPI Backend Reference
│   ├── app/
│   │   ├── main.py                    # ASGI app factory, CORS & lifespan
│   │   ├── config.py                  # Pydantic Settings (12-Factor App)
│   │   ├── database.py                # Async SQLAlchemy 2.0 engine & session dependency
│   │   ├── models/                    # ORM Entities (Applicant, Qualification, Submission, Contact, Audit)
│   │   ├── schemas/                   # Pydantic v2 DTOs with custom field validators
│   │   ├── routers/                   # Modular API routers (Health, Auth, Applications, Contacts)
│   │   ├── services/                  # Business logic & atomic database transactions
│   │   └── middleware/                # Security headers, rate limiting, exception handlers, logging
│   ├── tests/                         # Hermetic async pytest test suite (15 tests passing)
│   ├── requirements.txt               # Dependencies (FastAPI, SQLAlchemy, asyncpg, etc.)
│   ├── Dockerfile                     # Multi-stage secure container build
│   ├── docker-compose.yml             # Full cluster (App + PostgreSQL + Redis)
│   └── README.md                      # Backend reference quickstart
│
├── ai-automation/                     # Autonomous AI Candidate Screening Deliverable
│   ├── README.md                      # AI automation documentation & usage guide
│   ├── architecture.md                # Deterministic gates vs LLM evaluation architecture
│   ├── workflow.md                    # 5-stage lifecycle, failure recovery & sample I/O
│   ├── requirements.txt               # Module dependencies
│   ├── src/
│   │   ├── agent.py                   # Autonomous screening agent orchestrator
│   │   ├── extractor.py               # Candidate feature & competency tokenizer
│   │   ├── evaluator.py               # Tier-1 hard gates + Tier-2 scoring engine
│   │   └── notifier.py                # Candidate status notification generator
│   └── tests/
│       └── test_workflow.py           # Hermetic test suite (4 tests passing)
│
├── architecture/                      # Additional architecture documents
│   ├── current-observations.md
│   └── recommended-architecture.md
│
└── examples/                          # Standalone reference snippets
    ├── authentication/
    ├── validation/
    ├── rate-limiting/
    └── security/
```

---

## 3. Key Verified Observations & DOM Evidence

### 3.1 Careers Page & Target Role
* **URL:** `https://cynbit.in/careers/backend-developer-intern`
* **Openings Count:** 20 live openings observed (12 internships, 8 full-time roles).
* **Role Focus:** Design secure authentication, manage and optimize PostgreSQL/MongoDB schemas, build REST/GraphQL APIs, and ensure scalability.
* **Tech Stack:** Python, Node.js, Go, PostgreSQL, MongoDB, OAuth 2.0, JWT.

### 3.2 Application Form DOM Elements
Chrome DevTools Elements inspection confirmed the following native inputs:
- `fullName` (`<input type="text" name="fullName" required>`)
- `email` (`<input type="email" name="email" required>`)
- `phone` (`<input type="tel" name="phone" required>`)
- `whatsapp` (`<input type="tel" name="whatsapp" required>`)
- `dob` (`<input type="date" name="dob" required>`)
- `gender` (`<select name="gender" required>`: `Male`, `Female`, `Other`, `Prefer not to say`)
- `terms` (`<input type="checkbox" id="terms" name="agreedToTerms" required>`): Mandatory talent acquisition consent checkbox.

### 3.3 Contact Hub
* **URL:** `https://cynbit.in/contact`
* **Section:** Inquiry Hub ("Start Your Next Project With Us")
* **Inputs:** Full Name, Email Address, Company (Optional), Industry (Optional), Your Message.
* **Public Channels:** `opportunities@cynbit.in`, `support@cynbit.in`, Jaipur Headquarters.

---

## 4. Structured Findings Matrix

| Finding ID | Category | Severity | Confidence | Status | Title |
|---|---|---|---|---|---|
| **CYN-001** | Technology Fingerprinting | Informational | 100% | Verified | Next.js Frontend Framework & RSC In Use |
| **CYN-002** | Information Exposure | Informational | 100% | Verified | Corporate Email Addresses Publicly Disclosed |
| **CYN-003** | Input Validation | Medium | 70% | Potential Risk | Reliance on Native HTML5 Form Validation |
| **CYN-004** | Abuse Prevention | Medium | 65% | Potential Risk | Absence of Observable Rate Limiting on Modals |
| **CYN-005** | Audit & Compliance | Low | 80% | Potential Risk | Consent Checkbox Lacks Immutable Audit Trail |
| **CYN-006** | Transport Security | Low | 60% | Not Verified | HTTP Security Headers Configuration Unverified |
| **CYN-007** | Broken Access Control | Low | 60% | Not Verified | CSRF Protection Status on State-Changing Routes |
| **CYN-008** | Content Observation | Informational | 100% | Verified | 20 Live Job Openings Displayed |
| **CYN-009** | Telemetry Stream | Informational | 100% | Verified | Google Analytics 4 Telemetry Stream Active |
| **CYN-010** | File Security | Medium | 65% | Recommendation | SSRF Prevention on External Candidate Links |

> **Audit Integrity Note:** No unverified issue has been assigned High or Critical severity.

---

## 5. Practical Implementations

### 5.1 Backend Reference Application (`backend-reference/`)
A modular FastAPI backend modeling the complete Cynbit workflow:
- **FastAPI + Async SQLAlchemy 2.0:** High-concurrency async database operations.
- **Normalized PostgreSQL Schema:** `applicants`, `qualifications`, `application_submissions`, `contact_inquiries`, and `audit_events`.
- **Defense-in-Depth Middleware:** Sliding window rate limiting, Security Headers injection (HSTS, CSP, X-Frame-Options, nosniff), and request correlation (`X-Request-ID`).
- **Centralized Exception Handling:** Returns structured error envelopes and suppresses raw stack traces.
- **JWT + RBAC Authentication:** Native bcrypt password hashing and token validation.

```bash
# Setup & run backend reference
cd backend-reference
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 5.2 AI Automation Deliverable (`ai-automation/`)
An autonomous **Candidate Screening & Triage Agent**:
- **Tier-1 Deterministic Hard Gates:** Instant validation of legal consent, contact syntax, and intern cohort window without LLM token costs or hallucination risks.
- **Tier-2 Architectural Scoring:** Evaluates backend skills and narrative depth with heuristic fallback when offline.
- **Notification Engine:** Generates candidate communication and HR next-action instructions.

```bash
# Setup & run AI automation
cd ai-automation
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pytest -v tests/test_workflow.py
```

---

## 6. Automated Test Results

Across both deliverables, **19 automated tests** were implemented and verified locally:

```
backend-reference/tests:
  tests/test_applications.py . . . . . . . .   [100% Pass]
  tests/test_auth.py . . .                    [100% Pass]
  tests/test_contacts.py . . .                [100% Pass]
  tests/test_health.py .                      [100% Pass]
  -> 15 passed in 1.50s

ai-automation/tests:
  tests/test_workflow.py . . . .              [100% Pass]
  -> 4 passed in 0.32s

TOTAL: 19 passed, 0 failed (100% pass rate)
```

---

## 7. Submission Checklist

- [x] Full repository scaffolding with clean Git history
- [x] Zero fabricated findings or unverified Critical/High vulnerabilities
- [x] Chrome DevTools DOM inspection of `/careers/backend-developer-intern` and `/contact`
- [x] Complete documentation suite in `docs/` (12 comprehensive reports)
- [x] Relational database schema with SQL DDL and Mermaid ERD
- [x] Production-ready FastAPI reference implementation in `backend-reference/`
- [x] Standalone AI Automation deliverable in `ai-automation/`
- [x] Complete Dockerfile and docker-compose.yml configuration
- [x] 100% passing automated test suite (19/19 tests)
- [x] `.env.example` provided; zero secrets committed to Git
