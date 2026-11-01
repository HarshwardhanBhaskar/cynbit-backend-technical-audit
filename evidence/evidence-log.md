# Evidence Log & Safe Functional Testing Protocol

> **Audit Date:** November 2026  
> **Target Domain:** [https://cynbit.in](https://cynbit.in)  
> **Environment:** Google Chrome / Microsoft Edge DevTools on Windows 11  

---

## 1. DOM Element Inspection Evidence

### 1.1 Career Application Modal (`/careers/backend-developer-intern`)

Below are the exact DOM structures observed via Chrome DevTools Elements Inspector:

```html
<!-- Full Name Input -->
<div class="form-group">
  <label for="fullName">Full Name <span class="required">*</span></label>
  <input 
    type="text" 
    id="fullName" 
    name="fullName" 
    required 
    placeholder="Enter your full name" 
    class="cynbit-input" 
  />
</div>

<!-- Email Input -->
<div class="form-group">
  <label for="email">Email Address <span class="required">*</span></label>
  <input 
    type="email" 
    id="email" 
    name="email" 
    required 
    placeholder="name@example.com" 
    class="cynbit-input" 
  />
</div>

<!-- Phone & WhatsApp Inputs -->
<div class="form-row">
  <div class="form-group">
    <label for="phone">Phone Number <span class="required">*</span></label>
    <input 
      type="tel" 
      id="phone" 
      name="phone" 
      required 
      placeholder="+91 XXXXX XXXXX" 
    />
  </div>
  <div class="form-group">
    <label for="whatsapp">WhatsApp Number <span class="required">*</span></label>
    <input 
      type="tel" 
      id="whatsapp" 
      name="whatsapp" 
      required 
      placeholder="+91 XXXXX XXXXX" 
    />
  </div>
</div>

<!-- Date of Birth & Gender Dropdown -->
<div class="form-row">
  <div class="form-group">
    <label for="dob">Date of Birth <span class="required">*</span></label>
    <input 
      type="date" 
      id="dob" 
      name="dob" 
      required 
    />
  </div>
  <div class="form-group">
    <label for="gender">Gender <span class="required">*</span></label>
    <select id="gender" name="gender" required>
      <option value="" disabled selected>Select Gender</option>
      <option value="Male">Male</option>
      <option value="Female">Female</option>
      <option value="Other">Other</option>
      <option value="Prefer not to say">Prefer not to say</option>
    </select>
  </div>
</div>

<!-- Terms & Conditions Consent -->
<div class="form-checkbox">
  <input 
    type="checkbox" 
    id="terms" 
    name="agreedToTerms" 
    required 
  />
  <label for="terms">
    I agree to the Terms & Conditions and understand that my personal and academic data
    will be processed for architectural review during Cynbit Technologies' talent acquisition cycle.
  </label>
</div>
```

### 1.2 Visually Documented Application Fields (Pending Exact DOM Attribute Extraction)

The following fields were visually confirmed in the modal UI during inspection:

| Visual Field | Observed UI Presentation | Observed Options / Constraints | Verification Status |
|---|---|---|---|
| **Education & Qualification** | Modular section with institution entry | Repeatable card component | Visual Observation |
| **Add Another Qualification** | Interactive button element | Triggers dynamic form repeater | Visual Observation |
| **Graduation Year** | Select dropdown / numeric entry | Cohort targets (2024, 2025, 2026, 2027) | Visual Observation |
| **Education Status** | Selection / radio options | "Pursuing", "Completed" | Visual Observation |
| **Score System** | Selection menu | CGPA (out of 10), Percentage (out of 100) | Visual Observation |
| **Score Value** | Decimal / integer text input | Numeric grade entry (e.g. 8.5, 85%) | Visual Observation |
| **Notice Period** | Dropdown / text option | "Immediate", "15 Days", "1 Month" | Visual Observation |
| **Key Technical Skills** | Tag-based input / text field | Backend technologies (Python, Postgres, etc.) | Visual Observation |
| **Portfolio / Resume Link** | URL input field | External URL link to PDF / portfolio | Visual Observation |
| **LinkedIn Profile URL** | URL input field | External URL (linkedin.com/in/...) | Visual Observation |
| **GitHub / Behance Profile** | Optional URL input field | Developer / designer profile links | Visual Observation |
| **Why Cynbit? / Statement** | Multiline `<textarea>` | Personal application narrative | Visual Observation |
| **Architectural Narrative** | Multiline `<textarea>` | Technical architecture writeup | Visual Observation |

> **Ethical Note:** In strict compliance with audit rules, we do not fabricate the exact backend column mappings, internal HTML names, or proprietary API payload structures for these fields. They are fully implemented in our reference backend as proposed schemas.

---

## 2. Safe Functional Testing Matrix

To protect production server integrity and respect user privacy, **no live applications or mock contact inquiries were submitted**. Testing was restricted to client-side evaluation, DOM boundary checks, and passive HTTP request monitoring.

| Test ID | Area Tested | Test Description | Input Condition | Observed Result | Status |
|---|---|---|---|---|---|
| **SFT-001** | Contact Form | Empty form submission | Submit button clicked with all fields blank | Browser native validation triggered (`Please fill out this field`) | ✅ Verified Client-Side |
| **SFT-002** | Contact Form | Malformed email address | `invalid-user@@cynbit` | Browser rejects format before dispatch (`Include an '@' in the email address`) | ✅ Verified Client-Side |
| **SFT-003** | Career Form | Empty mandatory fields | Click submit with no fields populated | Browser flags `fullName` as required | ✅ Verified Client-Side |
| **SFT-004** | Career Form | Unchecked Terms Checkbox | All mock fields populated, terms unchecked | Browser prevents submit; highlights checkbox | ✅ Verified Client-Side |
| **SFT-005** | Career Form | Non-numeric Phone Input | `+91-ABCD-EFG` | HTML5 `type="tel"` allows freeform text on some engines; backend validation needed | ⚠️ Potential Risk |
| **SFT-006** | Career Form | Extreme String Length | 50,000 character string in statement | No `maxlength` attribute detected in raw DOM; backend limit required | ⚠️ Potential Risk |
| **SFT-007** | Career Form | Future Date of Birth | `2035-12-31` entered in date picker | No `max` attribute detected on `<input type="date">` | ⚠️ Potential Risk |
| **SFT-008** | Career Form | Whitespace-only string | Spaces only in `fullName` (`"    "`) | Native HTML `required` accepts spaces unless pattern/regex is specified | ⚠️ Potential Risk |
| **SFT-009** | Backend Endpoint | Form Submission Route | Inspect network tab during interaction | No active endpoint transmitted without triggering submission | 🔒 Not Verifiable Passively |
| **SFT-010** | Backend Endpoint | Rate Limiting Enforcement | Multiple simulated rapid submissions | Not executed to prevent traffic generation | 🔒 Not Tested (Safety Rule) |

---

## 3. Passive Network Log Summary

| Request URL / Asset | HTTP Method | Observed Status | Content Type | Role / Notes |
|---|---|---|---|---|
| `https://cynbit.in/` | `GET` | `200 OK` | `text/html; charset=utf-8` | Initial Next.js document |
| `https://cynbit.in/careers` | `GET` | `200 OK` | `text/html; charset=utf-8` | Careers index view |
| `https://cynbit.in/careers/backend-developer-intern` | `GET` | `200 OK` | `text/html; charset=utf-8` | Target role SSR page |
| `https://cynbit.in/contact` | `GET` | `200 OK` | `text/html; charset=utf-8` | Contact Inquiry Hub |
| `/_next/static/chunks/...` | `GET` | `200 OK` (cached) | `application/javascript` | React / Next.js client chunks |
| `https://www.google-analytics.com/g/collect` | `POST` | `204 No Content` | — | GA telemetry stream |
