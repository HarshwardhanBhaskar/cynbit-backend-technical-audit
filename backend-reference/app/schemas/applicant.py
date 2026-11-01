"""
Applicant and Qualification Validation Schemas
===============================================
Pydantic v2 validation models for candidate identity and qualifications.
"""

import re
from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class GenderEnum(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
    PREFER_NOT_TO_SAY = "Prefer not to say"


class ScoreSystemEnum(str, Enum):
    CGPA_10 = "CGPA_10"
    CGPA_4 = "CGPA_4"
    PERCENTAGE_100 = "PERCENTAGE_100"


class QualificationCreateDTO(BaseModel):
    graduation_year: int = Field(..., ge=1980, le=2035, description="Year of graduation")
    education_status: str = Field(..., min_length=2, max_length=50)
    score_system: ScoreSystemEnum
    score_value: float = Field(..., ge=0.0)
    institution_name: Optional[str] = Field(None, max_length=200)

    @field_validator("score_value")
    @classmethod
    def validate_score_bounds(cls, v: float, info) -> float:
        score_sys = info.data.get("score_system")
        if score_sys == ScoreSystemEnum.CGPA_10 and v > 10.0:
            raise ValueError("Score value cannot exceed 10.0 when score system is CGPA_10")
        if score_sys == ScoreSystemEnum.CGPA_4 and v > 4.0:
            raise ValueError("Score value cannot exceed 4.0 when score system is CGPA_4")
        if score_sys == ScoreSystemEnum.PERCENTAGE_100 and v > 100.0:
            raise ValueError("Percentage cannot exceed 100.0")
        return round(v, 2)


class QualificationResponseDTO(QualificationCreateDTO):
    id: str
    created_at: str

    model_config = ConfigDict(from_attributes=True)


class ApplicantBaseDTO(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=8, max_length=20)
    whatsapp: str = Field(..., min_length=8, max_length=20)
    dob: date = Field(..., description="Date of birth")
    gender: GenderEnum
    agreed_to_terms: bool = Field(..., description="Must be true to agree to terms")

    @field_validator("full_name")
    @classmethod
    def sanitize_full_name(cls, v: str) -> str:
        cleaned = " ".join(v.strip().split())
        if not re.match(r"^[a-zA-Z\s\-'\.]+$", cleaned):
            raise ValueError("Full name contains invalid characters. Only letters, spaces, hyphens and dots allowed.")
        return cleaned

    @field_validator("phone", "whatsapp")
    @classmethod
    def validate_phone_number(cls, v: str) -> str:
        # Normalize: strip spaces, hyphens, brackets
        cleaned = re.sub(r"[\s\-\(\)]", "", v)
        if not re.match(r"^\+?[1-9]\d{7,14}$", cleaned):
            raise ValueError("Phone number must be a valid E.164 telephony format (8 to 15 digits)")
        return cleaned

    @field_validator("dob")
    @classmethod
    def validate_age_boundaries(cls, v: date) -> date:
        today = date.today()
        if v >= today:
            raise ValueError("Date of birth must be a past date")
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 16:
            raise ValueError(f"Candidate must be at least 16 years of age (calculated age: {age})")
        if age > 75:
            raise ValueError(f"Date of birth exceeds realistic boundary (calculated age: {age})")
        return v

    @field_validator("agreed_to_terms")
    @classmethod
    def require_terms_consent(cls, v: bool) -> bool:
        if not v:
            raise ValueError("You must agree to the Terms & Conditions to submit your application")
        return v
