# AI Automation Deliverable — Candidate Screening & Triage Agent

> **Assessment Track:** Autonomous AI Workflow Deliverable  
> **Target Process:** Cynbit Talent Acquisition Pipeline (`/careers/backend-developer-intern`)  
> **Status:** Implemented & Fully Tested  

---

## 1. Executive Summary

This deliverable provides an autonomous **AI Candidate Screening & Triage Agent** designed to automate the initial qualification review of prospective software engineers. 

To prevent LLM hallucinations on objective compliance criteria (e.g., terms consent, minimum age, cohort eligibility), the architecture separates evaluation into:
1. **Tier-1 Deterministic Hard Gates (Zero LLM Tokens):** Instant rule checks for legal consent, valid contact syntax, and graduation window.
2. **Tier-2 Contextual Architectural Scoring (LLM / Heuristic Engine):** Deep evaluation of technical competencies (PostgreSQL, Python, AsyncIO, REST/GraphQL, Docker, JWT) with structured JSON output and candidate notification drafting.

---

## 2. Directory Layout

```
ai-automation/
├── README.md               # Deliverable documentation & execution guide
├── architecture.md         # Visual architecture & deterministic vs LLM separation
├── workflow.md             # 5-stage lifecycle & failure/retry policies
├── requirements.txt        # Python dependencies
├── src/
│   ├── __init__.py
│   ├── agent.py            # Central workflow orchestrator (CandidateScreeningAgent)
│   ├── extractor.py        # Tokenizer & competency extractor
│   ├── evaluator.py        # Tier-1 hard gates & Tier-2 scoring engine
│   └── notifier.py         # Candidate & HR notification generator
└── tests/
    ├── __init__.py
    └── test_workflow.py    # Automated test suite (pytest)
```

---

## 3. Setup & Execution

### 3.1 Installation
```bash
cd ai-automation
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # Linux/macOS
pip install -r requirements.txt
```

### 3.2 Running the Automated Tests
```bash
pytest -v tests/test_workflow.py
```

### 3.3 Programmatic Usage Example
```python
import asyncio
from src.agent import CandidateScreeningAgent

async def main():
    agent = CandidateScreeningAgent()  # Or pass openai_api_key="sk-..."
    
    candidate_submission = {
        "full_name": "Harshwardhan Bhaskar",
        "email": "harshwardhan@example.com",
        "phone": "+919876543210",
        "graduation_year": 2025,
        "agreed_to_terms": True,
        "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "AsyncIO"],
        "application_statement": "Deeply interested in scalable backend architectures and API security.",
        "architectural_narrative": "Designed relational schemas with composite indexing, asyncpg connection pooling, and JWT with RBAC."
    }
    
    report = await agent.process_candidate(candidate_submission)
    print(f"Candidate: {report.candidate_name}")
    print(f"Decision:  {report.decision} (Score: {report.overall_score}/100)")
    print(f"Tier:      {report.evaluation_tier}")
    print(f"Action:    {report.notification.action_required}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 4. Key Strengths
- **Zero Hallucination on Compliance:** Legal consent and mandatory fields cannot be bypassed by clever prompting.
- **Resilient Fallback:** Works fully offline using the built-in deterministic heuristic rubric even if external LLM APIs are unreachable.
- **Production Telemetry:** Captures full execution metrics and timing in milliseconds.
