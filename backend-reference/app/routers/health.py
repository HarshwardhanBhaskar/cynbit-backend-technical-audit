"""
Health Check Router
===================
Liveness and readiness probes for container orchestration (Kubernetes / Docker).
"""

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", status_code=status.HTTP_200_OK)
async def health_check(session: AsyncSession = Depends(get_db)):
    """
    Checks service liveness and database query connectivity.
    """
    try:
        await session.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "service": "cynbit-backend-reference",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": db_status,
    }
