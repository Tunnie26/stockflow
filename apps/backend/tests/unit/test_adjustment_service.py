from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from app.exceptions import AppError
from app.models.transaction import Transaction, TransactionType
from app.models.transaction_detail import TransactionDetail
from app.schemas.transaction import AdjustmentCreate
from app.services.adjustment_service import AdjustmentService


def make_adjustment_data(**overrides) -> AdjustmentCreate:
    data = {
        "warehouse_id": 1,
        "transaction_date": "2026-09-11",
        "reason": "Kiểm kê định kỳ",
        "details": [
            {
                "material_id": 1,
                "actual_quantity": Decimal("97"),
                "note": None,
            }
        ],
    }

    data.update(overrides)

    return AdjustmentCreate(**data)


def make_material(
    material_id: int = 1,
    warehouse_id: int = 1,
    is_active: bool = True,
):
    return MagicMock(
        id=material_id,
        warehouse_id=warehouse_id,
        is_active=is_active,
        sku="MAT-001",
        name="Test Material",
        unit="Cái",
        specification="Test specification",
    )


def test_create_adjustment_success():
    db = MagicMock()

    warehouse = MagicMock(
        id=1,
        is_active=True,
    )

    material = make_material()

    db.scalar.side_effect = [
        warehouse,
        None,
        material,
    ]

    inventory_service = MagicMock()

    service = AdjustmentService(db)
    service.inventory_service = inventory_service

    result = service.create(make_adjustment_data())

    assert isinstance(result, Transaction)
    assert result.transaction_type == TransactionType.ADJUSTMENT
    assert result.warehouse_id == 1
    assert result.note == "Kiểm kê định kỳ"

    added_details = [
        call.args[0]
        for call in db.add.call_args_list
        if isinstance(call.args[0], TransactionDetail)
    ]

    assert len(added_details) == 1

    detail = added_details[0]

    assert detail.material_id == 1
    assert detail.quantity == Decimal("97")
    assert detail.unit_price is None
    assert detail.total_amount is None

    inventory_service.apply_adjustment.assert_called_once_with(
        transaction_detail=detail,
        actual_quantity=Decimal("97"),
    )

    db.add.assert_any_call(result)
    db.flush.assert_called()


def test_create_adjustment_warehouse_not_found():
    db = MagicMock()
    db.scalar.return_value = None

    service = AdjustmentService(db)

    with pytest.raises(AppError) as exc_info:
        service.create(make_adjustment_data())

    assert exc_info.value.code == "WAREHOUSE_NOT_FOUND"

    db.add.assert_not_called()
    db.flush.assert_not_called()


def test_create_adjustment_warehouse_inactive():
    db = MagicMock()

    db.scalar.return_value = MagicMock(
        id=1,
        is_active=False,
    )

    service = AdjustmentService(db)

    with pytest.raises(AppError) as exc_info:
        service.create(make_adjustment_data())

    assert exc_info.value.code == "WAREHOUSE_INACTIVE"

    db.add.assert_not_called()
    db.flush.assert_not_called()


def test_create_adjustment_material_not_found():
    db = MagicMock()

    db.scalar.side_effect = [
        MagicMock(id=1, is_active=True),
        None,
        None,
    ]

    service = AdjustmentService(db)

    with pytest.raises(AppError) as exc_info:
        service.create(make_adjustment_data())

    assert exc_info.value.code == "MATERIAL_NOT_FOUND"


def test_create_adjustment_material_inactive():
    db = MagicMock()

    db.scalar.side_effect = [
        MagicMock(id=1, is_active=True),
        None,
        make_material(is_active=False),
    ]

    service = AdjustmentService(db)

    with pytest.raises(AppError) as exc_info:
        service.create(make_adjustment_data())

    assert exc_info.value.code == "MATERIAL_INACTIVE"


def test_create_adjustment_material_wrong_warehouse():
    db = MagicMock()

    db.scalar.side_effect = [
        MagicMock(id=1, is_active=True),
        None,
        make_material(warehouse_id=2),
    ]

    service = AdjustmentService(db)

    with pytest.raises(AppError) as exc_info:
        service.create(make_adjustment_data())

    assert exc_info.value.code == "MATERIAL_WRONG_WAREHOUSE"


def test_create_adjustment_multiple_details():
    db = MagicMock()

    warehouse = MagicMock(
        id=1,
        is_active=True,
    )

    material_1 = make_material(
        material_id=1,
    )

    material_2 = make_material(
        material_id=2,
    )

    db.scalar.side_effect = [
        warehouse,
        None,
        material_1,
        material_2,
    ]

    inventory_service = MagicMock()

    service = AdjustmentService(db)
    service.inventory_service = inventory_service

    data = make_adjustment_data(
        details=[
            {
                "material_id": 1,
                "actual_quantity": Decimal("97"),
            },
            {
                "material_id": 2,
                "actual_quantity": Decimal("105"),
            },
        ],
    )

    result = service.create(data)

    assert isinstance(result, Transaction)
    assert result.transaction_type == TransactionType.ADJUSTMENT
    assert result.warehouse_id == 1

    assert inventory_service.apply_adjustment.call_count == 2

    calls = inventory_service.apply_adjustment.call_args_list

    first_detail = calls[0].kwargs["transaction_detail"]
    first_quantity = calls[0].kwargs["actual_quantity"]

    second_detail = calls[1].kwargs["transaction_detail"]
    second_quantity = calls[1].kwargs["actual_quantity"]

    assert first_detail.material_id == 1
    assert first_detail.quantity == Decimal("97")
    assert first_quantity == Decimal("97")

    assert second_detail.material_id == 2
    assert second_detail.quantity == Decimal("105")
    assert second_quantity == Decimal("105")


def test_create_adjustment_generates_transaction_number():
    db = MagicMock()

    db.scalar.side_effect = [
        MagicMock(id=1, is_active=True),
        10,
        make_material(),
    ]

    service = AdjustmentService(db)
    service.inventory_service = MagicMock()

    result = service.create(make_adjustment_data())

    assert result.transaction_no == 11
