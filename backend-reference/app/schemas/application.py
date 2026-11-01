"""
Application Submission Schemas
==============================
Validates candidate job applications, external links, and narrative fields.
"""

import re
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

from app.schemas.applicant import ApplicantBaseDTO, QualificationCreateDTO, QualificationResponseDTO


class ApplicationStatusEnum(str, Enum):
    PENDING = "PENDING"
    REVIEWING = "REVIEWING"
    SHORTLISTED = "SHORTLISTED"
    REJECTED = "REJECTED"
    OFFERED = "OFFERED"


class ApplicationCreateDTO(BaseModel):
    applicant: ApplicantBaseDTO
    qualifications: List[QualificationCreateDTO] = Field(..., min_length=1)
    position_slug: str = Field(..., min_length=2, max_length=100)
    resume_url: str = Field(..., description="HTTPS link to resume")
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    application_statement: str = Field(..., min_length=20, max_length=5000)
    architectural_narrative: Optional[str] = Field(None, max_length=5000)

    @field_validator("resume_url", "linkedin_url", "github_url")
    @classmethod
    def validate_secure_external_url(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        cleaned = v.strip()
        if not cleaned.startswith("https://"):
            raise ValueError("All external URLs must use secure HTTPS scheme")
        # SSRF Protection: Disallow local/private IP ranges
        private_ip_pattern = r"https?://(127\.|10\.|172\.(1[6-9]|2[0-9]|3[0-1])\.|192\.168\.|169\.254\.|localhost)"
        if re.search(private_ip_pattern, cleaned, re.IGNORECASE):
            raise ValueError("Private IP addresses and loopback hosts are not permitted")
        return cleaned

    @field_validator("application_statement", "architectural_narrative")
    @classmethod
    def sanitize_narrative_text(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        # Strip potential HTML tags
        cleaned = re.sub(r"<[^>]+>", "", v).strip()
        return cleaned


class ApplicationStatusUpdateDTO(BaseModel):
    status: ApplicationStatusEnum
    reviewer_notes: Optional[str] = Field(None, max_length=1000)


class ApplicationResponseDTO(BaseModel):
    id: str
    position_slug: str
    status: str
    submitted_at: str

    model_config = ConfigDict(from_attributes=True)
