"""
AI Automation Workflow Tests
============================
Hermetic test suite verifying deterministic gates, feature extraction,
scoring logic, and notification generation.
"""

import sys
from pathlib import Path
import pytest

# Add parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent import CandidateScreeningAgent


@pytest.mark.asyncio
async def test_strong_candidate_shortlisted():
    agent = CandidateScreeningAgent()
    payload = {
        "full_name": "Harshwardhan Bhaskar",
        "email": "harshwardhan@example.com",
        "phone": "+919876543210",
        "graduation_year": 2025,
        "agreed_to_terms": True,
        "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "AsyncIO", "JWT"],
        "application_statement": "Passionate about backend performance, database indexing, and API security.",
        "architectural_narrative": "Designed scalable PostgreSQL schemas with async connection pooling and Redis rate limiting.",
    }

    report = await agent.process_candidate(payload)

    assert report.deterministic_passed is True
    assert report.overall_score >= 75
    assert report.decision == "SHORTLIST"
    assert "Invitation to Technical Interview" in report.notification.subject
    assert "postgresql" in report.detected_skills
    assert "python" in report.detected_skills


@pytest.mark.asyncio
async def test_unaccepted_terms_rejected_at_gate():
    agent = CandidateScreeningAgent()
    payload = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "+919876543210",
        "graduation_year": 2025,
        "agreed_to_terms": False,  # Gate failure!
        "skills": ["Python", "PostgreSQL"],
        "application_statement": "Hello Cynbit.",
    }

    report = await agent.process_candidate(payload)

    assert report.deterministic_passed is False
    assert report.decision == "REJECT"
    assert report.evaluation_tier == "DETERMINISTIC_GATE"
    assert any("Terms & Conditions" in r for r in report.failure_reasons)


@pytest.mark.asyncio
async def test_out_of_cohort_graduation_year_rejected():
    agent = CandidateScreeningAgent()
    payload = {
        "full_name": "Old Graduate",
        "email": "oldgrad@example.com",
        "phone": "+919876543210",
        "graduation_year": 2012,  # Way out of intern cohort
        "agreed_to_terms": True,
        "skills": ["Python"],
        "application_statement": "Senior developer looking for an internship.",
    }

    report = await agent.process_candidate(payload)

    assert report.deterministic_passed is False
    assert report.decision == "REJECT"
    assert any("cohort" in r.lower() for r in report.failure_reasons)


@pytest.mark.asyncio
async def test_partial_skills_triggers_manual_review():
    agent = CandidateScreeningAgent()
    payload = {
        "full_name": "Frontend Transitioner",
        "email": "transitioner@example.com",
        "phone": "+919876543210",
        "graduation_year": 2025,
        "agreed_to_terms": True,
        "skills": ["HTML", "CSS", "React"],  # Missing backend DB & Language pairing
        "application_statement": "Looking to transition from React to backend engineering.",
        "architectural_narrative": "Familiar with component hierarchies and API consumer patterns.",
    }

    report = await agent.process_candidate(payload)

    assert report.deterministic_passed is True
    assert report.decision in ("MANUAL_HR_REVIEW", "REJECT")
    assert report.notification.action_required in ("HR Specialist Review Required", "Archive Application Record")
