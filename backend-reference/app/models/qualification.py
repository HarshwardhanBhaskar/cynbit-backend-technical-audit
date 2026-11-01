"""
Qualification Model
===================
Models dynamic repeatable qualifications ("Add Another Qualification")
associated with an applicant.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Qualification(Base):
    __tablename__ = "qualifications"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    applicant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("applicants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    graduation_year: Mapped[int] = mapped_column(Integer, nullable=False)
    education_status: Mapped[str] = mapped_column(String(50), nullable=False)
    score_system: Mapped[str] = mapped_column(String(30), nullable=False)
    score_value: Mapped[float] = mapped_column(Float, nullable=False)
    institution_name: Mapped[str] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    applicant: Mapped["Applicant"] = relationship("Applicant", back_populates="qualifications")
