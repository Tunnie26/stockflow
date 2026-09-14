from uuid import uuid4

from fastapi.testclient import TestClient


def unique_code(prefix: str = "RU-TEST") -> str:
    return f"{prefix}-{uuid4().hex[:8].upper()}"


def create_test_receiving_unit(
    client: TestClient,
    admin_headers: dict[str, str],
) -> int:
    response = client.post(
        "/api/v1/receiving-units",
        json={
            "code": unique_code(),
            "name": "Test Receiving Unit",
        },
        headers=admin_headers,
    )

    assert response.status_code == 200

    return response.json()["data"]["id"]


def test_create_receiving_unit(client, admin_headers):
    code = unique_code()

    response = client.post(
        "/api/v1/receiving-units",
        json={
            "code": code,
            "name": "Receiving Unit A",
        },
        headers=admin_headers,
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert data["code"] == code
    assert data["name"] == "Receiving Unit A"
    assert data["is_active"] is True


def test_create_receiving_unit_duplicate_code(client, admin_headers):
    code = unique_code()

    payload = {
        "code": code,
        "name": "Receiving Unit A",
    }

    first_response = client.post(
        "/api/v1/receiving-units",
        json=payload,
        headers=admin_headers,
    )

    second_response = client.post(
        "/api/v1/receiving-units",
        json=payload,
        headers=admin_headers,
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert (
        second_response.json()["error"]["code"] == "RECEIVING_UNIT_CODE_ALREADY_EXISTS"
    )


def test_list_receiving_units(client, admin_headers):
    create_test_receiving_unit(
        client,
        admin_headers,
    )

    response = client.get(
        "/api/v1/receiving-units",
        headers=admin_headers,
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_receiving_unit(client, admin_headers):
    receiving_unit_id = create_test_receiving_unit(
        client,
        admin_headers,
    )

    response = client.get(
        f"/api/v1/receiving-units/{receiving_unit_id}",
        headers=admin_headers,
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert data["id"] == receiving_unit_id


def test_get_receiving_unit_not_found(client, admin_headers):
    response = client.get(
        "/api/v1/receiving-units/999999999",
        headers=admin_headers,
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "RECEIVING_UNIT_NOT_FOUND"


def test_update_receiving_unit(client, admin_headers):
    receiving_unit_id = create_test_receiving_unit(
        client,
        admin_headers,
    )

    response = client.patch(
        f"/api/v1/receiving-units/{receiving_unit_id}",
        json={
            "name": "Updated Receiving Unit",
        },
        headers=admin_headers,
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert data["id"] == receiving_unit_id
    assert data["name"] == "Updated Receiving Unit"


def test_update_receiving_unit_not_found(client, admin_headers):
    response = client.patch(
        "/api/v1/receiving-units/999999999",
        json={
            "name": "Updated Receiving Unit",
        },
        headers=admin_headers,
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "RECEIVING_UNIT_NOT_FOUND"


def test_receiving_unit_code_is_immutable(
    client,
    admin_headers,
):
    receiving_unit_id = create_test_receiving_unit(
        client,
        admin_headers,
    )

    response = client.patch(
        f"/api/v1/receiving-units/{receiving_unit_id}",
        json={
            "code": "NEW-CODE",
        },
        headers=admin_headers,
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert data["id"] == receiving_unit_id
    assert data["code"] != "NEW-CODE"
