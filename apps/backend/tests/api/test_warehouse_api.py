def test_create_warehouse(client, admin_headers):
    response = client.post(
        "/api/v1/warehouses",
        json={
            "code": "WH-TEST-001",
            "name": "Test Warehouse",
        },
        headers=admin_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert "data" in body
    assert body["data"]["code"] == "WH-TEST-001"
    assert body["data"]["name"] == "Test Warehouse"
    assert body["data"]["is_active"] is True


def test_create_warehouse_duplicate_code(client, admin_headers):
    client.post(
        "/api/v1/warehouses",
        json={
            "code": "WH-TEST-DUP",
            "name": "First Warehouse",
        },
        headers=admin_headers,
    )

    response = client.post(
        "/api/v1/warehouses",
        json={
            "code": "WH-TEST-DUP",
            "name": "Second Warehouse",
        },
        headers=admin_headers,
    )

    assert response.status_code == 400

    body = response.json()

    assert "error" in body
    assert body["error"]["code"] == "WAREHOUSE_CODE_ALREADY_EXISTS"


def test_list_warehouses(client, admin_headers):
    client.post(
        "/api/v1/warehouses",
        json={
            "code": "WH-TEST-LIST",
            "name": "List Test Warehouse",
        },
        headers=admin_headers,
    )

    response = client.get(
        "/api/v1/warehouses",
        headers=admin_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert "data" in body
    assert isinstance(body["data"], list)

    codes = [warehouse["code"] for warehouse in body["data"]]

    assert "WH-TEST-LIST" in codes


def test_get_warehouse(client, admin_headers):
    create_response = client.post(
        "/api/v1/warehouses",
        json={
            "code": "WH-TEST-GET",
            "name": "Get Test Warehouse",
        },
        headers=admin_headers,
    )

    warehouse_id = create_response.json()["data"]["id"]

    response = client.get(
        f"/api/v1/warehouses/{warehouse_id}",
        headers=admin_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert "data" in body
    assert body["data"]["id"] == warehouse_id
    assert body["data"]["code"] == "WH-TEST-GET"
    assert body["data"]["name"] == "Get Test Warehouse"


def test_get_warehouse_not_found(client, admin_headers):
    response = client.get(
        "/api/v1/warehouses/999999",
        headers=admin_headers,
    )

    assert response.status_code == 400

    body = response.json()

    assert "error" in body
    assert body["error"]["code"] == "WAREHOUSE_NOT_FOUND"


def test_update_warehouse(client, admin_headers):
    create_response = client.post(
        "/api/v1/warehouses",
        json={
            "code": "WH-TEST-UPDATE",
            "name": "Original Name",
        },
        headers=admin_headers,
    )

    warehouse_id = create_response.json()["data"]["id"]

    response = client.patch(
        f"/api/v1/warehouses/{warehouse_id}",
        json={
            "name": "Updated Name",
        },
        headers=admin_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert "data" in body
    assert body["data"]["id"] == warehouse_id
    assert body["data"]["code"] == "WH-TEST-UPDATE"
    assert body["data"]["name"] == "Updated Name"


def test_partial_update_warehouse(client, admin_headers):
    create_response = client.post(
        "/api/v1/warehouses",
        json={
            "code": "WH-TEST-PARTIAL",
            "name": "Original Name",
        },
        headers=admin_headers,
    )

    warehouse_id = create_response.json()["data"]["id"]

    response = client.patch(
        f"/api/v1/warehouses/{warehouse_id}",
        json={
            "is_active": False,
        },
        headers=admin_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["data"]["code"] == "WH-TEST-PARTIAL"
    assert body["data"]["name"] == "Original Name"
    assert body["data"]["is_active"] is False


def test_update_warehouse_not_found(client, admin_headers):
    response = client.patch(
        "/api/v1/warehouses/999999",
        json={
            "name": "Updated Name",
        },
        headers=admin_headers,
    )

    assert response.status_code == 400

    body = response.json()

    assert "error" in body
    assert body["error"]["code"] == "WAREHOUSE_NOT_FOUND"
