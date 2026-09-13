from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_test_warehouse() -> int:
    code = f"WH-INVENTORY-CHECK-{uuid4().hex[:8].upper()}"

    response = client.post(
        "/api/v1/warehouses",
        json={
            "code": code,
            "name": "Inventory Check Test Warehouse",
        },
    )

    assert response.status_code == 200
    return response.json()["data"]["id"]


def create_test_category() -> int:
    code = f"CAT-INVENTORY-CHECK-{uuid4().hex[:8].upper()}"

    response = client.post(
        "/api/v1/material-categories",
        json={
            "code": code,
            "name": "Inventory Check Test Category",
        },
    )

    assert response.status_code == 200
    return response.json()["data"]["id"]


def create_test_material(
    warehouse_id: int,
    category_id: int,
) -> int:
    sku = f"MAT-INVENTORY-CHECK-{uuid4().hex[:8].upper()}"

    response = client.post(
        "/api/v1/materials",
        json={
            "warehouse_id": warehouse_id,
            "category_id": category_id,
            "location_id": None,
            "sku": sku,
            "name": "Inventory Check Test Material",
            "unit": "Cái",
            "specification": "Test specification",
            "minimum_stock": 0,
            "note": None,
        },
    )

    assert response.status_code == 201
    return response.json()["data"]["id"]


def create_test_supplier() -> int:
    code = f"NCC-INVENTORY-CHECK-{uuid4().hex[:8].upper()}"

    response = client.post(
        "/api/v1/suppliers",
        json={
            "code": code,
            "name": "Inventory Check Test Supplier",
        },
    )

    assert response.status_code == 200
    return response.json()["data"]["id"]


def create_initial_stock(
    warehouse_id: int,
    material_id: int,
    supplier_id: int,
    quantity: int,
) -> None:
    response = client.post(
        "/api/v1/transactions",
        json={
            "transaction_type": "INBOUND",
            "warehouse_id": warehouse_id,
            "supplier_id": supplier_id,
            "transaction_date": "2026-09-13",
            "details": [
                {
                    "material_id": material_id,
                    "quantity": quantity,
                }
            ],
        },
    )

    assert response.status_code == 200


def test_create_inventory_check_creates_adjustment_and_updates_stock():
    warehouse_id = create_test_warehouse()
    category_id = create_test_category()
    material_id = create_test_material(
        warehouse_id,
        category_id,
    )
    supplier_id = create_test_supplier()

    create_initial_stock(
        warehouse_id,
        material_id,
        supplier_id,
        10,
    )

    response = client.post(
        "/api/v1/inventory-checks",
        json={
            "warehouse_id": warehouse_id,
            "check_date": "2026-09-13",
            "note": "Inventory check integration test",
            "details": [
                {
                    "material_id": material_id,
                    "actual_quantity": 7,
                    "note": "Short by 3",
                }
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert data["warehouse_id"] == warehouse_id
    assert data["adjustment_transaction_id"] is not None

    detail = data["details"][0]

    assert detail["material_id"] == material_id
    assert detail["system_quantity"] == "10.0000"
    assert detail["actual_quantity"] == "7.0000"
    assert detail["difference"] == "-3.0000"

    inventory_response = client.get(f"/api/v1/inventory/{material_id}")

    assert inventory_response.status_code == 200

    inventory = inventory_response.json()["data"]

    assert inventory["quantity"] == "7.0000"

    movement_response = client.get(
        "/api/v1/movements",
        params={
            "material_id": material_id,
            "transaction_type": "ADJUSTMENT",
        },
    )

    assert movement_response.status_code == 200

    movements = movement_response.json()["data"]

    assert len(movements) == 1
    assert movements[0]["quantity"] == "-3.0000"
