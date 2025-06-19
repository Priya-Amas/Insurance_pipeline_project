import json
import pytest
from scripts.api.insurance_api import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Insurance API is running" in response.data

def test_get_insurance_empty(client):
    response = client.get("/insurance")
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == []

def test_post_insurance_valid(client):
    payload = {
        "customer_name": "Test User",
        "premium_amount": 10000,
        "status": "Active"
    }
    response = client.post("/insurance", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["customer_name"] == "Test User"
    assert data["premium_amount"] == 10000
    assert data["status"] == "Active"
    assert "policy_id" in data
    assert "issued_date" in data

def test_post_insurance_missing_field(client):
    response = client.post("/insurance", json={})
    assert response.status_code == 201
    data = response.get_json()
    assert data["customer_name"] == "Unknown"
    assert data["premium_amount"] == 0
