"""
AI Automation Agent Orchestrator
================================
Main autonomous agent orchestrating candidate ingestion, feature extraction,
two-tier deterministic & LLM evaluation, and notification generation.
"""

import json
import logging
import time
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

from src.evaluator import CandidateEvaluator, EvaluationScoreDTO, GateCheckResult
from src.extractor import CandidateExtractor, CandidateProfileDTO
from src.notifier import CandidateNotifier, NotificationDTO

logger = logging.getLogger("cynbit.ai_agent")


class TriageReportDTO(BaseModel):
    candidate_name: str
    email: str
    phone: str
    graduation_year: int
    detected_skills: list[str]
    deterministic_passed: bool
    failure_reasons: list[str] = Field(default_factory=list)
    overall_score: int
    decision: str
    evaluation_tier: str
    strengths: list[str] = Field(default_factory=list)
    areas_for_review: list[str] = Field(default_factory=list)
    notification: NotificationDTO
    processing_time_ms: float


class CandidateScreeningAgent:
    def __init__(self, openai_api_key: Optional[str] = None):
        self.api_key = openai_api_key

    async def process_candidate(self, raw_submission: Dict[str, Any]) -> TriageReportDTO:
        start_time = time.time()
        logger.info("Agent started candidate triage workflow")

        # Step 1: Feature Extraction
        profile = CandidateExtractor.extract(raw_submission)

        # Step 2: Deterministic Hard Gate Checks
        gate_result: GateCheckResult = CandidateEvaluator.check_deterministic_gates(profile)

        if not gate_result.passed:
            logger.warning(
                f"Candidate {profile.email} failed deterministic gates: {gate_result.failure_reasons}"
            )
            eval_score = EvaluationScoreDTO(
                score=15,
                decision="REJECT",
                evaluation_tier="DETERMINISTIC_GATE",
                strengths=[],
                areas_for_review=gate_result.failure_reasons,
                reasoning="Rejected at Tier-1 due to failure of mandatory deterministic gates.",
            )
        else:
            # Step 3: Contextual Architectural Scoring (LLM / Heuristic Fallback)
            eval_score = await CandidateEvaluator.evaluate_contextual(
                profile=profile,
                api_key=self.api_key,
            )
            logger.info(
                f"Candidate {profile.email} evaluated. Score: {eval_score.score}, Decision: {eval_score.decision}"
            )

        # Step 4: Generate Candidate & HR Notification
        notification: NotificationDTO = CandidateNotifier.generate_notification(
            profile=profile,
            eval_result=eval_score,
        )

        duration_ms = round((time.time() - start_time) * 1000, 2)

        return TriageReportDTO(
            candidate_name=profile.full_name,
            email=profile.email,
            phone=profile.phone,
            graduation_year=profile.graduation_year,
            detected_skills=profile.detected_skills,
            deterministic_passed=gate_result.passed,
            failure_reasons=gate_result.failure_reasons,
            overall_score=eval_score.score,
            decision=eval_score.decision,
            evaluation_tier=eval_score.evaluation_tier,
            strengths=eval_score.strengths,
            areas_for_review=eval_score.areas_for_review,
            notification=notification,
            processing_time_ms=duration_ms,
        )
