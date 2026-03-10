import pytest
from httpx import ASGITransport, AsyncClient

from server.app import app


@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_list_customers(client):
    resp = await client.get("/api/customers")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 2
    assert data[0]["id"] == "cust_001"
    assert "name" in data[0]


@pytest.mark.asyncio
async def test_list_products(client):
    resp = await client.get("/api/products")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 2
    assert data[0]["id"] == "prod_001"
    assert "title" in data[0]


@pytest.mark.asyncio
async def test_generate_missing_fields(client):
    resp = await client.post("/api/generate", json={})
    assert resp.status_code == 422
