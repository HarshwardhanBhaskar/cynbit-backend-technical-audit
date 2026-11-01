# Testing Methodology & Safety Protocols

> **Protocol Purpose:** Define the safe testing rules, boundary conditions, and test harness design for the Cynbit Technical Assessment.  
> **Testing Scope:** Client-side evaluation, passive network monitoring, and local automated test execution on the reference backend.  

---

## 1. Ethical Testing Standard & Safe Rules of Engagement

To guarantee zero disruption to Cynbit's production services and absolute compliance with computer security ethics:

1. **Passive Reconnaissance Only on Production:**
   - No mock inquiries or fake job applications were submitted to `cynbit.in`.
   - Inspection was strictly confined to Chrome DevTools (Elements, Network, Console, Application tabs).
2. **Strict Payload Prohibitions on Live Targets:**
   - ❌ No automated vulnerability scanners (Nikto, SQLmap, OWASP ZAP automated fuzzers).
   - ❌ No SQL injection, NoSQL injection, or Command injection payloads.
   - ❌ No Cross-Site Scripting (XSS) polyglots or alert scripts.
   - ❌ No high-frequency or stress load requests (DoS testing).
   - ❌ No credential brute forcing or enumeration attacks.
3. **Safe Client-Side Boundary Checks:**
   - Verified native browser form validation behaviors by testing inputs locally within the browser context without transmitting state-changing requests.

---

## 2. Comprehensive Test Case Specifications

The following test suite defines the expected behavioral assertions for both client-side form controls and server-side backend handlers:

| Test ID | Test Category | Scenario / Input | Expected Result | Server Response |
|---|---|---|---|---|
| **TC-VAL-01** | Empty Submission | Submit payload with all fields empty or `null` | Reject submission; highlight mandatory fields | `422 Unprocessable Entity` |
| **TC-VAL-02** | Email Syntax | `test-user@`, `user@@domain.com`, `user@domain` | Reject non-compliant RFC 5322 address | `422 Unprocessable Entity` |
| **TC-VAL-03** | Phone Number | `abcdefg`, `12345`, `+91-XXXXX` | Reject non-telephony string; enforce 8–15 digits | `422 Unprocessable Entity` |
| **TC-VAL-04** | Date of Birth | Future date (`2030-01-01`) or underage (`2020-01-01`) | Reject; candidate must be between 16 and 75 years | `422 Unprocessable Entity` |
| **TC-VAL-05** | Date of Birth | Unrealistic past date (`1850-01-01`) | Reject date out of acceptable boundary | `422 Unprocessable Entity` |
| **TC-VAL-06** | Gender Enum | `Alien`, `Robot`, or raw integer `1` | Reject value not in approved enum list | `422 Unprocessable Entity` |
| **TC-VAL-07** | Terms Consent | `agreedToTerms = false` or omitted | Mandatory agreement required to process data | `422 Unprocessable Entity` |
| **TC-VAL-08** | Graduation Year | `1950` or `2045` | Must fall within reasonable academic window (1980–2035) | `422 Unprocessable Entity` |
| **TC-VAL-09** | Academic Score | Score value `15.0` when system is `CGPA_10` | Enforce upper numeric bound matching scoring scale | `422 Unprocessable Entity` |
| **TC-VAL-10** | External URLs | `http://insecure-site.com` or `ftp://files.com` | Require secure `https://` scheme | `422 Unprocessable Entity` |
| **TC-VAL-11** | SSRF Vector | `https://169.254.169.254/latest/meta-data` | Reject IP address targeting private/metadata ranges | `422 Unprocessable Entity` |
| **TC-VAL-12** | Text Overflow | 50,000 characters in `applicationStatement` | Reject payload exceeding 5,000 character maximum | `422 Unprocessable Entity` |
| **TC-VAL-13** | Whitespace Only | `"     "` in `fullName` | Strip whitespace; treat empty string as missing value | `422 Unprocessable Entity` |
| **TC-VAL-14** | Multi-Qualification | Array of 3 valid qualification objects | Accept and persist all 3 records atomically | `201 Created` |
| **TC-VAL-15** | Rate Limiting | 6th submission within 1 hour from same IP | Throttle request; return retry interval | `429 Too Many Requests` |
| **TC-VAL-16** | Health Check | `GET /api/v1/health` | Return operational status and DB connectivity | `200 OK` |

---

## 3. Automated Test Suite Architecture (`backend-reference/tests`)

To prove the validity of these specifications, the reference backend includes a fully automated test harness:
- **Framework:** `pytest` + `pytest-asyncio`
- **HTTP Client:** `httpx.AsyncClient` with `ASGITransport` (zero network socket overhead)
- **Database Isolation:** An asynchronous in-memory SQLite database (`sqlite+aiosqlite:///:memory:`) instantiated per test run with automatic schema migration, ensuring tests are deterministic, hermetic, and execute in under 3 seconds.
