# Input Validation & Data Integrity Findings

> **Audit Target:** Application Form & Contact Inquiry Form on Cynbit Platform  
> **Key Standard:** OWASP Input Validation Cheat Sheet, CWE-20 (Improper Input Validation)  

---

## 1. Executive Overview

In any production architecture, **client-side validation is solely a user experience enhancement; server-side validation is the true security and integrity boundary**.

During browser inspection of `https://cynbit.in/careers/backend-developer-intern` and `https://cynbit.in/contact`, several input controls were identified. This document establishes rigorous validation specifications and details potential risks.

---

## 2. Detailed Field Validation Matrix

Below is the required server-side validation specification for the observed application fields:

| Field Name | Type | Rules & Constraints | Sanitization / Normalization | Failure Response Code |
|---|---|---|---|---|
| `fullName` | `string` | Min: 2, Max: 100 chars; regex `^[a-zA-Z\s\-'\.]+$` | Strip leading/trailing whitespace, collapse internal spaces | `422 Unprocessable Entity` |
| `email` | `EmailStr` | Valid RFC 5322 syntax; max 254 chars; valid DNS MX record (optional check) | Lowercase conversion, strip whitespace | `422 Unprocessable Entity` |
| `phone` | `string` | E.164 standard format (`^\+?[1-9]\d{7,14}$`); 8 to 15 digits | Remove spaces, hyphens, and parentheses | `422 Unprocessable Entity` |
| `whatsapp` | `string` | E.164 standard format; must match telephony pattern | Normalize digits, verify country code prefix | `422 Unprocessable Entity` |
| `dob` | `date` | Must be in the past; age between 16 and 75 years | ISO 8601 `YYYY-MM-DD` | `422 Unprocessable Entity` |
| `gender` | `enum` | Must strictly match: `Male`, `Female`, `Other`, `Prefer not to say` | Exact enum string mapping | `422 Unprocessable Entity` |
| `agreedToTerms`| `boolean` | Must be strictly `true` | Coerce boolean | `422 Unprocessable Entity` |
| `graduationYear`| `integer`| Min: 1980, Max: Current Year + 6 | Integer casting | `422 Unprocessable Entity` |
| `scoreSystem` | `enum` | `CGPA_10`, `CGPA_4`, `PERCENTAGE_100` | Standardized enum | `422 Unprocessable Entity` |
| `scoreValue` | `float` | Bounds: 0.0 to 10.0 (CGPA) or 0.0 to 100.0 (Percentage) | Float precision rounded to 2 decimals | `422 Unprocessable Entity` |
| `resumeUrl` | `HttpUrl`| Scheme must be `https://`; must not resolve to internal private IPs (SSRF check) | URL encode parameters | `422 Unprocessable Entity` |
| `linkedinUrl` | `HttpUrl`| Domain must be `linkedin.com` or `*.linkedin.com` | Normalize URL | `422 Unprocessable Entity` |
| `githubUrl` | `HttpUrl`| Domain must be `github.com` or `behance.net` | Normalize URL | `422 Unprocessable Entity` |
| `statement` | `string` | Min: 20 chars, Max: 5000 chars | Strip HTML tags, escape markdown injection | `422 Unprocessable Entity` |

---

## 3. Server-Side Validation Defenses

### 3.1 Date of Birth Boundary Constraints
A common vulnerability in naive form validation is allowing arbitrary dates:
- **Future Dates:** Accepting `dob > today` causes logical corruption in age calculation.
- **Underage / Unrealistic Bounds:** Candidates must satisfy minimum working age requirements (e.g., minimum 16 years old) and reasonable upper bounds (e.g., maximum 75 years old).
- **Leap Year & Timezone:** Dates must be validated as standard UTC calendar dates without timezone shifting artifacts.

### 3.2 URL Validation & SSRF Prevention
When applicants provide external URLs for portfolios, GitHub, or resumes:
- Ensure the scheme is strictly `https` (`http://` should be rejected or upgraded).
- Prevent Server-Side Request Forgery (SSRF): If backend services scrape or generate thumbnails from applicant links, the HTTP client must block private address ranges:
  - `127.0.0.0/8` (Loopback)
  - `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` (Private RFC 1918)
  - `169.254.169.254` (Cloud Metadata Endpoint)

### 3.3 String Truncation & Memory Exhaustion Prevention
- Freeform text areas (such as "Why Cynbit?" and "Architectural Narrative") must enforce rigid upper bounds (e.g., 5,000 characters).
- Omitting length limits allows an attacker to transmit 100MB JSON payloads, causing high CPU parsing overhead and memory exhaustion on the server (Regex Denial of Service / ReDoS).

---

## 4. Error Hygiene & Client Responses

When input validation fails:
1. **Never return raw database exceptions:** PostgreSQL integrity errors (e.g., `duplicate key value violates unique constraint "uq_applicant_email"`) or SQLAlchemy stack traces must never reach the user.
2. **Structured, deterministic schema:** Return a consistent JSON envelope with exact field pointers and actionable remediation messages:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Input validation failed on 2 fields",
    "details": [
      {
        "field": "dob",
        "message": "Date of birth must indicate an age between 16 and 75 years"
      },
      {
        "field": "agreedToTerms",
        "message": "You must agree to the Terms & Conditions to proceed"
      }
    ],
    "request_id": "req_8f1b2c4e"
  }
}
```
