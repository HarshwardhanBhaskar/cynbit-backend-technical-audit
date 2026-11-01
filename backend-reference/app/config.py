"""
Application Configuration
=========================
Environment-driven settings management powered by Pydantic Settings.
Adheres strictly to the 12-Factor App methodology.
"""

from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with defaults and environment overrides."""

    APP_NAME: str = "Cynbit Backend Reference API"
    APP_ENV: str = "development"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./cynbit_dev.db",
        description="Async SQLAlchemy database connection string",
    )
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_ECHO: bool = False

    # Security & Tokens
    SECRET_KEY: str = "dev-secret-key-please-replace-in-production-environments-32-chars"
    JWT_SECRET_KEY: str = "dev-jwt-secret-key-32-bytes-minimum-length-for-hmac-sha256"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: str = "https://cynbit.in,https://www.cynbit.in,http://localhost:3000,http://localhost:8000"

    # Rate Limiting (in-memory fallback window)
    RATE_LIMIT_GLOBAL_LIMIT: int = 60
    RATE_LIMIT_GLOBAL_WINDOW: int = 60
    RATE_LIMIT_APPLICATION_LIMIT: int = 5
    RATE_LIMIT_APPLICATION_WINDOW: int = 3600  # 1 hour

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()
