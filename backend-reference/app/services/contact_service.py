"""
Contact Service Layer
=====================
Handles persistence of contact inquiries from `/contact`.
"""

import json
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contact import ContactInquiry
from app.models.audit import AuditEvent
from app.schemas.contact import ContactInquiryCreateDTO, ContactInquiryResponseDTO


class ContactService:
    @staticmethod
    async def create_inquiry(
        session: AsyncSession,
        dto: ContactInquiryCreateDTO,
        client_ip: str = None,
        user_agent: str = None,
    ) -> ContactInquiryResponseDTO:
        inquiry = ContactInquiry(
            full_name=dto.full_name,
            email=str(dto.email),
            company=dto.company,
            industry=dto.industry,
            message=dto.message,
            status="NEW",
        )
        session.add(inquiry)
        await session.flush()

        audit = AuditEvent(
            entity_type="CONTACT_INQUIRY",
            entity_id=inquiry.id,
            action="INQUIRY_CREATED",
            metadata_json=json.dumps({"email": str(dto.email), "company": dto.company}),
            ip_address=client_ip,
            user_agent=user_agent,
        )
        session.add(audit)

        return ContactInquiryResponseDTO(
            id=inquiry.id,
            status=inquiry.status,
            created_at=inquiry.created_at.isoformat(),
        )
