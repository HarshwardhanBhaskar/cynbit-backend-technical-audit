"""
Candidate Evaluator Module
==========================
Implements two-tier candidate evaluation:
Tier 1: Deterministic rule verification (hard pass/fail gates).
Tier 2: LLM contextual scoring with deterministic heuristic fallback.
"""

from typing import List, Optional
from pydantic import BaseModel, Field

from src.extractor import CandidateProfileDTO


class GateCheckResult(BaseModel):
    passed: bool
    failure_reasons: List[str] = Field(default_factory=list)


class EvaluationScoreDTO(BaseModel):
    score: int = Field(..., ge=0, le=100)
    decision: str  # SHORTLIST, MANUAL_HR_REVIEW, REJECT
    evaluation_tier: str  # DETERMINISTIC_FALLBACK or LLM_ASSISTED
    strengths: List[str] = Field(default_factory=list)
    areas_for_review: List[str] = Field(default_factory=list)
    reasoning: str


class CandidateEvaluator:
    @staticmethod
    def check_deterministic_gates(profile: CandidateProfileDTO) -> GateCheckResult:
        """
        Executes strict deterministic gate checks.
        Zero LLM tokens used.
        """
        reasons = []

        # Gate 1: Mandatory Legal Consent
        if not profile.agreed_to_terms:
            reasons.append("Mandatory Terms & Conditions consent was not accepted.")

        # Gate 2: Email present
        if not profile.email or "@" not in profile.email:
            reasons.append("Valid candidate email address is required for communication.")

        # Gate 3: Graduation year window (Internship target: 2024 - 2028)
        if profile.graduation_year and (profile.graduation_year < 2023 or profile.graduation_year > 2028):
            reasons.append(
                f"Graduation year ({profile.graduation_year}) falls outside target internship cohort (2023-2028)."
            )

        # Gate 4: Non-empty narrative
        if profile.word_count < 10:
            reasons.append("Application narrative is insufficient to perform architectural evaluation.")

        return GateCheckResult(passed=len(reasons) == 0, failure_reasons=reasons)

    @staticmethod
    async def evaluate_contextual(
        profile: CandidateProfileDTO,
        api_key: Optional[str] = None,
    ) -> EvaluationScoreDTO:
        """
        Tier-2 evaluation: Evaluates candidate architectural depth.
        If an OpenAI API key is supplied, performs LLM evaluation.
        Otherwise, executes a high-fidelity deterministic heuristic fallback.
        """
        if api_key and not api_key.startswith("sk-placeholder"):
            try:
                import httpx
                headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                prompt = (
                    f"Evaluate this candidate for a Backend Developer Intern role at Cynbit Technologies.\n"
                    f"Candidate: {profile.full_name}\n"
                    f"Skills Detected: {', '.join(profile.detected_skills)}\n"
                    f"Narrative: {profile.narrative_text}\n"
                    f"Score 0-100 based on backend relevance (Python, PostgreSQL, Async, REST/GraphQL)."
                )
                payload = {
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "You are a Senior Backend Engineering Manager evaluating intern candidates. Return concise JSON with score, decision, strengths, and areas_for_review."},
                        {"role": "user", "content": prompt},
                    ],
                    "response_format": {"type": "json_object"},
                }
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                    if resp.status_code == 200:
                        import json
                        content = json.loads(resp.json()["choices"][0]["message"]["content"])
                        return EvaluationScoreDTO(
                            score=content.get("score", 70),
                            decision=content.get("decision", "MANUAL_HR_REVIEW"),
                            evaluation_tier="LLM_ASSISTED",
                            strengths=content.get("strengths", []),
                            areas_for_review=content.get("areas_for_review", []),
                            reasoning="Scored via OpenAI gpt-4o-mini model.",
                        )
            except Exception:
                pass  # Fallback to heuristic engine on network or auth failure

        # Deterministic Heuristic Scoring Engine
        score = 40
        strengths = []
        areas = []

        if profile.has_backend_stack:
            score += 30
            strengths.append("Matches primary Cynbit backend stack (Languages: Python/Node/Go + DB: Postgres/Mongo)")
        else:
            areas.append("Missing one or more core backend foundation technologies (Language + Database pairing)")

        # Bonus for architectural breadth
        advanced_keywords = {"oauth", "jwt", "docker", "graphql", "redis", "fastapi", "asyncio"}
        matched_advanced = set(profile.detected_skills) & advanced_keywords
        if matched_advanced:
            score += min(20, len(matched_advanced) * 5)
            strengths.append(f"Demonstrates familiarity with modern backend tools: {', '.join(sorted(matched_advanced))}")

        # Depth of narrative
        if profile.word_count >= 40:
            score += 10
            strengths.append("Provided detailed architectural statement demonstrating problem-solving mindset")
        else:
            areas.append("Statement is brief; recommend deep-dive technical interview on architecture")

        score = min(100, max(0, score))

        if score >= 75:
            decision = "SHORTLIST"
        elif score >= 50:
            decision = "MANUAL_HR_REVIEW"
        else:
            decision = "REJECT"

        return EvaluationScoreDTO(
            score=score,
            decision=decision,
            evaluation_tier="DETERMINISTIC_FALLBACK",
            strengths=strengths,
            areas_for_review=areas,
            reasoning="Evaluated using Cynbit talent acquisition technical competency rubric.",
        )
