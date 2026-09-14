from uuid import uuid4

from fastapi.testclient import TestClient


def unique_code(prefix: str = "CUS-TEST") -> str:
    return f"{prefix}-{uuid4().hex[:8].upper()}"


def create_test_customer(
    client: TestClient,
    admin_headers: dict[str, str],
) -> int:
    response = client.post(
        "/api/v1/customers",
        json={
            "code": unique_code(),
            "name": "Test Customer",
            "note": "Test customer",
        },
        headers=admin_headers,
    )

    assert response.status_code == 200

    return response.json()["data"]["id"]


def test_customer_code_is_immutable(
    client,
    admin_headers,
):
    customer_id = create_test_customer(
        client,
        admin_headers,
    )

    response = client.patch(
        f"/api/v1/customers/{customer_id}",
        json={
            "code": "NEW-CODE",
        },
        headers=admin_headers,
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert data["id"] == customer_id
    assert data["code"] != "NEW-CODE"
