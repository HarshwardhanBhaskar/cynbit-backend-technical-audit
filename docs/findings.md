# Findings Matrix

## Table of Contents
- [Severity Summary](#severity-summary)
- [Findings Index](#findings-index)
- [Detailed Findings](#detailed-findings)

---

## Severity Summary

| Severity | Count | Verified | Potential | Not Verified |
|---|---|---|---|---|
| **Critical** | 0 | 0 | 0 | 0 |
| **High** | 0 | 0 | 0 | 0 |
| **Medium** | 3 | 0 | 3 | 0 |
| **Low** | 2 | 0 | 1 | 1 |
| **Informational** | 5 | 5 | 0 | 0 |
| **Total** | **10** | **5** | **4** | **1** |

---

## Findings Index

| ID | Title | Severity | Status |
|---|---|---|---|
| CYN-001 | Next.js Frontend Framework Identified | Informational | Verified Observation |
| CYN-002 | Google Analytics Integration Active | Informational | Verified Observation |
| CYN-003 | Contact Form Lacks Confirmed Backend Endpoint | Medium | Potential Risk |
| CYN-004 | Server-Side Input Validation Status Unknown | Medium | Potential Risk |
| CYN-005 | Rate Limiting Not Confirmed on Public Forms | Medium | Potential Risk |
| CYN-006 | HTTP Security Headers Not Fully Audited | Low | Not Verified |
| CYN-007 | CSRF Protection Status Unknown for Forms | Low | Potential Risk |
| CYN-008 | 20 Live Job Openings Displayed | Informational | Verified Observation |
| CYN-009 | Contact Information Publicly Displayed | Informational | Verified Observation |
| CYN-010 | React Server Components in Use | Informational | Verified Observation |

---

## Detailed Findings

---

### CYN-001: Next.js Frontend Framework Identified

| Field | Value |
|---|---|
| **ID** | CYN-001 |
| **Title** | Next.js Frontend Framework Identified |
| **Category** | Technology Fingerprinting |
| **Severity** | Informational |
| **Status** | Verified Observation |
| **Evidence** | Page-specific and shared JavaScript chunks consistent with Next.js bundling; RSC fetch requests observed in network tab |
| **Impact** | Framework identification is not a vulnerability. However, publicly identifiable frameworks allow attackers to target known framework-specific CVEs. |
| **Remediation** | Ensure Next.js is running the latest stable version with all security patches applied. Consider removing unnecessary version indicators from response headers. |
| **Reference** | [Next.js Security Documentation](https://nextjs.org/docs/advanced-features/security-headers) |

---

### CYN-002: Google Analytics Integration Active

| Field | Value |
|---|---|
| **ID** | CYN-002 |
| **Title** | Google Analytics Integration Active |
| **Category** | Third-Party Integration |
| **Severity** | Informational |
| **Status** | Verified Observation |
| **Evidence** | Google Analytics collection request observed in browser DevTools network tab |
| **Impact** | Standard analytics integration. Privacy impact depends on data collection configuration and consent mechanisms. |
| **Remediation** | Ensure cookie consent banner is implemented if serving users in jurisdictions requiring it (GDPR, India DPDP Act 2023). Review GA4 data retention settings. |
| **Reference** | [Google Analytics Data Privacy](https://support.google.com/analytics/answer/6004245) |

---

### CYN-003: Contact Form Lacks Confirmed Backend Endpoint

| Field | Value |
|---|---|
| **ID** | CYN-003 |
| **Title** | Contact Form Lacks Confirmed Backend Endpoint |
| **Category** | Data Handling |
| **Severity** | Medium |
| **Status** | Potential Risk |
| **Evidence** | Contact form with 5 fields observed (Full Name, Email, Company, Industry, Message). No form submission was performed. No API endpoint for form handling was identified in network observation. |
| **Impact** | If the form submission endpoint lacks proper validation, sanitization, or rate limiting, it could be vulnerable to injection attacks, spam, or data handling issues. |
| **Remediation** | Verify that the form submission endpoint implements: server-side validation, input sanitization, rate limiting, CSRF protection, and appropriate error responses. See [examples/validation/](../examples/validation/) for reference implementation. |
| **Reference** | OWASP Input Validation Cheat Sheet |

---

### CYN-004: Server-Side Input Validation Status Unknown

| Field | Value |
|---|---|
| **ID** | CYN-004 |
| **Title** | Server-Side Input Validation Status Unknown |
| **Category** | Input Validation (A03:2021 – Injection) |
| **Severity** | Medium |
| **Status** | Potential Risk |
| **Evidence** | Contact form fields observed but no submission was made. Server-side validation cannot be assessed without submitting data or reviewing source code. |
| **Impact** | Without server-side validation, the application could be vulnerable to injection attacks, data corruption, or unexpected behavior from malformed input. |
| **Remediation** | Implement comprehensive server-side validation for all form inputs: required field checks, email format validation, input length limits, type validation, and sanitization. Never rely solely on client-side validation. |
| **Reference** | CWE-20: Improper Input Validation |

---

### CYN-005: Rate Limiting Not Confirmed on Public Forms

| Field | Value |
|---|---|
| **ID** | CYN-005 |
| **Title** | Rate Limiting Not Confirmed on Public Forms |
| **Category** | Availability / Abuse Prevention |
| **Severity** | Medium |
| **Status** | Potential Risk |
| **Evidence** | Contact form is publicly accessible. No rate limiting was tested (no submissions were made). |
| **Impact** | Without rate limiting, public form endpoints can be abused for spam submissions, email bombing (if the form triggers email notifications), or resource exhaustion. |
| **Remediation** | Implement rate limiting on all public-facing form submission endpoints. Consider CAPTCHA or similar bot protection. See [examples/rate-limiting/](../examples/rate-limiting/) for reference implementation. |
| **Reference** | OWASP Rate Limiting Guidelines |

---

### CYN-006: HTTP Security Headers Not Fully Audited

| Field | Value |
|---|---|
| **ID** | CYN-006 |
| **Title** | HTTP Security Headers Not Fully Audited |
| **Category** | Transport Security |
| **Severity** | Low |
| **Status** | Not Verified |
| **Evidence** | HTTP response headers were not systematically reviewed. HTTPS is in use (confirmed by URL scheme), but specific headers (CSP, X-Frame-Options, HSTS, etc.) were not individually inspected. |
| **Impact** | Missing security headers can enable clickjacking, MIME-type sniffing, and weaken XSS protections. |
| **Remediation** | Audit and configure the following headers: `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options`, `Strict-Transport-Security`, `Referrer-Policy`, `Permissions-Policy`. See [examples/security/](../examples/security/) for configuration examples. |
| **Reference** | OWASP Secure Headers Project |

---

### CYN-007: CSRF Protection Status Unknown for Forms

| Field | Value |
|---|---|
| **ID** | CYN-007 |
| **Title** | CSRF Protection Status Unknown for Forms |
| **Category** | Session Security (A01:2021 – Broken Access Control) |
| **Severity** | Low |
| **Status** | Potential Risk |
| **Evidence** | Contact form observed but no form submission was tested. CSRF token presence was not inspected in the form HTML or network requests. |
| **Impact** | Without CSRF protection, an attacker could craft pages that trick users into submitting forms on behalf of the attacker. Impact depends on the actions the form triggers. |
| **Remediation** | Implement CSRF protection using either synchronizer tokens or SameSite cookie attributes. Next.js Server Actions include CSRF protection by default in recent versions — verify this is enabled. |
| **Reference** | CWE-352: Cross-Site Request Forgery |

---

### CYN-008: 20 Live Job Openings Displayed

| Field | Value |
|---|---|
| **ID** | CYN-008 |
| **Title** | 20 Live Job Openings Displayed |
| **Category** | Content Observation |
| **Severity** | Informational |
| **Status** | Verified Observation |
| **Evidence** | Careers page displayed 20 openings: 12 internship positions and 8 full-time positions. Job cards link to individual pages at `/careers/<slug>`. |
| **Impact** | No security impact. Indicates active hiring and a growing organization. |
| **Remediation** | N/A — Informational observation. |

---

### CYN-009: Contact Information Publicly Displayed

| Field | Value |
|---|---|
| **ID** | CYN-009 |
| **Title** | Contact Information Publicly Displayed |
| **Category** | Information Exposure |
| **Severity** | Informational |
| **Status** | Verified Observation |
| **Evidence** | Email addresses (opportunities@cynbit.in, support@cynbit.in), phone number, and headquarters address (Jaipur, Rajasthan) are publicly displayed on the contact page. |
| **Impact** | Public contact information is standard for business websites. However, displayed email addresses may receive unsolicited spam or be used in phishing/social engineering attacks. |
| **Remediation** | Consider using contact forms as the primary contact method and obfuscating email addresses where possible. Implement SPF, DKIM, and DMARC records for email domain security. |

---

### CYN-010: React Server Components in Use

| Field | Value |
|---|---|
| **ID** | CYN-010 |
| **Title** | React Server Components in Use |
| **Category** | Technology Fingerprinting |
| **Severity** | Informational |
| **Status** | Verified Observation |
| **Evidence** | RSC fetch requests observed in browser DevTools network tab, consistent with Next.js App Router architecture. |
| **Impact** | No direct security impact. RSC architecture indicates the application uses server-side rendering, which can have positive security implications (less client-side state exposure). |
| **Remediation** | N/A — Informational observation. Ensure Server Components do not inadvertently expose sensitive data in their serialized payloads. |
