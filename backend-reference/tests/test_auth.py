"""
Authentication & JWT Tests
==========================
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_successful_login_returns_jwt_token(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/token",
        json={"email": "admin@cynbit.in", "password": "CynbitAdmin2026!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] > 0


@pytest.mark.asyncio
async def test_invalid_login_returns_401(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/token",
        json={"email": "admin@cynbit.in", "password": "WrongPassword!"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_access_protected_route_with_valid_jwt(client: AsyncClient):
    # 1. Login to get token
    login_res = await client.post(
        "/api/v1/auth/token",
        json={"email": "admin@cynbit.in", "password": "CynbitAdmin2026!"},
    )
    token = login_res.json()["access_token"]

    # 2. Submit an application to have a real ID
    from tests.test_applications import create_valid_application_payload
    app_res = await client.post("/api/v1/applications", json=create_valid_application_payload())
    app_id = app_res.json()["id"]

    # 3. Request with Bearer header
    headers = {"Authorization": f"Bearer {token}"}
    detail_res = await client.get(f"/api/v1/applications/{app_id}", headers=headers)
    assert detail_res.status_code == 200
    assert detail_res.json()["id"] == app_id
