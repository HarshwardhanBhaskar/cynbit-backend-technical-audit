# Executive Summary

## Cynbit Technologies – Backend Technical Audit

**Date:** November 2026  
**Auditor:** Harshwardhan Bhaskar  
**Target:** [https://cynbit.in](https://cynbit.in)  
**Audit Type:** External Passive Inspection  

---

## Purpose

This audit was performed as part of the Cynbit Technologies Backend Developer Intern Technical Assessment. The objective is to demonstrate backend engineering competence through a structured, evidence-based review of the company's public-facing web platform.

---

## Scope

The audit covered two publicly accessible pages:

1. **Careers page** (`/careers`) — Job listing structure, CTAs, frontend technology
2. **Contact page** (`/contact`) — Form design, contact information, network behavior

The audit was **passive and non-destructive**. No forms were submitted, no backend code was accessed, and no exploitation was attempted.

---

## Key Observations

### Technology Stack
- The website is built with **Next.js** (React-based framework)
- Server-side rendering with **React Server Components (RSC)** is in use
- **Google Analytics** is integrated for tracking
- Backend technology, database, and hosting provider could not be confirmed

### Careers Page
- **20 live job openings** displayed (12 internships, 8 full-time positions)
- Job cards link to individual detail pages (`/careers/<slug>`)
- CTAs present for portfolio submission and company story
- The full job application workflow was not tested end-to-end

### Contact Page
- Professional contact form with 5 fields (Full Name, Email, Company, Industry, Message)
- Contact details publicly displayed (email addresses, phone, Jaipur HQ address)
- HTTP 200 responses for page loads and static assets
- **No API submission endpoint was confirmed** — form validation and backend handling remain untested

---

## Risk Summary

| Severity | Count | Notes |
|---|---|---|
| **Critical** | 0 | No critical vulnerabilities confirmed |
| **High** | 0 | No high-severity issues confirmed |
| **Medium** | — | Potential risks identified, pending verification |
| **Low** | — | Best-practice observations noted |
| **Informational** | Several | Technology observations and recommendations |

> **Note:** No issues have been assigned Critical or High severity because the audit scope did not include active testing that would be required to confirm such findings.

---

## Top Recommendations

1. **Verify server-side input validation** on the contact form (currently untested)
2. **Audit HTTP security headers** (Content-Security-Policy, X-Frame-Options, etc.)
3. **Implement rate limiting** on public-facing form endpoints
4. **Review CSRF protection** on form submissions
5. **Ensure API error responses** do not leak stack traces or internal paths

These are industry best-practice recommendations and are not based on confirmed vulnerabilities.

---

## Limitations

- No backend source code access
- No form submissions were made
- No authenticated endpoint testing
- No database or infrastructure assessment
- Findings are limited to what is publicly observable

For the complete list of limitations, see [limitations.md](limitations.md).

---

## Conclusion

The Cynbit Technologies website presents a professional, modern frontend built on Next.js. The technology choices observed (SSR, RSC, structured routing) indicate competent frontend engineering. However, the backend security posture cannot be fully assessed without authenticated access or active testing. The recommendations provided follow OWASP and industry best practices and should be treated as general guidance rather than responses to confirmed issues.
