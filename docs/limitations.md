# Audit Limitations

This document provides full transparency about the boundaries of this assessment. Understanding what was and was not tested is essential for correctly interpreting the findings.

---

## 1. Access Limitations

| Limitation | Impact |
|---|---|
| **No backend source code access** | Cannot verify server-side logic, validation, or security controls |
| **No database access** | Cannot assess data storage, encryption at rest, or query patterns |
| **No infrastructure access** | Cannot evaluate server configuration, network security, or deployment |
| **No admin/dashboard access** | Cannot assess internal tools, RBAC, or admin-level security |
| **No CI/CD pipeline access** | Cannot evaluate build security, dependency scanning, or deployment flow |

---

## 2. Testing Limitations

| Limitation | Impact |
|---|---|
| **No form submissions** | Cannot verify server-side validation, error handling, or data processing |
| **No authentication testing** | Cannot assess login security, session management, or token handling |
| **No API endpoint testing** | Cannot evaluate API security, rate limiting, or error responses |
| **No file upload testing** | Cannot assess upload validation, malware scanning, or storage security |
| **No injection testing** | Cannot confirm or deny SQL injection, XSS, or other injection vulnerabilities |

---

## 3. Scope Limitations

| Limitation | Impact |
|---|---|
| **Only 2 pages inspected** | Careers and Contact pages only; other pages may have different security characteristics |
| **No mobile app analysis** | If a mobile app exists, it was not assessed |
| **No third-party integration audit** | Third-party services (beyond Google Analytics) were not evaluated |
| **Point-in-time assessment** | Findings reflect the website state at the time of inspection; changes after that are not captured |
| **No load/performance testing** | Cannot assess behavior under stress or high traffic conditions |

---

## 4. Methodology Limitations

| Limitation | Impact |
|---|---|
| **Passive inspection only** | Many backend security properties are invisible without active testing |
| **No automated scanning** | Did not use vulnerability scanners, fuzzers, or security testing tools |
| **Browser-based only** | Inspection was limited to what a browser exposes (DevTools, View Source) |
| **Single session** | No longitudinal or multi-session testing was performed |

---

## 5. What This Means for the Findings

Because of these limitations:

1. **No finding in this audit should be interpreted as a confirmed vulnerability** unless explicitly tagged as "Verified Observation."
2. **The absence of a finding does not mean the absence of a vulnerability.** Many security issues are only discoverable through active testing.
3. **Severity ratings on unverified items are conservative.** Items that could not be tested are rated no higher than "Medium" or "Informational."
4. **Recommendations are based on industry best practices**, not on exploitation of specific weaknesses.

---

## 6. Recommendations for a Full Assessment

To achieve comprehensive coverage, the following additional assessments would be recommended:

- **Authenticated penetration test** with proper authorization
- **Source code review** (SAST) of backend codebase
- **Dynamic application security testing** (DAST) with authorized scope
- **Infrastructure security assessment** (server, network, cloud configuration)
- **Dependency audit** for known vulnerabilities in third-party packages
- **API security assessment** following OWASP API Security Top 10
- **Compliance review** if handling personal data (GDPR, India DPDP Act)

> **Note:** All extended testing must be performed only with explicit written authorization from Cynbit Technologies.
