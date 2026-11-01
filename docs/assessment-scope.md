# Assessment Scope and Boundaries

> **Target Platform:** Cynbit Technologies ([https://cynbit.in](https://cynbit.in/))  
> **Specific Focus Areas:**
> - Careers Page & Role: [https://cynbit.in/careers/backend-developer-intern](https://cynbit.in/careers/backend-developer-intern)
> - Contact Inquiry Hub: [https://cynbit.in/contact](https://cynbit.in/contact)
> - General Architecture & Public Surface: [https://cynbit.in](https://cynbit.in/)  
> **Evaluation Type:** External, Passive Technical Audit & Engineering Assessment  
> **Lead Reviewer:** Backend Engineering / Application Security Auditor  

---

## 1. Scope Objective

The objective of this assessment is to conduct a professional, evidence-based evaluation of the public-facing Cynbit Technologies web platform from the perspective of a Senior Backend Engineer and Application Security Reviewer. The scope is designed to demonstrate deep competency in:
- System workflow analysis and DOM/network inspection
- Backend architectural modeling and relational schema design
- Security controls (Authentication, Authorization, Session & Token management, Rate limiting, Injection prevention, CSRF, Transport security)
- Server-side data validation, normalization, and sanitization
- API contract specification and error hygiene
- Performance, indexing, and scalability planning
- Construction of a runnable reference backend in FastAPI
- An autonomous AI workflow for talent acquisition processing

---

## 2. In-Scope Targets

| Target URL / Resource | Inspection Scope | Verification Method |
|---|---|---|
| `https://cynbit.in` | Main landing page, technical headers, asset distribution, framework detection | Browser DevTools, Network Tab, View Source |
| `https://cynbit.in/careers` | Careers index, live openings count (20 listings), role categorization | DOM structure, layout components |
| `https://cynbit.in/careers/backend-developer-intern` | Job description, tech stack requirements, application modal/form elements | Chrome DevTools Elements inspection, input attributes |
| `https://cynbit.in/contact` | Inquiry Hub, contact fields, public contact channels, response claims | Form structure analysis, network request tracing |
| Public Static Assets | JavaScript bundles, CSS chunks, React Server Component (RSC) requests | Passive HTTP observation, chunk header inspection |

---

## 3. Explicit Out-of-Scope Boundaries

To maintain strict ethical boundaries and zero disruption to production systems:
- **No Access to Private Codebases:** We have no access to Cynbit's private repositories, source control, build pipelines, or cloud hosting consoles.
- **No Database Access:** Internal schemas, query engines, indexing strategies, and database engines are not directly accessible.
- **No Form Submissions with Fake/Real PII:** No live applications or unsolicited inquiry submissions were transmitted across production endpoints.
- **No Active Exploitation or Attack Simulations:**
  - ❌ No SQL injection, NoSQL injection, or Command injection payloads sent to servers
  - ❌ No Cross-Site Scripting (XSS) payload reflections attempted
  - ❌ No Brute-force credential attacks or password spraying
  - ❌ No Denial-of-Service (DoS) or volume load tests
  - ❌ No Bypass attempts on production WAFs or perimeter filters

---

## 4. Classification & Verification Standards

To guarantee scientific and engineering integrity, all statements within this repository adhere strictly to four standardized classifications:

```
[VERIFIED OBSERVATION]
Directly confirmed via reproducible browser DevTools inspection, HTTP response inspection,
or DOM element tree analysis. Zero speculation.

[POTENTIAL RISK]
An architectural or security concern identified from client-side indicators or lack of observable
defense-in-depth controls, requiring backend source verification before confirmation.

[RECOMMENDATION]
Industry-standard engineering best practices (OWASP ASVS v4.0, NIST 800-63B, RFC 7519)
proposed to guarantee resilience, data integrity, and compliance.

[NOT VERIFIED / NOT TESTED]
System behavior or backend implementation details that cannot be confirmed without private
backend source code access or active penetration testing.
```

---

## 5. Ethical & Legal Compliance

This evaluation was conducted under passive, authorized open-source intelligence (OSINT) and non-invasive browser inspection standards. No personal data was collected, exfiltrated, or processed. All architectural models and code examples are provided as vendor-neutral reference designs.
