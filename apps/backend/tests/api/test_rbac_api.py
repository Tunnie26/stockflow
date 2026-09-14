def test_no_token_cannot_read_materials(client):
    response = client.get("/api/v1/materials")

    assert response.status_code == 401


def test_viewer_can_read_materials(client, viewer_headers):
    response = client.get(
        "/api/v1/materials",
        headers=viewer_headers,
    )

    assert response.status_code == 200


def test_viewer_cannot_create_material(client, viewer_headers):
    response = client.post(
        "/api/v1/materials",
        json={
            "warehouse_id": 1,
            "category_id": 1,
            "sku": "RBAC-VIEWER-TEST",
            "name": "RBAC Viewer Test",
            "unit": "Cái",
            "minimum_stock": 0,
        },
        headers=viewer_headers,
    )

    assert response.status_code == 403


def test_user_can_create_material(client, user_headers):
    response = client.post(
        "/api/v1/materials",
        json={
            "warehouse_id": 1,
            "category_id": 1,
            "location_id": None,
            "customer_ids": [],
            "sku": "RBAC-USER-TEST",
            "name": "RBAC User Test",
            "unit": "Cái",
            "specification": "RBAC User Test",
            "minimum_stock": 0,
            "note": "",
        },
        headers=user_headers,
    )

    assert response.status_code == 201


def test_admin_can_create_material(client, admin_headers):
    response = client.post(
        "/api/v1/materials",
        json={
            "warehouse_id": 1,
            "category_id": 1,
            "location_id": None,
            "customer_ids": [],
            "sku": "RBAC-Admin-TEST",
            "name": "RBAC Admin Test",
            "unit": "Cái",
            "specification": "RBAC Admin Test",
            "minimum_stock": 0,
            "note": "",
        },
        headers=admin_headers,
    )

    assert response.status_code == 201


def test_viewer_cannot_create_adjustment(client, viewer_headers):
    response = client.post(
        "/api/v1/transactions/adjustments",
        json={
            "warehouse_id": 1,
            "transaction_date": "2026-09-14",
            "reason": "RBAC viewer test",
            "details": [
                {
                    "material_id": 1,
                    "actual_quantity": 10,
                }
            ],
        },
        headers=viewer_headers,
    )

    assert response.status_code == 403


def test_user_cannot_create_adjustment(client, user_headers):
    response = client.post(
        "/api/v1/transactions/adjustments",
        json={
            "warehouse_id": 1,
            "transaction_date": "2026-09-14",
            "reason": "RBAC user test",
            "details": [
                {
                    "material_id": 1,
                    "actual_quantity": 10,
                }
            ],
        },
        headers=user_headers,
    )

    assert response.status_code == 403


def test_viewer_cannot_create_inventory_check(
    client,
    viewer_headers,
):
    response = client.post(
        "/api/v1/inventory-checks",
        json={
            "warehouse_id": 1,
            "check_date": "2026-09-14",
            "details": [
                {
                    "material_id": 1,
                    "actual_quantity": 10,
                }
            ],
        },
        headers=viewer_headers,
    )

    assert response.status_code == 403


def test_user_can_create_inventory_check(
    client,
    user_headers,
):
    response = client.post(
        "/api/v1/inventory-checks",
        json={
            "warehouse_id": 999999,
            "check_date": "2026-09-14",
            "details": [
                {
                    "material_id": 999999,
                    "actual_quantity": 10,
                }
            ],
        },
        headers=user_headers,
    )

    assert response.status_code == 404


def test_viewer_cannot_create_transaction(
    client,
    viewer_headers,
):
    response = client.post(
        "/api/v1/transactions",
        json={
            "transaction_type": "INBOUND",
            "warehouse_id": 1,
            "supplier_id": 1,
            "transaction_date": "2026-09-14",
            "details": [
                {
                    "material_id": 1,
                    "quantity": 10,
                }
            ],
        },
        headers=viewer_headers,
    )

    assert response.status_code == 403


def test_user_can_create_transaction(
    client,
    user_headers,
):
    response = client.post(
        "/api/v1/transactions",
        json={
            "transaction_type": "INBOUND",
            "warehouse_id": 999999,
            "supplier_id": 999999,
            "transaction_date": "2026-09-14",
            "details": [
                {
                    "material_id": 999999,
                    "quantity": 10,
                }
            ],
        },
        headers=user_headers,
    )

    assert response.status_code == 404
