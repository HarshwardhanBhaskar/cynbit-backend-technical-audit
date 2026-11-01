# AI Automation Architecture

> **Component:** AI Candidate Screening & Triage Pipeline  
> **Domain:** Talent Acquisition Automation for Backend Developer Roles  
> **Pattern:** Hybrid Deterministic Verification + LLM Scoring Fallback  

---

## 1. Architectural Philosophy: Deterministic vs. LLM Decisions

A critical engineering failure in naive AI implementations is delegating hard deterministic constraints (e.g., minimum working age, mandatory legal consent, required contact information) to non-deterministic Large Language Models (LLMs). This introduces hallucinations, non-reproducible outcomes, and potential regulatory liability under data protection laws.

Our architecture enforces a **two-tier decision model**:

```mermaid
graph TD
    A[Incoming Candidate Submission] --> B[Tier 1: Deterministic Engine]
    
    subgraph "Deterministic Hard Gates (Zero LLM Tokens)"
        B --> B1{Agreed to Terms?}
        B1 -->|No| R1[Immediate Rejection: Consent Missing]
        B1 -->|Yes| B2{Valid E.164 Contact & Email?}
        B2 -->|No| R2[Immediate Rejection: Invalid Contact]
        B2 -->|Yes| B3{Graduation Year in Scope?}
        B3 -->|No| R3[Immediate Rejection: Academic Out of Scope]
        B3 -->|Yes| B4{Essential Skills Present?}
        B4 -->|Fail| R4[Deterministic Auto-Filter]
    end

    B4 -->|Passes Hard Gates| C[Tier 2: AI Evaluator Agent]

    subgraph "LLM Evaluation (Contextual Reasoning)"
        C --> C1[Extract Architectural Narrative & Resume Signals]
        C1 --> C2[LLM Evaluation Engine: Prompt Template + Rubric]
        C2 --> C3{Confidence Score >= 0.75?}
        C3 -->|Yes| D1[Decision: SHORTLIST]
        C3 -->|0.50 - 0.74| D2[Decision: MANUAL_HR_REVIEW]
        C3 -->|Below 0.50| D3[Decision: REJECT]
    end

    D1 --> E[Disposition Notification Service]
    D2 --> E
    D3 --> E
    E --> F[Persistence & Audit Log]
```

---

## 2. Component Architecture

```mermaid
graph LR
    subgraph "ai-automation Package"
        A[Client / Trigger] --> B[agent.py - Workflow Orchestrator]
        B --> C[extractor.py - Feature Extraction & Normalization]
        B --> D[evaluator.py - Rule-Based + LLM Evaluator]
        B --> E[notifier.py - Candidate Disposition & Email Formatter]
    end

    subgraph "External Integrations"
        D -.->|OpenAI API / Mock Fallback| F[LLM Provider]
        E -.->|SMTP / SES API| G[Notification Gateway]
    end
```

### 2.1 Component Responsibilities

1. **`extractor.py`**:
   - Parses the application payload into a normalized candidate profile.
   - Extracts technical skill tokens (Python, PostgreSQL, Docker, Async, FastAPI, MongoDB, Go).
   - Normalizes URLs and computes candidate academic tenure.
2. **`evaluator.py`**:
   - Executes Tier-1 deterministic rule checks (zero cost, 100% deterministic).
   - Executes Tier-2 LLM evaluation with structured output schema (Score 0–100, recommendation, strengths, weaknesses, reasoning).
   - Includes automatic heuristic fallback when no external LLM API key is provisioned.
3. **`notifier.py`**:
   - Generates personalized candidate communication based on triage stage.
   - Outputs machine-readable disposition payloads for HR tracking.
4. **`agent.py`**:
   - The central autonomous controller managing state machine transitions, retries, structured JSON telemetry, and exception handling.
