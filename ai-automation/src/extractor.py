"""
Feature Extractor Module
========================
Extracts and normalizes structured applicant features, technical competencies,
and narrative signals from raw submission payloads.
"""

import re
from typing import Any, Dict, List, Set
from pydantic import BaseModel, Field


class CandidateProfileDTO(BaseModel):
    full_name: str
    email: str
    phone: str
    graduation_year: int
    agreed_to_terms: bool
    detected_skills: List[str] = Field(default_factory=list)
    has_backend_stack: bool = False
    narrative_text: str = ""
    word_count: int = 0


# Target competencies derived from Cynbit Backend Intern job posting
TARGET_SKILLS: Set[str] = {
    "python",
    "nodejs",
    "node.js",
    "go",
    "golang",
    "postgresql",
    "postgres",
    "mongodb",
    "oauth",
    "jwt",
    "fastapi",
    "docker",
    "rest",
    "graphql",
    "redis",
    "asyncio",
}


class CandidateExtractor:
    @staticmethod
    def extract(payload: Dict[str, Any]) -> CandidateProfileDTO:
        full_name = payload.get("full_name") or payload.get("applicant", {}).get("full_name", "Unknown")
        email = payload.get("email") or payload.get("applicant", {}).get("email", "")
        phone = payload.get("phone") or payload.get("applicant", {}).get("phone", "")
        terms = payload.get("agreed_to_terms")
        if terms is None:
            terms = payload.get("applicant", {}).get("agreed_to_terms", False)

        # Extract graduation year
        grad_year = payload.get("graduation_year", 0)
        if not grad_year and "qualifications" in payload and payload["qualifications"]:
            grad_year = payload["qualifications"][0].get("graduation_year", 0)

        # Combine text for signal extraction
        explicit_skills = payload.get("skills", [])
        statement = payload.get("application_statement", "")
        narrative = payload.get("architectural_narrative", "")
        combined_text = f"{' '.join(explicit_skills)} {statement} {narrative}".lower()

        # Tokenize and identify skills
        detected = []
        for skill in TARGET_SKILLS:
            # Word boundary regex check
            if re.search(r"\b" + re.escape(skill) + r"\b", combined_text):
                detected.append(skill)

        # Check for core backend competency
        core_languages = {"python", "nodejs", "node.js", "go", "golang"}
        core_databases = {"postgresql", "postgres", "mongodb"}
        has_backend = bool(set(detected) & core_languages) and bool(set(detected) & core_databases)

        words = len(combined_text.split())

        return CandidateProfileDTO(
            full_name=full_name,
            email=email,
            phone=phone,
            graduation_year=int(grad_year),
            agreed_to_terms=bool(terms),
            detected_skills=sorted(detected),
            has_backend_stack=has_backend,
            narrative_text=f"{statement} {narrative}".strip(),
            word_count=words,
        )
