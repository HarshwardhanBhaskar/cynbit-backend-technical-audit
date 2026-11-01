"""
Contacts Router
==============
Handles public inquiry submissions from `/contact`.
"""

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.rate_limiter import contact_rate_limiter
from app.schemas.contact import ContactInquiryCreateDTO, ContactInquiryResponseDTO
from app.services.contact_service import ContactService

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.post("", response_model=ContactInquiryResponseDTO, status_code=status.HTTP_201_CREATED)
async def submit_contact_inquiry(
    request: Request,
    dto: ContactInquiryCreateDTO,
    session: AsyncSession = Depends(get_db),
):
    """
    Submits an inquiry from the public Contact page.
    Enforces per-IP sliding window rate limiting.
    """
    contact_rate_limiter.check(request)

    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    return await ContactService.create_inquiry(
        session=session,
        dto=dto,
        client_ip=client_ip,
        user_agent=user_agent,
    )
