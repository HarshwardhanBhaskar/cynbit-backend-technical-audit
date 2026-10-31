# Raw Inspection Observations

> **Date:** November 2026  
> **Inspector:** Harshwardhan Bhaskar  
> **Method:** Passive browser inspection (Chrome/Edge DevTools)

---

## 1. Careers Page — `/careers`

### Visual Observations

- **Page loaded successfully** — HTTP 200 response
- **Job listings count:** 20 total
  - 12 internship positions
  - 8 full-time positions
- **Job card structure:**
  - Each card is a clickable element
  - Links follow the pattern `/careers/<slug>`
  - Cards display job title and type (internship/full-time)
- **Call-to-Action buttons:**
  - Portfolio CTA → links to `/contact`
  - Company Story CTA → links to `/story`
- **Page layout:** Clean, card-based grid layout

### Technical Observations

- **Framework:** Next.js identified via JavaScript chunk naming patterns
- **Rendering:** Server-side rendered content with client-side hydration
- **JavaScript bundles:**
  - Page-specific chunks loaded for the careers page
  - Shared/framework chunks loaded (React runtime, Next.js core)
- **The inspected shared JavaScript chunk** contained framework/shared frontend code
- **The uploaded React runtime chunk** did not establish backend implementation details

### Network Tab

- Document request: `GET /careers` → 200
- Static JS chunks: Multiple requests → 200
- Static CSS: Loaded → 200
- RSC fetch requests visible (consistent with Next.js App Router)
- Google Analytics collection request observed

---

## 2. Contact Page — `/contact`

### Visual Observations

#### Inquiry Hub Section
- **Heading:** "Start Your Next Project With Us"
- **Section label:** Inquiry Hub

#### Contact Form
| Field Label | Input Type | Required |
|---|---|---|
| Full Name | Text input | Yes (implied) |
| Email Address | Email input | Yes (implied) |
| Company | Text input | No (marked "Optional") |
| Industry | Text input or select | No (marked "Optional") |
| Your Message | Textarea | Yes (implied) |

- **Submit button label:** "Send Inquiry"

#### Contact Details Displayed
- **Email (Opportunities):** opportunities@cynbit.in
- **Email (Support):** support@cynbit.in
- **Phone:** Displayed on page (not recorded in this document for privacy)
- **Headquarters:** Jaipur, Rajasthan
- **Response claim:** 24-hour response time

#### Additional Page Elements
- Newsletter subscription CTA
- Bitelevate Program portal link
- Join the Team portal link

### Network Tab

- Document request: `GET /contact` → 200
- Static resources: Most returned HTTP 200
- Next.js RSC fetch requests visible
- Google Analytics collection request visible
- **No form submission API endpoint was identified** during passive observation
  - The form was not submitted
  - No XHR/fetch requests to a form handling endpoint were triggered

---

## 3. General Observations

### Technology Indicators

| Indicator | Source | Confidence |
|---|---|---|
| Next.js framework | JS bundle patterns, chunk naming | High |
| React | Component hydration, JSX patterns | High |
| React Server Components | RSC fetch requests in network tab | High |
| Google Analytics | GA collection request | High |
| Server-Side Rendering | Initial HTML content present before JS execution | High |

### What Was NOT Observed

- No login or registration pages were visited
- No API endpoints were directly called
- No form submissions were made
- No error pages were triggered
- No admin panels or dashboards were found
- No cookies were manually inspected
- No HTTP response headers were systematically reviewed

---

## 4. Screenshots

> **Note:** Screenshots directory (`evidence/screenshots/`) is reserved for visual evidence.  
> Screenshots should be added to support specific findings when captured during inspection.

No screenshots were captured during this observation session.

---

## 5. Observation Integrity Statement

All observations recorded in this document were made through standard browser navigation and developer tools inspection. No data was submitted, no forms were filled, no automated tools were used, and no attempts were made to access non-public areas of the website.
