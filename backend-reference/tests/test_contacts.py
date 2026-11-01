"""
Contacts Endpoint Tests
=======================
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_valid_contact_inquiry_returns_201(client: AsyncClient):
    payload = {
        "full_name": "Alice Smith",
        "email": "alice.smith@enterprise.com",
        "company": "Acme Technologies",
        "industry": "Fintech",
        "message": "We would like to discuss an architectural engineering consulting engagement.",
    }
    response = await client.post("/api/v1/contacts", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["status"] == "NEW"
    assert "created_at" in data


@pytest.mark.asyncio
async def test_empty_contact_payload_returns_422(client: AsyncClient):
    response = await client.post("/api/v1/contacts", json={})
    assert response.status_code == 422
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "VALIDATION_ERROR"


@pytest.mark.asyncio
async def test_invalid_contact_email_returns_422(client: AsyncClient):
    payload = {
        "full_name": "Bob Jones",
        "email": "not-an-email-address",
        "message": "Hello, testing invalid email validation.",
    }
    response = await client.post("/api/v1/contacts", json=payload)
    assert response.status_code == 422
