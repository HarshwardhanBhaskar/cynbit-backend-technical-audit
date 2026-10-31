# Backend Technical Audit Report

## Cynbit Technologies — cynbit.in

---

**Document Version:** 1.0  
**Date:** November 2026  
**Auditor:** Harshwardhan Bhaskar  
**Classification:** Assessment Submission  

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Scope](#2-scope)
3. [Technology Stack Observations](#3-technology-stack-observations)
4. [Page-Level Observations](#4-page-level-observations)
5. [Security Assessment Framework](#5-security-assessment-framework)
6. [Authentication & Authorization](#6-authentication--authorization)
7. [Performance Considerations](#7-performance-considerations)
8. [Data Validation Assessment](#8-data-validation-assessment)
9. [Findings Summary](#9-findings-summary)
10. [Recommendations Summary](#10-recommendations-summary)
11. [Conclusion](#11-conclusion)

---

## 1. Introduction

This document presents a structured technical audit of the Cynbit Technologies website ([cynbit.in](https://cynbit.in)) performed as part of the Backend Developer Intern Technical Assessment. The audit employs passive, non-destructive inspection techniques to evaluate the public-facing web application from a backend engineering and security perspective.

The objective is not to identify exploitable vulnerabilities but to demonstrate a systematic, evidence-based approach to evaluating web application security and architecture.

---

## 2. Scope

### In Scope

| Target | URL | Status |
|---|---|---|
| Careers Page | `https://cynbit.in/careers` | Inspected |
| Contact Page | `https://cynbit.in/contact` | Inspected |
| HTTP Responses | Various (page loads, assets) | Observed |
| Frontend Technology | JavaScript bundles, page structure | Inspected |

### Out of Scope

- Backend source code (no access)
- Database systems (no access)
- Server/infrastructure configuration (no access)
- Authenticated areas (no credentials)
- Other pages beyond `/careers` and `/contact`
- Mobile applications (if any)
- Third-party service security

---

## 3. Technology Stack Observations

### Confirmed

| Component | Technology | Evidence |
|---|---|---|
| Frontend Framework | Next.js (React) | JS bundle structure, chunk naming conventions |
| Rendering Model | Server-Side Rendering + RSC | RSC fetch requests in network tab |
| Analytics | Google Analytics | GA collection requests observed |
| Protocol | HTTPS | URL scheme |

### Not Confirmed

| Component | Status | Notes |
|---|---|---|
| Backend Language | Unknown | No server-side code access |
| Backend Framework | Unknown | Could be Next.js API routes, standalone service, or external |
| Database | Unknown | No database indicators observed |
| Hosting/CDN | Unknown | No definitive hosting indicators noted |
| Caching Layer | Unknown | No cache headers systematically reviewed |
| Authentication System | Unknown | No login or auth pages inspected |

> **Important:** The React runtime chunk that was inspected contained framework/shared frontend code only. It does not establish the backend implementation.

---

## 4. Page-Level Observations

### 4.1 Careers Page (`/careers`)

**Verification Status:** ✅ Verified Observation

#### Content Inventory

| Element | Details |
|---|---|
| Total Job Listings | 20 |
| Internship Positions | 12 |
| Full-Time Positions | 8 |
| Job Card Links | Individual pages at `/careers/<slug>` |
| Portfolio CTA | Links to `/contact` |
| Story CTA | Links to `/story` |

#### Technical Observations

- Page loaded successfully with HTTP 200
- Job listings are rendered with consistent card components
- Individual job pages follow a clean URL pattern (`/careers/<slug>`)
- The page structure suggests a CMS or database-driven job listing system

#### What Was NOT Verified

- ❌ Whether the full job application process works end-to-end
- ❌ Whether job listing data is fetched from an API or statically rendered
- ❌ Whether job detail pages include application forms
- ❌ Backend handling of job application submissions

---

### 4.2 Contact Page (`/contact`)

**Verification Status:** ✅ Verified Observation (page content only)

#### Content Inventory

| Section | Details |
|---|---|
| Page Heading | "Start Your Next Project With Us" |
| Section Label | Inquiry Hub |

#### Contact Form Fields

| Field | Required | Type |
|---|---|---|
| Full Name | Yes (implied) | Text |
| Email Address | Yes (implied) | Email |
| Company | No (marked Optional) | Text |
| Industry | No (marked Optional) | Text/Select |
| Your Message | Yes (implied) | Textarea |
| Submit Button | — | "Send Inquiry" |

#### Displayed Contact Information

| Type | Value |
|---|---|
| Email (Opportunities) | opportunities@cynbit.in |
| Email (Support) | support@cynbit.in |
| Phone | Displayed (not recorded for privacy) |
| Headquarters | Jaipur, Rajasthan |
| Response Claim | 24-hour response time |

#### Additional Elements
- Newsletter subscription CTA
- Specialized portal: Bitelevate Program
- Specialized portal: Join the Team

#### Network Observations

| Request Type | Status |
|---|---|
| Contact page document | HTTP 200 |
| Static assets (JS, CSS, images) | HTTP 200 (most) |
| Next.js RSC fetch requests | Observed |
| Google Analytics collection | Observed |
| **Form submission API endpoint** | **Not identified** |

#### What Was NOT Verified

- ❌ Form submission behavior (no data was submitted)
- ❌ Server-side validation responses
- ❌ Error handling for invalid inputs
- ❌ Rate limiting on form submission
- ❌ CSRF token implementation
- ❌ What happens after successful form submission
- ❌ Whether form data is sent via email, stored in a database, or both

---

## 5. Security Assessment Framework

The following areas were evaluated. For each area, the verification status indicates whether evidence was collected.

### 5A. Input Sanitization & Validation

| Check | Status | Evidence |
|---|---|---|
| Client-side validation present | Not Verified | Form not submitted |
| Server-side validation present | Not Verified | No backend access |
| Input length limits enforced | Not Verified | No testing performed |
| Email format validation | Not Verified | No testing performed |
| HTML/Script injection prevention | Not Verified | No testing performed |
| SQL injection prevention | Not Verified | No testing performed |

### 5B. Output Encoding

| Check | Status | Evidence |
|---|---|---|
| HTML entity encoding | Not Verified | Would need to submit data and observe rendering |
| JSON response encoding | Not Verified | No API responses observed |
| React auto-escaping | Potential (framework default) | Next.js/React escapes by default |

### 5C. Transport Security

| Check | Status | Evidence |
|---|---|---|
| HTTPS enforced | Verified | Site accessible via HTTPS |
| HSTS header | Not Verified | Headers not systematically reviewed |
| TLS version | Not Verified | Not inspected |
| Certificate validity | Not Verified | Not inspected |

### 5D. Security Headers

| Header | Status | Evidence |
|---|---|---|
| Content-Security-Policy | Not Verified | Not inspected |
| X-Content-Type-Options | Not Verified | Not inspected |
| X-Frame-Options | Not Verified | Not inspected |
| Referrer-Policy | Not Verified | Not inspected |
| Permissions-Policy | Not Verified | Not inspected |

### 5E. Error Handling

| Check | Status | Evidence |
|---|---|---|
| Custom error pages | Not Verified | No errors triggered |
| Stack trace exposure | Not Verified | No errors triggered |
| Consistent error format | Not Verified | No API errors observed |

---

## 6. Authentication & Authorization

> **Important:** No authentication or authorization systems were observed during this audit. The inspected pages (/careers, /contact) are public-facing and do not require authentication.

The following framework is provided for completeness:

| Area | Status | Notes |
|---|---|---|
| Login page | Not Found | Not inspected beyond /careers and /contact |
| Password hashing | Not Verified | No backend access |
| Session management | Not Verified | No authenticated sessions observed |
| JWT implementation | Not Verified | No tokens observed |
| Role-based access control | Not Verified | No admin or protected areas found |
| Account recovery | Not Verified | No such feature observed |
| Multi-factor auth | Not Verified | No such feature observed |

---

## 7. Performance Considerations

| Area | Status | Notes |
|---|---|---|
| Page load time | Observed (acceptable) | Pages loaded without notable delays |
| Static asset caching | Not Verified | Cache headers not reviewed |
| Image optimization | Not Verified | Image formats and sizes not analyzed |
| Code splitting | Verified | Next.js chunk-based loading observed |
| API response time | Not Verified | No API calls tested |
| Database query performance | Not Verified | No database access |

---

## 8. Data Validation Assessment

Based on the contact form fields observed, here is the recommended validation framework:

| Field | Server-Side Validation Needed |
|---|---|
| Full Name | Required, 2-100 chars, no dangerous characters |
| Email Address | Required, RFC 5322 format, max 254 chars |
| Company | Optional, max 200 chars, sanitized |
| Industry | Optional, predefined list preferred, max 100 chars |
| Your Message | Required, 10-5000 chars, HTML stripped/escaped |

**Verification Status:** These are recommendations. Whether these validations are implemented server-side cannot be determined without submitting data or reviewing source code.

---

## 9. Findings Summary

See [findings.md](findings.md) for the complete findings matrix with detailed evidence and remediation guidance.

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 3 |
| Low | 2 |
| Informational | 5 |

---

## 10. Recommendations Summary

See [recommendations.md](recommendations.md) for the complete recommendations list with implementation guidance.

### Top 5 Recommendations

1. Verify and strengthen server-side input validation on all form endpoints
2. Implement rate limiting on public-facing form endpoints
3. Audit and configure HTTP security headers
4. Verify CSRF protection on form submissions
5. Implement structured API error responses that do not leak internals

---

## 11. Conclusion

The Cynbit Technologies website demonstrates a modern frontend architecture built on Next.js with server-side rendering capabilities. The technology choices — structured routing, React Server Components, and clean URL patterns — indicate thoughtful frontend engineering.

Due to the passive nature of this audit, most backend security properties could not be verified. The findings and recommendations in this report are intended to provide a framework for evaluating backend security rather than to assert the presence of specific vulnerabilities.

The recommendations follow OWASP and industry best practices and are accompanied by reference implementations in the `examples/` directory to demonstrate how each concern can be addressed in a production backend.

---

*End of Report*
