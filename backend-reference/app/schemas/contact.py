"""
Contact Inquiry Schemas
=======================
Validates public inquiries from `/contact`.
"""

import re
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class ContactInquiryCreateDTO(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    company: Optional[str] = Field(None, max_length=200)
    industry: Optional[str] = Field(None, max_length=100)
    message: str = Field(..., min_length=10, max_length=5000)

    @field_validator("full_name")
    @classmethod
    def sanitize_full_name(cls, v: str) -> str:
        cleaned = " ".join(v.strip().split())
        if not re.match(r"^[a-zA-Z\s\-'\.]+$", cleaned):
            raise ValueError("Full name contains invalid characters")
        return cleaned

    @field_validator("company", "industry", "message")
    @classmethod
    def strip_html_tags(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        return re.sub(r"<[^>]+>", "", v).strip()


class ContactInquiryResponseDTO(BaseModel):
    id: str
    status: str
    created_at: str

    model_config = ConfigDict(from_attributes=True)
