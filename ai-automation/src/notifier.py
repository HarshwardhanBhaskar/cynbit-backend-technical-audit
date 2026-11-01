"""
Candidate Notification Generator
================================
Formats candidate communications and generates actionable HR notifications.
"""

from typing import Dict
from pydantic import BaseModel

from src.evaluator import EvaluationScoreDTO
from src.extractor import CandidateProfileDTO


class NotificationDTO(BaseModel):
    recipient_email: str
    recipient_name: str
    subject: str
    body_text: str
    action_required: str


class CandidateNotifier:
    @staticmethod
    def generate_notification(
        profile: CandidateProfileDTO,
        eval_result: EvaluationScoreDTO,
    ) -> NotificationDTO:
        if eval_result.decision == "SHORTLIST":
            subject = "Invitation to Technical Interview — Backend Developer Intern at Cynbit"
            action = "Schedule Technical Architecture Interview"
            body = (
                f"Dear {profile.full_name},\n\n"
                f"Thank you for applying for the Backend Developer Intern role at Cynbit Technologies.\n\n"
                f"Based on your profile and technical background in {', '.join(profile.detected_skills[:4])}, "
                f"our architectural talent review team has shortlisted your application!\n\n"
                f"Our recruitment team will be in touch within 24 hours to schedule your technical discussion.\n\n"
                f"Best regards,\nCynbit Technologies Talent Acquisition Team"
            )
        elif eval_result.decision == "MANUAL_HR_REVIEW":
            subject = "Application Status Update — Cynbit Technologies"
            action = "HR Specialist Review Required"
            body = (
                f"Dear {profile.full_name},\n\n"
                f"Your application for the Backend Developer Intern position has been received and "
                f"is currently undergoing secondary review by our engineering leads.\n\n"
                f"We appreciate your patience as we complete our evaluation.\n\n"
                f"Best regards,\nCynbit Technologies Talent Acquisition Team"
            )
        else:
            subject = "Regarding your application at Cynbit Technologies"
            action = "Archive Application Record"
            body = (
                f"Dear {profile.full_name},\n\n"
                f"Thank you for your interest in the Backend Developer Intern role at Cynbit Technologies.\n\n"
                f"At this stage, we have decided to advance other candidates whose current technical focus "
                f"more closely aligns with our immediate architectural stack requirements.\n\n"
                f"We wish you all the best in your career journey.\n\n"
                f"Sincerely,\nCynbit Technologies Talent Acquisition Team"
            )

        return NotificationDTO(
            recipient_email=profile.email,
            recipient_name=profile.full_name,
            subject=subject,
            body_text=body,
            action_required=action,
        )
