"""
Applications Router
===================
API routes managing candidate submissions, status transitions, and retrieval.
"""

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.rate_limiter import application_rate_limiter
from app.routers.auth import get_current_user, require_role
from app.schemas.auth import TokenPayloadDTO
from app.schemas.application import (
    ApplicationCreateDTO,
    ApplicationResponseDTO,
    ApplicationStatusUpdateDTO,
)
from app.services.application_service import ApplicationService

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post("", response_model=ApplicationResponseDTO, status_code=status.HTTP_201_CREATED)
async def submit_application(
    request: Request,
    dto: ApplicationCreateDTO,
    session: AsyncSession = Depends(get_db),
):
    """
    Submits a career application with applicant personal details and qualifications list.
    Enforces per-IP sliding window rate limiting.
    """
    application_rate_limiter.check(request)

    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    result = await ApplicationService.submit_application(
        session=session,
        dto=dto,
        client_ip=client_ip,
        user_agent=user_agent,
    )
    return result


@router.get("/{application_id}", response_model=ApplicationResponseDTO)
async def get_application(
    application_id: str,
    session: AsyncSession = Depends(get_db),
    current_user: TokenPayloadDTO = Depends(get_current_user),
):
    """
    Retrieves application details. Requires authenticated JWT session.
    """
    submission = await ApplicationService.get_application_by_id(session, application_id)
    return ApplicationResponseDTO(
        id=submission.id,
        position_slug=submission.position_slug,
        status=submission.status,
        submitted_at=submission.submitted_at.isoformat(),
    )


@router.patch("/{application_id}/status", response_model=ApplicationResponseDTO)
async def update_application_status(
    application_id: str,
    dto: ApplicationStatusUpdateDTO,
    session: AsyncSession = Depends(get_db),
    admin_user: TokenPayloadDTO = Depends(require_role("admin")),
):
    """
    Updates the candidate hiring stage. Restricted to administrator credentials.
    """
    return await ApplicationService.update_status(
        session=session,
        application_id=application_id,
        dto=dto,
        reviewer=admin_user.sub,
    )
