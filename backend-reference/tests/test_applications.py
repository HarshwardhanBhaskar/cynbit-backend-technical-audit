"""
Applications Endpoint & Validation Tests
========================================
Validates server-side validation rules, boundary conditions, and transactional persistence.
"""

import pytest
from httpx import AsyncClient


def create_valid_application_payload():
    return {
        "applicant": {
            "full_name": "Harshwardhan Bhaskar",
            "email": "harshwardhan@example.com",
            "phone": "+919876543210",
            "whatsapp": "+919876543210",
            "dob": "2002-05-15",
            "gender": "Male",
            "agreed_to_terms": True,
        },
        "qualifications": [
            {
                "graduation_year": 2025,
                "education_status": "Pursuing",
                "score_system": "CGPA_10",
                "score_value": 8.75,
                "institution_name": "BIT Mesra",
            }
        ],
        "position_slug": "backend-developer-intern",
        "resume_url": "https://example.com/resumes/harshwardhan_resume.pdf",
        "linkedin_url": "https://linkedin.com/in/harshwardhan-bhaskar",
        "github_url": "https://github.com/HarshwardhanBhaskar",
        "application_statement": "I am deeply passionate about architecting distributed, secure backend services and API gateways.",
        "architectural_narrative": "Experienced in designing PostgreSQL schemas with connection pooling and async event loops.",
    }


@pytest.mark.asyncio
async def test_valid_application_submission_returns_201(client: AsyncClient):
    payload = create_valid_application_payload()
    response = await client.post("/api/v1/applications", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["position_slug"] == "backend-developer-intern"
    assert data["status"] == "PENDING"
    assert "submitted_at" in data


@pytest.mark.asyncio
async def test_empty_application_payload_returns_422(client: AsyncClient):
    response = await client.post("/api/v1/applications", json={})
    assert response.status_code == 422
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "VALIDATION_ERROR"


@pytest.mark.asyncio
async def test_invalid_phone_format_returns_422(client: AsyncClient):
    payload = create_valid_application_payload()
    payload["applicant"]["phone"] = "abcdefg123"  # Non-numeric telephony string
    response = await client.post("/api/v1/applications", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["success"] is False
    assert any("phone" in str(err["field"]) for err in data["error"]["details"])


@pytest.mark.asyncio
async def test_future_dob_returns_422(client: AsyncClient):
    payload = create_valid_application_payload()
    payload["applicant"]["dob"] = "2040-01-01"  # Future date
    response = await client.post("/api/v1/applications", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert any("dob" in str(err["field"]) for err in data["error"]["details"])


@pytest.mark.asyncio
async def test_unaccepted_terms_returns_422(client: AsyncClient):
    payload = create_valid_application_payload()
    payload["applicant"]["agreed_to_terms"] = False
    response = await client.post("/api/v1/applications", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert any("agreed_to_terms" in str(err["field"]) for err in data["error"]["details"])


@pytest.mark.asyncio
async def test_insecure_http_resume_url_returns_422(client: AsyncClient):
    payload = create_valid_application_payload()
    payload["resume_url"] = "http://insecure-host.com/resume.pdf"  # HTTP instead of HTTPS
    response = await client.post("/api/v1/applications", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_multiple_qualifications_persisted(client: AsyncClient):
    payload = create_valid_application_payload()
    payload["applicant"]["email"] = "multiqual@example.com"
    payload["qualifications"].append({
        "graduation_year": 2021,
        "education_status": "Completed",
        "score_system": "PERCENTAGE_100",
        "score_value": 92.4,
        "institution_name": "High School",
    })
    response = await client.post("/api/v1/applications", json=payload)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_application_unauthorized_without_jwt(client: AsyncClient):
    response = await client.get("/api/v1/applications/some-fake-id")
    # Missing Authorization header
    assert response.status_code in (401, 403)
