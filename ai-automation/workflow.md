# AI Automation Workflow & Processing Specification

> **Pipeline:** Candidate Application Triage & Architectural Assessment  
> **Trigger:** Application Submission Event (`APPLICATION_SUBMITTED`)  

---

## 1. End-to-End Processing Steps

The workflow follows a 6-stage lifecycle:

```mermaid
sequenceDiagram
    autonumber
    actor Trigger as Application Ingestion Event
    participant Agent as Agent Orchestrator (agent.py)
    participant Extractor as Feature Extractor (extractor.py)
    participant Evaluator as Evaluation Engine (evaluator.py)
    participant Notifier as Notification Generator (notifier.py)

    Trigger->>Agent: process_candidate(raw_payload)
    Note over Agent: Stage 1: Payload Ingestion & Validation
    
    Agent->>Extractor: extract_features(raw_payload)
    Extractor-->>Agent: CandidateProfileDTO

    Note over Agent: Stage 2: Deterministic Hard Gates
    Agent->>Evaluator: run_deterministic_checks(profile)
    alt Fails Hard Gate (e.g. Terms Unaccepted or Missing Skills)
        Evaluator-->>Agent: GateResult(passed=False, reason=...)
        Agent->>Notifier: generate_rejection_notice(profile, reason)
        Notifier-->>Agent: EmailMessageDTO
        Agent-->>Trigger: TriageResult(status="REJECTED", tier="DETERMINISTIC")
    end
    Evaluator-->>Agent: GateResult(passed=True)

    Note over Agent: Stage 3: LLM Architectural Scoring
    Agent->>Evaluator: run_llm_evaluation(profile)
    Evaluator-->>Agent: EvaluationScoreDTO (Score, Strengths, Weaknesses, Decision)

    Note over Agent: Stage 4: Triage Classification
    alt Score >= 75
        Agent->>Notifier: generate_shortlist_notice(profile)
    else Score between 50 and 74
        Agent->>Notifier: generate_manual_review_notice(profile)
    else Score < 50
        Agent->>Notifier: generate_rejection_notice(profile)
    end
    Notifier-->>Agent: NotificationDTO

    Note over Agent: Stage 5: Output Generation & Telemetry
    Agent-->>Trigger: FullTriageReportDTO
```

---

## 2. Failure Handling & Retry Strategy

| Failure Scenario | Mitigation / Recovery Mechanism |
|---|---|
| **Malformed Ingestion Payload** | Caught at Stage 1; immediately logged as `ERROR` and routed to dead-letter queue without triggering LLM. |
| **LLM Provider Outage / 503** | Exponential backoff retry (3 attempts: 1s, 2s, 4s). If all retries fail, fall back gracefully to the heuristic rule engine with `triage_status="MANUAL_HR_REVIEW"`. |
| **API Rate Limit Exceeded (429)** | Respect `Retry-After` header with jitter. |
| **Incomplete Resume / Narrative** | Extractor flags `low_information_density=True`; penalizes contextual score without crashing. |

---

## 3. Sample Input & Output

### 3.1 Sample Ingestion Input
```json
{
  "full_name": "Harshwardhan Bhaskar",
  "email": "harshwardhan@example.com",
  "phone": "+919876543210",
  "graduation_year": 2025,
  "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "AsyncIO"],
  "agreed_to_terms": true,
  "application_statement": "Deeply interested in scalable backend architectures and API security.",
  "architectural_narrative": "Designed relational schemas with composite indexing, asyncpg connection pooling, and JWT with RBAC."
}
```

### 3.2 Sample Triage Output
```json
{
  "candidate_name": "Harshwardhan Bhaskar",
  "email": "harshwardhan@example.com",
  "deterministic_passed": true,
  "overall_score": 88,
  "decision": "SHORTLIST",
  "evaluation_tier": "LLM_ASSISTED",
  "strengths": [
    "Core backend stack matches Cynbit requirements (Python, PostgreSQL, FastAPI)",
    "Explicit architectural understanding of connection pooling and database indexing",
    "Valid graduation year for intern cohort (2025)"
  ],
  "areas_for_review": [
    "Verify depth of Redis distributed caching knowledge in technical interview"
  ],
  "notification_preview": {
    "subject": "Update on your Backend Developer Intern Application at Cynbit Technologies",
    "recipient": "harshwardhan@example.com",
    "action_required": "Schedule Technical Architecture Interview"
  }
}
```
