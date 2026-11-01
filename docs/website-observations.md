# Website and Application Workflow Observations

> **Audited Targets:**
> - [https://cynbit.in/careers](https://cynbit.in/careers)
> - [https://cynbit.in/careers/backend-developer-intern](https://cynbit.in/careers/backend-developer-intern)
> - [https://cynbit.in/contact](https://cynbit.in/contact)

---

## 1. Careers Page & Role Overview

### 1.1 Index Page (`/careers`)
- **Total Openings Observed:** 20 live job openings.
- **Breakdown:** 12 internship positions, 8 full-time positions.
- **Navigation Structure:** Clean slug-based routing (`/careers/<slug>`).
- **Call-to-Action Elements:**
  - Portfolio review CTA routing to `/contact`
  - Company journey CTA routing to `/story`

### 1.2 Target Role: Backend Developer Intern
- **Target URL:** `https://cynbit.in/careers/backend-developer-intern`
- **Location / Mode:** Remote / Jaipur, Rajasthan
- **Employment Type:** Internship
- **Role Narrative:** Focused on designing and maintaining the high-performance core of Cynbit's software architecture.
- **Core Responsibilities:**
  1. Design and implement secure authentication and authorization systems (OAuth, JWT, session management).
  2. Architect, manage, and optimize database schemas, relational indexes, and query execution plans.
  3. Develop and document high-throughput RESTful and GraphQL APIs.
  4. Ensure overall backend scalability, fault tolerance, and security hardening.
- **Documented Requirements / Tech Stack:**
  - Programming Languages: Python, Node.js, or Go
  - Databases: PostgreSQL and MongoDB
  - Security / Protocols: OAuth 2.0, JWT, REST, GraphQL
  - Strong architectural mindset and database normalization knowledge

---

## 2. Application Form — Exact HTML DOM Inspection

The application modal on `/careers/backend-developer-intern` was inspected using Chrome DevTools Elements inspector.

### 2.1 Confirmed Input Elements (Verified via DOM Inspection)

| Form Field Label | HTML Tag | Name Attribute (`name=`) | Type Attribute (`type=`) | Required | Additional DOM Attributes / Values |
|---|---|---|---|---|---|
| **Full Name** | `<input>` | `fullName` | `text` | Yes (`required`) | `placeholder="Enter your full name"` |
| **Email Address** | `<input>` | `email` | `email` | Yes (`required`) | Browser RFC 5322 pattern check |
| **Phone Number** | `<input>` | `phone` | `tel` / `text` | Yes (`required`) | Telephony input |
| **WhatsApp Number** | `<input>` | `whatsapp` | `tel` / `text` | Yes (`required`) | Telephony input |
| **Date of Birth** | `<input>` | `dob` | `date` | Yes (`required`) | Date picker interface |
| **Gender** | `<select>` | `gender` | Dropdown | Yes (`required`) | Dropdown menu (see options below) |
| **Consent & Terms** | `<input>` | `agreedToTerms` | `checkbox` | Yes (`required`) | `id="terms"`, mandatory checkbox |

#### Gender Dropdown Verified Options:
```html
<select name="gender" required>
  <option value="" disabled selected>Select Gender</option>
  <option value="Male">Male</option>
  <option value="Female">Female</option>
  <option value="Other">Other</option>
  <option value="Prefer not to say">Prefer not to say</option>
</select>
```

#### Terms Checkbox & Consent Text:
- **Element ID:** `terms`
- **Element Name:** `agreedToTerms`
- **Type:** `checkbox`
- **Mandatory:** Yes (`required`)
- **Observed Legal / Talent Acquisition Text:**
  > *"I agree to the Terms & Conditions and understand that my personal and academic data will be processed for architectural review during Cynbit Technologies' talent acquisition cycle."*

### 2.2 Application Fields Identified Visually (Pending Direct Backend Verification)

The following input sections were visually documented on the interactive application form:
1. **Graduation Year** (Numeric/Dropdown, e.g., 2024, 2025, 2026, 2027)
2. **Education Status** (e.g., Pursuing, Completed)
3. **Score System** (e.g., CGPA out of 10, Percentage out of 100)
4. **Score Value** (Float/Numeric grade entry)
5. **Add Another Qualification** (Dynamic repeatable client-side form repeater)
6. **Notice Period** (Dropdown / Input, e.g., Immediate, 15 Days, 1 Month)
7. **Key Technical Skills** (Tags / Text input for backend skills)
8. **Portfolio / Resume Link** (External URL to PDF or portfolio)
9. **LinkedIn Profile URL** (URL string)
10. **GitHub / Behance Profile URL** (Optional professional profile link)
11. **Why Cynbit? / Application Statement** (Multiline `<textarea>`)
12. **Architectural Narrative** (Technical write-up or problem-solving response)

> **Integrity Note:** While these visual fields are visible to applicants, their internal HTML attributes, exact backend column mappings, and server-side validation rules have not been exposed in source code and are clearly classified as **Pending Exact HTML Inspection**.

---

## 3. Contact Page Inspection (`/contact`)

### 3.1 Visible UI Elements
- **Heading:** *"Start Your Next Project With Us"*
- **Section Label:** `Inquiry Hub`
- **Response Claim:** Prominently advertises a 24-hour response turnaround.
- **Form Inputs:**
  - Full Name (required)
  - Email Address (required, type="email")
  - Company (explicitly marked "Optional")
  - Industry (explicitly marked "Optional")
  - Your Message (required multiline textarea)
  - Action Button: `"Send Inquiry"`

### 3.2 Publicly Disclosed Contact Channels
- **Inquiries / Careers:** `opportunities@cynbit.in`
- **Support / General:** `support@cynbit.in`
- **Headquarters Location:** Jaipur, Rajasthan, India
- **Additional CTAs:**
  - Bitelevate Program portal link
  - Join the Team link
  - Newsletter subscription widget

---

## 4. Frontend Technical Observations

- **Application Architecture:** Built on modern **Next.js** framework with **React** component hierarchy.
- **Rendering Model:** Uses Server-Side Rendering (SSR) combined with React Server Components (RSC) hydration for dynamic interactive states.
- **Structured Data:** Embedded JSON-LD schema describing the Organization, address, and social metadata.
- **Client-Side Form Validation:** The DOM relies on native HTML5 constraints (`required`, `type="email"`, `type="date"`). 
  - *Engineering Warning:* Native browser constraints can be bypassed trivially via DevTools or headless HTTP clients (e.g., curl, Postman). Robust server-side validation is indispensable.
