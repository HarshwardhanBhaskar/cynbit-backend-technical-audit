"""
Authentication Schemas
======================
Schemas for login credentials and JWT token exchange.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class TokenResponseDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class LoginCredentialsDTO(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class TokenPayloadDTO(BaseModel):
    sub: str
    role: str = "user"
    exp: Optional[int] = None
