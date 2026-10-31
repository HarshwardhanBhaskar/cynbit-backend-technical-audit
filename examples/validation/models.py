"""
Pydantic Input Validation Examples
===================================
Reference implementation for server-side request validation.
These models demonstrate how to validate contact form inputs
and return structured error responses.

This is a RECOMMENDATION — not a claim about Cynbit's implementation.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


# --- Enums ---

class IndustryType(str, Enum):
    """Predefined industry categories for validated selection."""
    TECHNOLOGY = "technology"
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    EDUCATION = "education"
    ECOMMERCE = "ecommerce"
    MEDIA = "media"
    MANUFACTURING = "manufacturing"
    CONSULTING = "consulting"
    OTHER = "other"


# --- Request Models ---

class ContactFormRequest(BaseModel):
    """
    Validated contact form request model.

    Maps to the observed contact form fields on cynbit.in/contact:
    - Full Name (required)
    - Email Address (required)
    - Company (optional)
    - Industry (optional)
    - Your Message (required)
    """

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Full name of the person submitting the inquiry",
        examples=["Jane Doe"],
    )

    email: EmailStr = Field(
        ...,
        description="Valid email address for follow-up",
        examples=["jane.doe@example.com"],
    )

    company: Optional[str] = Field(
        None,
        max_length=200,
        description="Company name (optional)",
        examples=["Acme Corp"],
    )

    industry: Optional[IndustryType] = Field(
        None,
        description="Industry category (optional)",
        examples=["technology"],
    )

    message: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Inquiry message content",
        examples=["I'd like to discuss a potential project collaboration."],
    )

    @field_validator("full_name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Sanitize name: allow letters, spaces, hyphens, apostrophes only."""
        import re
        cleaned = v.strip()
        if not re.match(r"^[a-zA-Z\s\-'\.]+$", cleaned):
            raise ValueError(
                "Name may only contain letters, spaces, hyphens, and apostrophes"
            )
        return cleaned

    @field_validator("message")
    @classmethod
    def sanitize_message(cls, v: str) -> str:
        """Strip HTML tags from message to prevent stored XSS."""
        import re
        cleaned = re.sub(r"<[^>]+>", "", v)
        return cleaned.strip()

    @field_validator("company")
    @classmethod
    def sanitize_company(cls, v: Optional[str]) -> Optional[str]:
        """Strip HTML tags from company name."""
        if v is None:
            return v
        import re
        return re.sub(r"<[^>]+>", "", v).strip()


class JobApplicationRequest(BaseModel):
    """Example validated job application model."""

    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    position_slug: str = Field(..., min_length=1, max_length=200)
    cover_letter: Optional[str] = Field(None, max_length=10000)
    resume_url: Optional[str] = Field(None, max_length=500)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Basic phone number validation."""
        if v is None:
            return v
        import re
        cleaned = re.sub(r"[\s\-\(\)]", "", v)
        if not re.match(r"^\+?\d{7,15}$", cleaned):
            raise ValueError("Invalid phone number format")
        return cleaned


# --- Response Models ---

class ErrorDetail(BaseModel):
    """Individual field-level error."""
    field: str
    message: str


class ErrorResponse(BaseModel):
    """Structured error response — never exposes internals."""
    success: bool = False
    error: dict = Field(
        ...,
        examples=[{
            "code": "VALIDATION_ERROR",
            "message": "Invalid input provided",
            "details": [{"field": "email", "message": "Must be a valid email address"}],
        }],
    )


class ContactFormResponse(BaseModel):
    """Successful contact form submission response."""
    success: bool = True
    data: dict = Field(
        ...,
        examples=[{
            "inquiry_id": "inq_abc123",
            "message": "Your inquiry has been submitted successfully.",
            "estimated_response": "24 hours",
        }],
    )


# --- Example usage ---

if __name__ == "__main__":
    # Valid request
    try:
        valid = ContactFormRequest(
            full_name="Jane Doe",
            email="jane@example.com",
            company="Acme Corp",
            industry="technology",
            message="I'd like to discuss a web development project for our company.",
        )
        print(f"✅ Valid request: {valid.model_dump_json(indent=2)}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    print()

    # Invalid request — triggers validation errors
    try:
        invalid = ContactFormRequest(
            full_name="A",  # Too short
            email="not-an-email",  # Invalid format
            message="Hi",  # Too short
        )
    except Exception as e:
        print(f"✅ Caught validation error (expected):\n{e}")
