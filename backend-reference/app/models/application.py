"""
Application Submission Model
============================
Models role applications, status lifecycle, and candidate narratives.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ApplicationSubmission(Base):
    __tablename__ = "application_submissions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    applicant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("applicants.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    position_slug: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    resume_url: Mapped[str] = mapped_column(String(500), nullable=False)
    linkedin_url: Mapped[str] = mapped_column(String(500), nullable=True)
    github_url: Mapped[str] = mapped_column(String(500), nullable=True)
    application_statement: Mapped[str] = mapped_column(Text, nullable=False)
    architectural_narrative: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="PENDING", nullable=False, index=True)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    applicant: Mapped["Applicant"] = relationship("Applicant", back_populates="applications")
