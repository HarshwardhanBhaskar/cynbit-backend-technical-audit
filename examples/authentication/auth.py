"""
Secure Password Hashing & JWT Authentication
=============================================
Reference implementation demonstrating:
- Password hashing with bcrypt
- JWT token creation and validation
- Token refresh flow
- Protected route decorator pattern

This is a RECOMMENDATION — not a claim about Cynbit's implementation.
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field

# --- Configuration (from environment variables) ---

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "CHANGE-ME-IN-PRODUCTION")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

if SECRET_KEY == "CHANGE-ME-IN-PRODUCTION":
    import warnings
    warnings.warn(
        "JWT_SECRET_KEY is using default value. Set a strong secret in production!",
        stacklevel=2,
    )


# --- Password Hashing ---

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,  # Cost factor — increase for higher security
)


def hash_password(plain_password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        plain_password: The plaintext password to hash.

    Returns:
        The bcrypt hash string.
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its bcrypt hash.

    Args:
        plain_password: The plaintext password to verify.
        hashed_password: The stored bcrypt hash.

    Returns:
        True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


# --- JWT Tokens ---

class TokenPayload(BaseModel):
    """JWT token payload."""
    sub: str  # Subject (user ID or email)
    role: str = "user"
    exp: Optional[datetime] = None
    iat: Optional[datetime] = None
    token_type: str = "access"


class TokenResponse(BaseModel):
    """Token response returned to the client."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(description="Access token expiry in seconds")


class LoginRequest(BaseModel):
    """Login request model."""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class RegisterRequest(BaseModel):
    """Registration request model."""
    email: EmailStr
    password: str = Field(..., min_length=12, max_length=128)
    full_name: str = Field(..., min_length=2, max_length=100)

    # Note: In production, add password strength validation


def create_access_token(
    subject: str,
    role: str = "user",
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create a JWT access token.

    Args:
        subject: User identifier (ID or email).
        role: User role for RBAC.
        expires_delta: Custom expiration time.

    Returns:
        Encoded JWT string.
    """
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    payload = {
        "sub": subject,
        "role": role,
        "exp": expire,
        "iat": now,
        "token_type": "access",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(subject: str) -> str:
    """
    Create a JWT refresh token (longer-lived).

    Args:
        subject: User identifier.

    Returns:
        Encoded JWT refresh token string.
    """
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    payload = {
        "sub": subject,
        "exp": expire,
        "iat": now,
        "token_type": "refresh",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> TokenPayload:
    """
    Decode and validate a JWT token.

    Args:
        token: The JWT string to decode.

    Returns:
        Validated TokenPayload.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenPayload(**payload)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


# --- Dependency: Get Current User ---

security_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> TokenPayload:
    """
    FastAPI dependency to extract and validate the current user from JWT.

    Usage:
        @app.get("/protected")
        async def protected_route(user: TokenPayload = Depends(get_current_user)):
            return {"user": user.sub}
    """
    token_data = decode_token(credentials.credentials)

    if token_data.token_type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    return token_data


def require_role(required_role: str):
    """
    Factory for role-based access control dependency.

    Usage:
        @app.get("/admin", dependencies=[Depends(require_role("admin"))])
        async def admin_route():
            return {"message": "Admin access granted"}
    """
    async def role_checker(
        user: TokenPayload = Depends(get_current_user),
    ) -> TokenPayload:
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required role: {required_role}",
            )
        return user
    return role_checker


# --- Example usage ---

if __name__ == "__main__":
    print("=== Password Hashing Demo ===")
    password = "SecureP@ssw0rd!2026"
    hashed = hash_password(password)
    print(f"Password: {password}")
    print(f"Hash:     {hashed}")
    print(f"Verify (correct):  {verify_password(password, hashed)}")
    print(f"Verify (wrong):    {verify_password('wrong', hashed)}")

    print("\n=== JWT Token Demo ===")
    access = create_access_token(subject="user@example.com", role="user")
    refresh = create_refresh_token(subject="user@example.com")
    print(f"Access Token:  {access[:50]}...")
    print(f"Refresh Token: {refresh[:50]}...")

    decoded = decode_token(access)
    print(f"Decoded sub:   {decoded.sub}")
    print(f"Decoded role:  {decoded.role}")
    print(f"Token type:    {decoded.token_type}")
