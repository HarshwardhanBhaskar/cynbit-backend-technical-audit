"""
Authentication Router & Dependencies
====================================
JWT Bearer token generation, password verification via native bcrypt, and RBAC guards.
"""

from datetime import datetime, timedelta, timezone
from typing import Callable
import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.config import settings
from app.middleware.rate_limiter import auth_rate_limiter
from app.schemas.auth import LoginCredentialsDTO, TokenPayloadDTO, TokenResponseDTO

router = APIRouter(prefix="/auth", tags=["Authentication"])

security_scheme = HTTPBearer()


def hash_password(plain: str) -> str:
    """Hash password using direct bcrypt (avoids legacy passlib incompatibility)."""
    pwd_bytes = plain.encode("utf-8")[:72]
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """Verify password against bcrypt hash."""
    pwd_bytes = plain.encode("utf-8")[:72]
    return bcrypt.checkpw(pwd_bytes, hashed.encode("utf-8"))


# Seed user records for demonstration
DEMO_USERS = {
    "admin@cynbit.in": {
        "password_hash": hash_password("CynbitAdmin2026!"),
        "role": "admin",
    },
    "reviewer@cynbit.in": {
        "password_hash": hash_password("ReviewerPass2026!"),
        "role": "reviewer",
    },
}


def create_access_token(sub: str, role: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": sub,
        "role": role,
        "exp": int(expires.timestamp()),
        "iat": int(datetime.now(timezone.utc).timestamp()),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> TokenPayloadDTO:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return TokenPayloadDTO(sub=payload["sub"], role=payload.get("role", "user"))
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials or token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_role(required_role: str) -> Callable:
    async def role_dependency(user: TokenPayloadDTO = Depends(get_current_user)) -> TokenPayloadDTO:
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Forbidden: '{required_role}' authorization required",
            )
        return user
    return role_dependency


@router.post("/token", response_model=TokenResponseDTO)
async def login(credentials: LoginCredentialsDTO):
    user = DEMO_USERS.get(credentials.email)
    if not user or not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(sub=credentials.email, role=user["role"])
    return TokenResponseDTO(
        access_token=token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
