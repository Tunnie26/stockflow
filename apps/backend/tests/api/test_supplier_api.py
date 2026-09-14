from uuid import uuid4

from fastapi.testclient import TestClient


def unique_code(prefix: str = "NCC-TEST") -> str:
    return f"{prefix}-{uuid4().hex[:8].upper()}"


def create_test_supplier(
    client: TestClient,
    admin_headers: dict[str, str],
) -> int:
    response = client.post(
        "/api/v1/suppliers",
        json={
            "code": unique_code(),
            "name": "Test Supplier",
            "tax_code": "123456789",
            "phone": "0900000000",
            "email": "test@example.com",
            "address": "Da Lat",
            "contact_person": "Test Contact",
            "note": "Test supplier",
        },
        headers=admin_headers,
    )

    assert response.status_code == 200

    return response.json()["data"]["id"]


def test_create_supplier(client, admin_headers):
    code = unique_code()

    response = client.post(
        "/api/v1/suppliers",
        json={
            "code": code,
            "name": "Supplier A",
            "tax_code": "123456789",
            "phone": "0900000000",
            "email": "supplier@example.com",
            "address": "Da Lat",
            "contact_person": "Nguyen Van A",
            "note": "Test",
        },
        headers=admin_headers,
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert data["code"] == code
    assert data["name"] == "Supplier A"
    assert data["is_active"] is True


def test_create_supplier_duplicate_code(client, admin_headers):
    code = unique_code()

    payload = {
        "code": code,
        "name": "Supplier A",
    }

    first_response = client.post(
        "/api/v1/suppliers",
        json=payload,
        headers=admin_headers,
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/api/v1/suppliers",
        json=payload,
        headers=admin_headers,
    )

    assert second_response.status_code == 400
    assert second_response.json()["error"]["code"] == "SUPPLIER_CODE_ALREADY_EXISTS"


def test_list_suppliers(client, admin_headers):
    create_test_supplier(client, admin_headers)

    response = client.get(
        "/api/v1/suppliers",
        headers=admin_headers,
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_supplier(client, admin_headers):
    supplier_id = create_test_supplier(
        client,
        admin_headers,
    )

    response = client.get(
        f"/api/v1/suppliers/{supplier_id}",
        headers=admin_headers,
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert data["id"] == supplier_id


def test_get_supplier_not_found(client, admin_headers):
    response = client.get(
        "/api/v1/suppliers/999999999",
        headers=admin_headers,
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "SUPPLIER_NOT_FOUND"


def test_update_supplier(client, admin_headers):
    supplier_id = create_test_supplier(
        client,
        admin_headers,
    )

    response = client.patch(
        f"/api/v1/suppliers/{supplier_id}",
        json={
            "name": "Updated Supplier",
            "phone": "0911111111",
            "note": "Updated",
        },
        headers=admin_headers,
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert data["id"] == supplier_id
    assert data["name"] == "Updated Supplier"
    assert data["phone"] == "0911111111"
    assert data["note"] == "Updated"


def test_update_supplier_code_is_immutable(client, admin_headers):
    supplier_id = create_test_supplier(
        client,
        admin_headers,
    )

    response = client.patch(
        f"/api/v1/suppliers/{supplier_id}",
        json={
            "code": "NEW-CODE",
        },
        headers=admin_headers,
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert data["id"] == supplier_id
    assert data["code"] != "NEW-CODE"


def test_update_supplier_not_found(client, admin_headers):
    response = client.patch(
        "/api/v1/suppliers/999999999",
        json={
            "name": "Updated Supplier",
        },
        headers=admin_headers,
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "SUPPLIER_NOT_FOUND"
