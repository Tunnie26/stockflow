from decimal import Decimal

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_adjustment_transaction():
    warehouse_response = client.post(
        "/api/v1/warehouses",
        json={
            "code": "WH-ADJ-010",
            "name": "Adjustment Warehouse",
            "address": None,
            "note": None,
        },
    )
    assert warehouse_response.status_code == 200

    warehouse_id = warehouse_response.json()["data"]["id"]

    category_response = client.post(
        "/api/v1/material-categories",
        json={
            "code": "CAT-ADJ-010",
            "name": "Adjustment Category",
            "description": None,
        },
    )
    assert category_response.status_code == 200

    category_id = category_response.json()["data"]["id"]

    material_response = client.post(
        "/api/v1/materials",
        json={
            "warehouse_id": warehouse_id,
            "category_id": category_id,
            "sku": "MAT-ADJ-010",
            "name": "Adjustment Material",
            "unit": "Cái",
            "specification": "Test",
            "minimum_stock": 0,
            "note": None,
        },
    )
    assert material_response.status_code == 201

    material_id = material_response.json()["data"]["id"]

    response = client.post(
        "/api/v1/transactions/adjustments",
        json={
            "warehouse_id": warehouse_id,
            "transaction_date": "2026-09-12",
            "reason": "Kiểm kê định kỳ",
            "details": [
                {
                    "material_id": material_id,
                    "actual_quantity": "97",
                    "note": "Thực tế kiểm kê",
                }
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert data["transaction_type"] == "ADJUSTMENT"
    assert data["warehouse_id"] == warehouse_id
    assert data["note"] == "Kiểm kê định kỳ"

    assert len(data["details"]) == 1

    detail = data["details"][0]

    assert detail["material_id"] == material_id
    assert Decimal(str(detail["quantity"])) == Decimal("97")
    assert detail["unit_price"] is None
    assert detail["total_amount"] is None


def test_create_adjustment_decreases_existing_stock():
    warehouse_response = client.post(
        "/api/v1/warehouses",
        json={
            "code": "WH-ADJ-011",
            "name": "Adjustment Existing Stock Warehouse",
            "address": None,
            "note": None,
        },
    )
    assert warehouse_response.status_code == 200

    warehouse_id = warehouse_response.json()["data"]["id"]

    category_response = client.post(
        "/api/v1/material-categories",
        json={
            "code": "CAT-ADJ-011",
            "name": "Adjustment Existing Stock Category",
            "description": None,
        },
    )
    assert category_response.status_code == 200

    category_id = category_response.json()["data"]["id"]

    material_response = client.post(
        "/api/v1/materials",
        json={
            "warehouse_id": warehouse_id,
            "category_id": category_id,
            "sku": "MAT-ADJ-011",
            "name": "Adjustment Existing Stock Material",
            "unit": "Cái",
            "specification": "Test",
            "minimum_stock": 0,
            "note": None,
        },
    )
    assert material_response.status_code == 201

    material_id = material_response.json()["data"]["id"]

    supplier_response = client.post(
        "/api/v1/suppliers",
        json={
            "code": "SUP-ADJ-011",
            "name": "Adjustment Supplier",
            "address": None,
            "phone": None,
            "email": None,
            "tax_code": None,
            "note": None,
        },
    )
    assert supplier_response.status_code == 200

    supplier_id = supplier_response.json()["data"]["id"]

    inbound_response = client.post(
        "/api/v1/transactions",
        json={
            "transaction_type": "INBOUND",
            "warehouse_id": warehouse_id,
            "supplier_id": supplier_id,
            "transaction_date": "2026-09-12",
            "details": [
                {
                    "material_id": material_id,
                    "quantity": "100",
                    "unit_price": "1000",
                    "note": None,
                }
            ],
        },
    )

    assert inbound_response.status_code == 200

    adjustment_response = client.post(
        "/api/v1/transactions/adjustments",
        json={
            "warehouse_id": warehouse_id,
            "transaction_date": "2026-09-12",
            "reason": "Kiểm kê thực tế",
            "details": [
                {
                    "material_id": material_id,
                    "actual_quantity": "97",
                    "note": "Thiếu 3 cái",
                }
            ],
        },
    )

    assert adjustment_response.status_code == 200

    data = adjustment_response.json()["data"]

    assert data["transaction_type"] == "ADJUSTMENT"
    assert data["warehouse_id"] == warehouse_id
    assert data["details"][0]["material_id"] == material_id
    assert Decimal(data["details"][0]["quantity"]) == Decimal("97")
