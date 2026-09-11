from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def unique_code(prefix: str = "CUS-TEST") -> str:
    return f"{prefix}-{uuid4().hex[:8].upper()}"


def create_test_customer() -> int:
    response = client.post(
        "/api/v1/customers",
        json={
            "code": unique_code(),
            "name": "Test Customer",
            "note": "Test customer",
        },
    )

    assert response.status_code == 200

    return response.json()["data"]["id"]


def test_customer_code_is_immutable():
    customer_id = create_test_customer()

    response = client.patch(
        f"/api/v1/customers/{customer_id}",
        json={
            "code": "NEW-CODE",
        },
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert data["id"] == customer_id
    assert data["code"] != "NEW-CODE"
