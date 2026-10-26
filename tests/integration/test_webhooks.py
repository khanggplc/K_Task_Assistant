import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_health_check_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_gmail_webhook_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/webhooks/gmail", json={"message": {"data": "eyJlbWFpbEFkZHJlc3MiOiAidGVzdEBleGFtcGxlLmNvbSIsICJoaXN0b3J5SWQiOiAiMTIzNCJ9"}})
        assert response.status_code == 200
        assert response.json() == {"status": "accepted"}
