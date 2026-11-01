"""
Applicant Model
===============
Represents candidate personal identification details collected from the
Cynbit Careers Application modal.
"""

import uuid
from datetime import date, datetime, timezone
from sqlalchemy import Boolean, Date, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Applicant(Base):
    __tablename__ = "applicants"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(254), nullable=False, unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    whatsapp: Mapped[str] = mapped_column(String(20), nullable=False)
    dob: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(30), nullable=False)
    agreed_to_terms: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    qualifications: Mapped[list["Qualification"]] = relationship(
        "Qualification",
        back_populates="applicant",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    applications: Mapped[list["ApplicationSubmission"]] = relationship(
        "ApplicationSubmission",
        back_populates="applicant",
        cascade="all, delete",
        lazy="selectin",
    )
