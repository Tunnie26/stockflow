from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_test_warehouse() -> int:
    code = f"WH-LOCATION-{uuid4().hex[:8].upper()}"

    response = client.post(
        "/api/v1/warehouses",
        json={
            "code": code,
            "name": "Location Test Warehouse",
        },
    )

    assert response.status_code == 200

    return response.json()["data"]["id"]


def test_create_location():
    warehouse_id = create_test_warehouse()

    response = client.post(
        "/api/v1/locations",
        json={
            "warehouse_id": warehouse_id,
            "code": "A01",
            "name": "Location A01",
            "description": "Test location",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "data" in body
    assert body["data"]["warehouse_id"] == warehouse_id
    assert body["data"]["code"] == "A01"
    assert body["data"]["name"] == "Location A01"
    assert body["data"]["description"] == "Test location"
    assert body["data"]["is_active"] is True


def test_create_location_warehouse_not_found():
    response = client.post(
        "/api/v1/locations",
        json={
            "warehouse_id": 999999,
            "code": "A01",
            "name": "Location A01",
        },
    )

    assert response.status_code == 400

    body = response.json()

    assert "error" in body
    assert body["error"]["code"] == "WAREHOUSE_NOT_FOUND"


def test_create_location_inactive_warehouse():
    warehouse_id = create_test_warehouse()

    response = client.patch(
        f"/api/v1/warehouses/{warehouse_id}",
        json={
            "is_active": False,
        },
    )

    assert response.status_code == 200

    response = client.post(
        "/api/v1/locations",
        json={
            "warehouse_id": warehouse_id,
            "code": "A02",
            "name": "Inactive Warehouse Location",
        },
    )

    assert response.status_code == 400

    body = response.json()

    assert "error" in body
    assert body["error"]["code"] == "WAREHOUSE_INACTIVE"


def test_create_location_duplicate_code():
    warehouse_id = create_test_warehouse()

    first_response = client.post(
        "/api/v1/locations",
        json={
            "warehouse_id": warehouse_id,
            "code": "DUP01",
            "name": "First Location",
        },
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/api/v1/locations",
        json={
            "warehouse_id": warehouse_id,
            "code": "DUP01",
            "name": "Second Location",
        },
    )

    assert second_response.status_code == 400

    body = second_response.json()

    assert "error" in body
    assert body["error"]["code"] == "LOCATION_CODE_ALREADY_EXISTS"


def test_list_locations():
    warehouse_id = create_test_warehouse()

    response = client.post(
        "/api/v1/locations",
        json={
            "warehouse_id": warehouse_id,
            "code": "LIST01",
            "name": "List Location",
        },
    )

    assert response.status_code == 200

    response = client.get("/api/v1/locations")

    assert response.status_code == 200

    body = response.json()

    assert "data" in body
    assert isinstance(body["data"], list)

    codes = [location["code"] for location in body["data"]]

    assert "LIST01" in codes


def test_get_location():
    warehouse_id = create_test_warehouse()

    create_response = client.post(
        "/api/v1/locations",
        json={
            "warehouse_id": warehouse_id,
            "code": "GET01",
            "name": "Get Location",
        },
    )

    assert create_response.status_code == 200

    location_id = create_response.json()["data"]["id"]

    response = client.get(f"/api/v1/locations/{location_id}")

    assert response.status_code == 200

    body = response.json()

    assert "data" in body
    assert body["data"]["id"] == location_id
    assert body["data"]["warehouse_id"] == warehouse_id
    assert body["data"]["code"] == "GET01"


def test_get_location_not_found():
    response = client.get("/api/v1/locations/999999")

    assert response.status_code == 400

    body = response.json()

    assert "error" in body
    assert body["error"]["code"] == "LOCATION_NOT_FOUND"


def test_update_location():
    warehouse_id = create_test_warehouse()

    create_response = client.post(
        "/api/v1/locations",
        json={
            "warehouse_id": warehouse_id,
            "code": "UPDATE01",
            "name": "Original Location",
        },
    )

    assert create_response.status_code == 200

    location_id = create_response.json()["data"]["id"]

    response = client.patch(
        f"/api/v1/locations/{location_id}",
        json={
            "name": "Updated Location",
            "description": "Updated description",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["data"]["id"] == location_id
    assert body["data"]["warehouse_id"] == warehouse_id
    assert body["data"]["code"] == "UPDATE01"
    assert body["data"]["name"] == "Updated Location"
    assert body["data"]["description"] == "Updated description"


def test_update_location_duplicate_code():
    warehouse_id = create_test_warehouse()

    first_response = client.post(
        "/api/v1/locations",
        json={
            "warehouse_id": warehouse_id,
            "code": "CODE01",
            "name": "First Location",
        },
    )

    second_response = client.post(
        "/api/v1/locations",
        json={
            "warehouse_id": warehouse_id,
            "code": "CODE02",
            "name": "Second Location",
        },
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    first_location_id = first_response.json()["data"]["id"]

    response = client.patch(
        f"/api/v1/locations/{first_location_id}",
        json={
            "code": "CODE02",
        },
    )

    assert response.status_code == 400

    body = response.json()

    assert "error" in body
    assert body["error"]["code"] == "LOCATION_CODE_ALREADY_EXISTS"


def test_update_location_not_found():
    response = client.patch(
        "/api/v1/locations/999999",
        json={
            "name": "Updated Location",
        },
    )

    assert response.status_code == 400

    body = response.json()

    assert "error" in body
    assert body["error"]["code"] == "LOCATION_NOT_FOUND"
