from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_test_warehouse() -> int:
    code = f"WH-TRANSACTION-{uuid4().hex[:8].upper()}"

    response = client.post(
        "/api/v1/warehouses",
        json={
            "code": code,
            "name": "Transaction Test Warehouse",
        },
    )

    assert response.status_code == 200

    return response.json()["data"]["id"]


def create_test_category() -> int:
    code = f"CAT-{uuid4().hex[:8].upper()}"

    response = client.post(
        "/api/v1/material-categories",
        json={
            "code": code,
            "name": "Transaction Test Category",
        },
    )

    assert response.status_code == 200

    return response.json()["data"]["id"]


def create_test_material(
    warehouse_id: int,
    category_id: int,
) -> int:
    sku = f"MAT-{uuid4().hex[:8].upper()}"

    response = client.post(
        "/api/v1/materials",
        json={
            "warehouse_id": warehouse_id,
            "category_id": category_id,
            "location_id": None,
            "sku": sku,
            "name": "Transaction Test Material",
            "unit": "Cái",
            "specification": "Test specification",
            "minimum_stock": 0,
            "note": None,
        },
    )

    assert response.status_code == 201

    return response.json()["data"]["id"]


def create_test_supplier() -> int:
    code = f"NCC-TRANSACTION-{uuid4().hex[:8].upper()}"

    response = client.post(
        "/api/v1/suppliers",
        json={
            "code": code,
            "name": "Transaction Test Supplier",
        },
    )

    assert response.status_code == 200

    return response.json()["data"]["id"]


def test_create_inbound_transaction():
    warehouse_id = create_test_warehouse()
    category_id = create_test_category()
    material_id = create_test_material(
        warehouse_id,
        category_id,
    )
    supplier_id = create_test_supplier()

    response = client.post(
        "/api/v1/transactions",
        json={
            "transaction_type": "INBOUND",
            "warehouse_id": warehouse_id,
            "destination_warehouse_id": None,
            "supplier_id": supplier_id,
            "receiving_unit_id": None,
            "other_recipient": None,
            "transaction_date": "2026-09-11",
            "note": "Test inbound transaction",
            "details": [
                {
                    "material_id": material_id,
                    "quantity": 10,
                    "unit_price": 15000,
                    "note": "Test inbound detail",
                }
            ],
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "data" in body

    data = body["data"]

    assert data["transaction_type"] == "INBOUND"
    assert data["warehouse_id"] == warehouse_id
    assert data["supplier_id"] == supplier_id
    assert data["destination_warehouse_id"] is None

    assert len(data["details"]) == 1

    detail = data["details"][0]

    assert detail["material_id"] == material_id
    assert detail["quantity"] == "10.0000"
    assert detail["unit_price"] == "15000.00"
    assert detail["total_amount"] == "150000.00"


def test_create_outbound_transaction():
    warehouse_id = create_test_warehouse()
    category_id = create_test_category()
    material_id = create_test_material(
        warehouse_id,
        category_id,
    )
    supplier_id = create_test_supplier()

    inbound_response = client.post(
        "/api/v1/transactions",
        json={
            "transaction_type": "INBOUND",
            "warehouse_id": warehouse_id,
            "supplier_id": supplier_id,
            "transaction_date": "2026-09-11",
            "details": [
                {
                    "material_id": material_id,
                    "quantity": 10,
                }
            ],
        },
    )

    assert inbound_response.status_code == 200

    outbound_response = client.post(
        "/api/v1/transactions",
        json={
            "transaction_type": "OUTBOUND",
            "warehouse_id": warehouse_id,
            "receiving_unit_id": None,
            "other_recipient": "Test Recipient",
            "transaction_date": "2026-09-11",
            "details": [
                {
                    "material_id": material_id,
                    "quantity": 4,
                }
            ],
        },
    )

    assert outbound_response.status_code == 200

    data = outbound_response.json()["data"]

    assert data["transaction_type"] == "OUTBOUND"
    assert data["warehouse_id"] == warehouse_id
    assert len(data["details"]) == 1
    assert data["details"][0]["material_id"] == material_id
    assert data["details"][0]["quantity"] == "4.0000"


def test_create_transfer_transaction():
    source_warehouse_id = create_test_warehouse()
    destination_warehouse_id = create_test_warehouse()

    category_id = create_test_category()

    material_id = create_test_material(
        source_warehouse_id,
        category_id,
    )

    supplier_id = create_test_supplier()

    inbound_response = client.post(
        "/api/v1/transactions",
        json={
            "transaction_type": "INBOUND",
            "warehouse_id": source_warehouse_id,
            "supplier_id": supplier_id,
            "transaction_date": "2026-09-11",
            "details": [
                {
                    "material_id": material_id,
                    "quantity": 10,
                }
            ],
        },
    )

    assert inbound_response.status_code == 200

    transfer_response = client.post(
        "/api/v1/transactions",
        json={
            "transaction_type": "TRANSFER",
            "warehouse_id": source_warehouse_id,
            "destination_warehouse_id": destination_warehouse_id,
            "supplier_id": None,
            "receiving_unit_id": None,
            "other_recipient": None,
            "transaction_date": "2026-09-11",
            "note": "Test transfer transaction",
            "details": [
                {
                    "material_id": material_id,
                    "quantity": 4,
                }
            ],
        },
    )

    assert transfer_response.status_code == 200

    data = transfer_response.json()["data"]

    assert data["transaction_type"] == "TRANSFER"
    assert data["warehouse_id"] == source_warehouse_id
    assert data["destination_warehouse_id"] == destination_warehouse_id

    assert data["supplier_id"] is None
    assert data["receiving_unit_id"] is None
    assert data["other_recipient"] is None

    assert len(data["details"]) == 1

    detail = data["details"][0]

    assert detail["material_id"] == material_id
    assert detail["quantity"] == "4.0000"


def test_create_inbound_transaction_with_multiple_details():
    warehouse_id = create_test_warehouse()
    category_id = create_test_category()

    material_1_id = create_test_material(
        warehouse_id,
        category_id,
    )

    material_2_id = create_test_material(
        warehouse_id,
        category_id,
    )

    supplier_id = create_test_supplier()

    response = client.post(
        "/api/v1/transactions",
        json={
            "transaction_type": "INBOUND",
            "warehouse_id": warehouse_id,
            "supplier_id": supplier_id,
            "transaction_date": "2026-09-11",
            "note": "Multiple details test",
            "details": [
                {
                    "material_id": material_1_id,
                    "quantity": 10,
                    "unit_price": 10000,
                },
                {
                    "material_id": material_2_id,
                    "quantity": 20,
                    "unit_price": 20000,
                },
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert data["transaction_type"] == "INBOUND"
    assert data["warehouse_id"] == warehouse_id
    assert data["supplier_id"] == supplier_id

    assert len(data["details"]) == 2

    details = {detail["material_id"]: detail for detail in data["details"]}

    assert details[material_1_id]["quantity"] == "10.0000"
    assert details[material_1_id]["unit_price"] == "10000.00"
    assert details[material_1_id]["total_amount"] == "100000.00"

    assert details[material_2_id]["quantity"] == "20.0000"
    assert details[material_2_id]["unit_price"] == "20000.00"
    assert details[material_2_id]["total_amount"] == "400000.00"


def test_create_transaction_rolls_back_on_invalid_detail():
    warehouse_id = create_test_warehouse()
    other_warehouse_id = create_test_warehouse()
    category_id = create_test_category()

    valid_material_id = create_test_material(
        warehouse_id,
        category_id,
    )

    invalid_material_id = create_test_material(
        other_warehouse_id,
        category_id,
    )

    supplier_id = create_test_supplier()

    response = client.post(
        "/api/v1/transactions",
        json={
            "transaction_type": "INBOUND",
            "warehouse_id": warehouse_id,
            "supplier_id": supplier_id,
            "transaction_date": "2026-09-11",
            "note": "Rollback test",
            "details": [
                {
                    "material_id": valid_material_id,
                    "quantity": 10,
                },
                {
                    "material_id": invalid_material_id,
                    "quantity": 20,
                },
            ],
        },
    )

    assert response.status_code == 400

    body = response.json()

    assert "error" in body
