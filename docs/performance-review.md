# Performance, Scalability & Reliability Review

> **Focus Area:** Backend Throughput, Query Optimization, Caching & Asynchronous Processing  
> **Target Architecture:** Cynbit Talent Acquisition & Inquiry Processing Pipeline  

---

## 1. Relational Database Performance & Indexing

High-throughput backend architectures require proactive database design rather than reactive query fixing.

### 1.1 Indexing Strategy
For the PostgreSQL schema supporting applications and inquiries:

1. **Composite B-Tree Indexes:**
   - `idx_applications_status_created`: `(status, created_at DESC)`  
     *Rationale:* Talent acquisition dashboards query applications by status sorted chronologically. This composite index eliminates expensive file-sort operations.
2. **Unique B-Tree Indexes:**
   - `idx_applicants_email`: `(email)`  
     *Rationale:* Instant $O(\log N)$ lookup during candidate de-duplication.
3. **Foreign Key Indexes:**
   - `idx_qualifications_applicant_id`: `(applicant_id)`  
     *Rationale:* Prevents sequential table scans when joining applicant records with academic qualification history.
4. **Partial Indexes:**
   - `idx_unprocessed_inquiries`: `(created_at) WHERE status = 'pending'`  
     *Rationale:* Indexes only the subset of inquiries needing active review, consuming 90% less disk memory than indexing the entire historical table.

---

## 2. Scalable API Pagination: Keyset vs Offset

### 2.1 The Problem with `OFFSET / LIMIT`
Standard offset pagination (`OFFSET 10000 LIMIT 50`) forces PostgreSQL to read and discard 10,000 rows sequentially before returning 50, resulting in quadratic $O(N)$ degradation as datasets grow.

### 2.2 Recommended Solution: Keyset (Cursor-Based) Pagination
Query rows relative to the last seen cursor (`id` or `created_at`):

```sql
SELECT id, full_name, email, created_at
FROM applications
WHERE created_at < :cursor_timestamp
ORDER BY created_at DESC
LIMIT 50;
```
*Complexity:* Constant $O(1)$ index seek, irrespective of whether accessing the first page or the millionth page.

---

## 3. Asynchronous I/O and Connection Pooling

### 3.1 Async Event Loop (FastAPI + `asyncpg`)
- FastAPI utilizes `uvloop` for high-concurrency non-blocking I/O.
- Database access should leverage asynchronous drivers (`asyncpg` for PostgreSQL) rather than synchronous blocking drivers (`psycopg2`), enabling a single application instance to sustain thousands of concurrent connections.

### 3.2 Database Connection Pool Sizing
Applying the standard PostgreSQL formula:
$$\text{Pool Size} = ((\text{Core Count} \times 2) + \text{Effective Spindle Count})$$
- Default pool size: 10–20 connections per pod.
- `max_overflow`: 10 burst connections.
- `pool_recycle`: 1800 seconds (prevents stale TCP connections).
- `pool_timeout`: 30 seconds (prevents hanging threads).

---

## 4. Caching & State Management (Redis)

### 4.1 Cache-Aside Pattern for Public Listings
- Job listings (`/careers`) and role descriptions (`/careers/backend-developer-intern`) change infrequently.
- **Cache-Aside Flow:**
  1. API checks Redis: `GET careers:openings`
  2. Cache Hit: Return cached JSON immediately ($<2\text{ms}$).
  3. Cache Miss: Fetch from PostgreSQL, write to Redis with a 1-hour TTL (`EX 3600`).
  4. Invalidation: Trigger Redis eviction (`DEL careers:openings`) whenever an HR administrator updates or closes a listing.

---

## 5. Background Task Offloading & Worker Queues

Heavy side-effects must never block client request-response cycles:
- **Email Notifications:** Dispatching candidate acknowledgment emails takes 300–800ms over external SMTP.
- **Resume Processing / Vector Indexing:** Parsing resumes and computing embeddings takes seconds.
- **Architecture:** Offload all downstream side-effects to asynchronous background workers (ARQ / Celery with Redis Streams). The API endpoint persists the submission, publishes an event, and returns `201 Created` in under 30ms.

---

## 6. Submission Idempotency

When users submit applications over unstable mobile connections, they frequently double-click or retry dropped requests.
- **Idempotency-Key Header:** Require an `Idempotency-Key: <UUID>` header on `POST /api/v1/applications`.
- **Backend Flow:** Store the key in Redis for 24 hours. If a request arrives with an existing key, return the cached initial response without re-executing database insertions or email triggers.
