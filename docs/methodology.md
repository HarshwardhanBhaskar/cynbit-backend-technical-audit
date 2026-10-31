# Audit Methodology

## 1. Approach

This audit follows an **external, passive inspection** methodology. No authenticated access, source code access, or active exploitation techniques were used. The goal is to identify observable security characteristics, technology indicators, and potential areas for improvement based on what is publicly visible.

### Methodology Classification

| Aspect | Classification |
|---|---|
| **Type** | External Passive Audit |
| **Access Level** | Unauthenticated, Public |
| **Techniques** | Visual inspection, HTTP observation, technology fingerprinting |
| **Destructive Testing** | Not performed |
| **Active Exploitation** | Not performed |

---

## 2. Inspection Phases

### Phase 1: Reconnaissance (Passive)
- Visual inspection of public-facing pages
- Technology stack identification via page source and network activity
- HTTP response code observation
- Frontend framework identification

### Phase 2: Page-Level Analysis
- Element inventory (forms, CTAs, navigation, links)
- Input field mapping on interactive pages
- Network request observation (document loads, static assets, API patterns)
- Client-side JavaScript bundle inspection (limited to publicly served chunks)

### Phase 3: Security Indicator Assessment
- HTTPS/TLS status check
- HTTP security header observation
- Cookie attribute inspection (where visible)
- Error handling behavior (based on standard navigation only)

### Phase 4: Architecture Inference
- Frontend framework and rendering model identification
- API pattern observation (RSC fetches, static asset patterns)
- Third-party integration identification (analytics, tracking)
- Hosting/CDN indicators (where visible)

### Phase 5: Documentation and Reporting
- Findings categorized by verification status
- Severity assigned based on verifiable evidence
- Recommendations mapped to industry standards (OWASP, CWE)
- Reference implementations provided for applicable findings

---

## 3. Tools Used

| Tool | Purpose |
|---|---|
| **Web Browser** (Chrome/Edge) | Visual page inspection |
| **Browser DevTools** | Network tab, Elements tab, Console |
| **View Source** | Page structure and technology identification |
| **HTTP Observation** | Status codes, response headers, request patterns |

No automated scanning tools, vulnerability scanners, or exploitation frameworks were used.

---

## 4. Standards Referenced

- [OWASP Top 10 (2021)](https://owasp.org/Top10/)
- [OWASP Application Security Verification Standard (ASVS) v4.0](https://owasp.org/www-project-application-security-verification-standard/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [RFC 6749 – OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc6749)
- [RFC 7519 – JSON Web Tokens](https://datatracker.ietf.org/doc/html/rfc7519)

---

## 5. Ethical Boundaries

The following actions were **explicitly avoided**:

- ❌ Submitting test data through forms
- ❌ Attempting SQL injection, XSS, or any injection attack
- ❌ Brute-force login or credential stuffing
- ❌ Denial-of-service or load testing
- ❌ Accessing non-public endpoints or admin panels
- ❌ Intercepting or modifying traffic between client and server
- ❌ Social engineering or phishing attempts
- ❌ Downloading or exfiltrating any user data

All inspection was limited to what a normal visitor would see when browsing the website.

---

## 6. Verification Status Definitions

Each finding in this audit is tagged with one of the following verification statuses:

| Status | Meaning |
|---|---|
| **Verified Observation** | Directly observed and documented with evidence |
| **Potential Risk** | Inferred from observed indicators but not confirmed through testing |
| **Not Verified** | Relevant security area but no evidence collected either way |
| **Recommendation** | Best-practice suggestion not tied to a specific observed issue |

These statuses ensure that the reader can clearly distinguish between facts and professional judgement.
