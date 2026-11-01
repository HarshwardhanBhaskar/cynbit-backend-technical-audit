# Consolidated Technical Audit Report

## Cynbit Technologies — Comprehensive Backend & Security Audit

---

**Document Version:** 2.0 (Consolidated Master Report)  
**Target:** [https://cynbit.in](https://cynbit.in/)  
**Role Evaluated:** Backend Developer Intern (`/careers/backend-developer-intern`)  
**Lead Auditor:** Senior Backend Engineer & Application Security Auditor  
**Date:** November 2026  

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Assessment Scope](#2-assessment-scope)
3. [Methodology](#3-methodology)
4. [Website Overview](#4-website-overview)
5. [Observed Application Workflow](#5-observed-application-workflow)
6. [Verified Frontend Findings](#6-verified-frontend-findings)
7. [Security Review](#7-security-review)
8. [Validation Review](#8-validation-review)
9. [Performance Review](#9-performance-review)
10. [Backend Architecture Proposal](#10-backend-architecture-proposal)
11. [Database Design](#11-database-design)
12. [API Design](#12-api-design)
13. [Practical Code Examples](#13-practical-code-examples)
14. [Testing Results](#14-testing-results)
15. [Risks and Priorities](#15-risks-and-priorities)
16. [Limitations](#16-limitations)
17. [Conclusion](#17-conclusion)

---

## 1. Executive Summary

This report delivers a rigorous, evidence-based technical assessment of Cynbit Technologies' public-facing digital infrastructure ([cynbit.in](https://cynbit.in)), with specific scrutiny directed toward the **Careers Application Workflow** (`/careers/backend-developer-intern`) and the **Contact Inquiry Hub** (`/contact`). 

The assessment was conducted under strict passive evaluation guidelines: no private backend repositories, production databases, or confidential server credentials were accessed. All findings are classified into standardized verification categories: **[Verified Observation]**, **[Potential Risk]**, **[Recommendation]**, and **[Not Verified]**.

Key Takeaways:
- **Architecture:** The platform is powered by a modern **Next.js** SSR architecture with React Server Components (RSC) and Google Analytics integration.
- **Workflow & UI:** The Backend Developer Intern application form contains native HTML5 required inputs and fields for personal, contact, academic, and technical qualifications.
- **Security Posture:** Zero critical or high-severity vulnerabilities were confirmed on live endpoints (in keeping with passive ethical testing). Several potential risks were identified regarding server-side validation, rate limiting, and HTTP response headers.
- **Deliverables:** A complete, production-grade reference backend has been built in FastAPI, SQLAlchemy, and PostgreSQL, accompanied by a separate AI Automation workflow for talent acquisition processing.

---

## 2. Assessment Scope

The audit target is confined to publicly observable web assets:
- **Primary Pages:** `https://cynbit.in/`, `/careers`, `/careers/backend-developer-intern`, and `/contact`.
- **In-Scope Areas:** Frontend DOM elements, input attributes, client-side scripts, HTTP response status codes, network telemetry, and transport protocol security.
- **Explicit Exclusions:** Private source repositories, internal cloud infrastructure, active penetration testing, database direct access, and transmission of fabricated data across production forms.

---

## 3. Methodology

Inspection was performed utilizing:
1. **Chrome DevTools Elements Inspector:** To extract exact DOM tag names, input types, and attributes (`fullName`, `email`, `phone`, `whatsapp`, `dob`, `gender`, `terms`).
2. **Chrome DevTools Network Monitor:** To analyze document loading, static chunk distribution, RSC streaming, and telemetry calls.
3. **OWASP ASVS v4.0 & CWE Taxonomy:** To evaluate defense-in-depth requirements across authentication, session management, input validation, and rate limiting.
4. **Safety Protocol:** Strictly zero destructive payloads, credential brute-forcing, or data pollution.

---

## 4. Website Overview

Cynbit Technologies maintains an online presence centered around technology consulting, architecture engineering, and talent development.
- **Careers Section:** Displays 20 live openings (12 internships and 8 full-time roles).
- **Target Opening:** Backend Developer Intern, emphasizing authentication systems, schema optimization, REST/GraphQL APIs, scalability, Python, Node.js, Go, PostgreSQL, and MongoDB.
- **Contact Hub:** Prominently advertises a 24-hour response turnaround and provides direct email channels (`opportunities@cynbit.in`, `support@cynbit.in`).

---

## 5. Observed Application Workflow

The application workflow for prospective engineers entails:
1. Navigating to the individual job posting at `/careers/backend-developer-intern`.
2. Interacting with the application modal/form.
3. Entering personal identity data: `fullName`, `email`, `phone`, `whatsapp`, `dob`, and `gender`.
4. Entering academic credentials: `graduationYear`, `educationStatus`, `scoreSystem`, `scoreValue`, and repeating via "Add Another Qualification".
5. Supplying technical links: Portfolio/Resume URL, LinkedIn, GitHub/Behance.
6. Drafting narrative statements: "Why Cynbit?" and "Architectural Narrative".
7. Explicitly checking the mandatory Terms & Conditions consent checkbox.
8. Submitting the package for review during Cynbit's talent acquisition cycle.

---

## 6. Verified Frontend Findings

| Verified Item | DOM / Network Evidence | Verification Status |
|---|---|---|
| **Next.js SSR Stack** | `/_next/static/chunks/...` script tags and React Server Component fetch headers | [VERIFIED OBSERVATION] |
| **Full Name Input** | `<input type="text" name="fullName" required placeholder="Enter your full name">` | [VERIFIED OBSERVATION] |
| **Email Input** | `<input type="email" name="email" required placeholder="name@example.com">` | [VERIFIED OBSERVATION] |
| **Phone & WhatsApp** | `<input type="tel" name="phone" required>` and `<input type="tel" name="whatsapp" required>` | [VERIFIED OBSERVATION] |
| **Date of Birth** | `<input type="date" name="dob" required>` | [VERIFIED OBSERVATION] |
| **Gender Dropdown** | `<select name="gender" required>` with options: `Male`, `Female`, `Other`, `Prefer not to say` | [VERIFIED OBSERVATION] |
| **Terms Checkbox** | `<input type="checkbox" id="terms" name="agreedToTerms" required>` with mandatory talent review consent | [VERIFIED OBSERVATION] |
| **Analytics Stream** | HTTP POST telemetry dispatch to `https://www.google-analytics.com/g/collect` | [VERIFIED OBSERVATION] |

---

## 7. Security Review

### Comprehensive Finding Summaries

#### CYN-001: Technology Fingerprinting via Framework Chunks
* **Category:** Information Exposure (CWE-200) | **Severity:** Informational | **Confidence:** 100%
* **Evidence:** Next.js chunk naming conventions visible in page source.
* **Remediation:** Disable `poweredByHeader` in Next.js config; ensure dependencies remain updated against known CVEs.

#### CYN-002: Public Corporate Email Exposure
* **Category:** Information Exposure (CWE-200) | **Severity:** Informational | **Confidence:** 100%
* **Evidence:** Plaintext mailto links for `opportunities@cynbit.in` and `support@cynbit.in`.
* **Remediation:** Route all incoming messages through captcha-protected contact forms; implement strict SPF, DKIM, and DMARC DNS policies.

#### CYN-003: Potential Reliance on Client-Side Form Validation
* **Category:** Input Validation (CWE-20) | **Severity:** Medium | **Confidence:** 70%
* **Evidence:** Native HTML5 validation present; backend endpoint handling not publicly exposed.
* **Remediation:** Implement server-side Pydantic models with type coercion, boundary checks, and sanitization.

#### CYN-004: Lack of Observable Rate Limiting on Application Modal
* **Category:** Abuse Prevention (CWE-400) | **Severity:** Medium | **Confidence:** 65%
* **Evidence:** No client-side captcha challenge before dispatching applications.
* **Remediation:** Enforce distributed Redis sliding-window rate limiting (e.g., 5 submissions/hour/IP) combined with Cloudflare Turnstile.

#### CYN-005: Audit Logging of Legal Consent
* **Category:** Compliance / Auditability | **Severity:** Low | **Confidence:** 80%
* **Evidence:** Checkbox `agreedToTerms` captured without verified server-side audit table.
* **Remediation:** Record IP address, user-agent, terms version ID, and timestamp into an immutable `audit_events` table upon submission.

---

## 8. Validation Review

To protect data integrity, every field identified on the application modal must be validated server-side:
- **Full Name:** 2 to 100 characters, alphabet and standard punctuation only.
- **Phone / WhatsApp:** Validated against E.164 telephony standard (`^\+?[1-9]\d{7,14}$`).
- **Date of Birth:** Constrained between 16 and 75 years relative to the current UTC timestamp. Future dates must trigger an immediate `422 Unprocessable Entity`.
- **URLs (Resume, LinkedIn, GitHub):** Scheme must strictly be `https://`. Must block private/internal IP ranges (SSRF defense).
- **Text Bounds:** Narrative statements capped at 5,000 characters to prevent memory exhaustion and ReDoS attacks.

---

## 9. Performance Review

Key performance recommendations for high-throughput talent acquisition systems:
1. **Database Indexing:** Composite index `(status, created_at DESC)` on applications; partial index on unprocessed contact inquiries.
2. **Cursor Pagination:** Keyset pagination utilizing `created_at` or `id` instead of high-offset SQL queries.
3. **Async I/O:** Async event loops using `asyncpg` with a pooled connection pool of 10–20 connections.
4. **Cache-Aside:** Redis caching for public job descriptions with a 1-hour TTL.
5. **Background Task Workers:** Asynchronous worker processing for resume parsing and confirmation email dispatch.

---

## 10. Backend Architecture Proposal

A decoupled, layered micro-architecture:
- **Edge:** Cloudflare WAF, TLS 1.3, DDoS filtering.
- **API Gateway:** Reverse proxy handling rate limiting, CORS headers, and request ID correlation.
- **Application Core:** FastAPI application pods executing stateless business logic.
- **Persistence Layer:** PostgreSQL 16+ (Primary + Read Replica) with strict foreign key constraints.
- **Cache & Message Broker:** Redis cluster for session rate-limiting and job queueing.

---

## 11. Database Design

A fully normalized relational schema comprising:
- `applicants`: Core candidate identity and contact records.
- `qualifications`: Repeatable educational history linked via foreign key (`ON DELETE CASCADE`).
- `application_submissions`: Specific role applications with narrative statements and status enum.
- `application_status_history`: Historical transition log tracking reviewer decisions.
- `contact_inquiries`: General inquiries from `/contact`.
- `audit_events`: Immutable audit trail for compliance with data protection standards.

---

## 12. API Design

RESTful endpoints featuring standard HTTP verb semantics:
- `GET /api/v1/health`: System health and DB readiness probe.
- `POST /api/v1/applications`: Atomic applicant and qualification ingestion.
- `GET /api/v1/applications/{id}`: Protected candidate retrieval.
- `PATCH /api/v1/applications/{id}/status`: State transition endpoint for HR reviewers.
- `POST /api/v1/contacts`: Contact inquiry submission.
- `POST /api/v1/auth/token`: JWT credential authentication.

---

## 13. Practical Code Examples

To demonstrate these recommendations in action, a complete reference application has been developed in `backend-reference/`:
- **App Core:** Modular routers, Pydantic schemas, and SQLAlchemy ORM models.
- **Security:** bcrypt password hashing, JWT bearer auth with RBAC dependency injection, security headers middleware, and centralized exception handling.
- **Testing:** Automated test suite (`pytest`) executing against an in-memory async SQLite engine.

---

## 14. Testing Results

All automated test cases implemented in the reference backend were executed:
- **Total Tests:** 16 automated assertions.
- **Passing:** 16 (100%).
- **Key Scenarios Tested:** Empty payloads (422), malformed phone numbers (422), future date of birth (422), unaccepted terms (422), valid multi-qualification submission (201), JWT authentication (200/401), and health probe (200).

---

## 15. Risks and Priorities

| Priority | Action Item | Estimated Effort |
|---|---|---|
| **P1 - High** | Implement server-side Pydantic validation across all public input forms | 2-3 Days |
| **P2 - High** | Deploy Redis-backed rate limiting on application and inquiry routes | 1-2 Days |
| **P3 - Medium** | Audit and declare explicit HTTP security headers (CSP, HSTS, X-Frame-Options) | 1 Day |
| **P4 - Medium** | Establish immutable audit event logging for applicant consent | 2 Days |
| **P5 - Low** | Implement email address obfuscation and strict DNS SPF/DKIM/DMARC records | 1 Day |

---

## 16. Limitations

- **Point-in-Time Review:** This audit reflects website behavior observed in November 2026.
- **No Private Source Code Access:** Internal routing logic, database configurations, and server scripts could not be directly reviewed.
- **No Live Exploitation:** Conforms to ethical disclosure standards; zero live attack payloads were sent.

---

## 17. Conclusion

The Cynbit Technologies platform presents a modern, responsive web presence built on Next.js. While the client-side user experience is well-structured, backend engineering excellence demands defense-in-depth: complete server-side validation, distributed rate limiting, secure relational data modeling, and rigorous error handling. The accompanying reference implementation (`backend-reference/`) and AI automation module (`ai-automation/`) provide concrete, executable blueprints for these standards.
