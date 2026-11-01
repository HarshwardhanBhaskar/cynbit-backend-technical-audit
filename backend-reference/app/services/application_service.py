"""
Application Service Layer
=========================
Orchestrates business logic, database transactions, applicant de-duplication,
qualifications mapping, and audit trail creation.
"""

import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.applicant import Applicant
from app.models.qualification import Qualification
from app.models.application import ApplicationSubmission
from app.models.audit import AuditEvent
from app.schemas.application import ApplicationCreateDTO, ApplicationResponseDTO, ApplicationStatusUpdateDTO


class ApplicationService:
    @staticmethod
    async def submit_application(
        session: AsyncSession,
        dto: ApplicationCreateDTO,
        client_ip: str = None,
        user_agent: str = None,
    ) -> ApplicationResponseDTO:
        # 1. Lookup or create Applicant by unique email
        query = select(Applicant).where(Applicant.email == str(dto.applicant.email))
        result = await session.execute(query)
        applicant = result.scalar_one_or_none()

        if applicant is None:
            applicant = Applicant(
                full_name=dto.applicant.full_name,
                email=str(dto.applicant.email),
                phone=dto.applicant.phone,
                whatsapp=dto.applicant.whatsapp,
                dob=dto.applicant.dob,
                gender=dto.applicant.gender.value,
                agreed_to_terms=dto.applicant.agreed_to_terms,
            )
            session.add(applicant)
            await session.flush()  # Generates applicant.id
        else:
            # Update existing applicant profile details
            applicant.full_name = dto.applicant.full_name
            applicant.phone = dto.applicant.phone
            applicant.whatsapp = dto.applicant.whatsapp
            applicant.dob = dto.applicant.dob
            applicant.gender = dto.applicant.gender.value
            applicant.agreed_to_terms = dto.applicant.agreed_to_terms

        # 2. Add Qualifications
        for q in dto.qualifications:
            qualification = Qualification(
                applicant_id=applicant.id,
                graduation_year=q.graduation_year,
                education_status=q.education_status,
                score_system=q.score_system.value,
                score_value=q.score_value,
                institution_name=q.institution_name,
            )
            session.add(qualification)

        # 3. Create Application Submission
        submission = ApplicationSubmission(
            applicant_id=applicant.id,
            position_slug=dto.position_slug,
            resume_url=dto.resume_url,
            linkedin_url=dto.linkedin_url,
            github_url=dto.github_url,
            application_statement=dto.application_statement,
            architectural_narrative=dto.architectural_narrative,
            status="PENDING",
        )
        session.add(submission)
        await session.flush()

        # 4. Record Audit Event
        audit_event = AuditEvent(
            entity_type="APPLICATION",
            entity_id=submission.id,
            action="APPLICATION_SUBMITTED",
            metadata_json=json.dumps({
                "position_slug": dto.position_slug,
                "email": str(dto.applicant.email),
                "qualifications_count": len(dto.qualifications),
            }),
            ip_address=client_ip,
            user_agent=user_agent,
        )
        session.add(audit_event)

        return ApplicationResponseDTO(
            id=submission.id,
            position_slug=submission.position_slug,
            status=submission.status,
            submitted_at=submission.submitted_at.isoformat(),
        )

    @staticmethod
    async def get_application_by_id(
        session: AsyncSession, application_id: str
    ) -> ApplicationSubmission:
        query = select(ApplicationSubmission).where(ApplicationSubmission.id == application_id)
        result = await session.execute(query)
        submission = result.scalar_one_or_none()
        if not submission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Application with ID {application_id} not found",
            )
        return submission

    @staticmethod
    async def update_status(
        session: AsyncSession,
        application_id: str,
        dto: ApplicationStatusUpdateDTO,
        reviewer: str = "admin",
    ) -> ApplicationResponseDTO:
        submission = await ApplicationService.get_application_by_id(session, application_id)
        submission.status = dto.status.value

        audit_event = AuditEvent(
            entity_type="APPLICATION",
            entity_id=submission.id,
            action=f"STATUS_UPDATED_TO_{dto.status.value}",
            metadata_json=json.dumps({
                "reviewer": reviewer,
                "notes": dto.reviewer_notes,
            }),
        )
        session.add(audit_event)

        return ApplicationResponseDTO(
            id=submission.id,
            position_slug=submission.position_slug,
            status=submission.status,
            submitted_at=submission.submitted_at.isoformat(),
        )
