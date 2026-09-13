from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.exceptions import AppError
from app.schemas.transaction import TransactionType
from app.services.inventory_check_service import InventoryCheckService


def make_warehouse(
    warehouse_id=1,
    is_active=True,
):
    return SimpleNamespace(
        id=warehouse_id,
        is_active=is_active,
    )


def make_material(
    material_id,
    warehouse_id=1,
    sku=None,
    name=None,
    unit="Cái",
    is_active=True,
):
    return SimpleNamespace(
        id=material_id,
        warehouse_id=warehouse_id,
        sku=sku or f"SKU-{material_id}",
        name=name or f"Material {material_id}",
        unit=unit,
        specification="Test",
        is_active=is_active,
    )


def make_balance(
    material_id,
    quantity,
):
    return SimpleNamespace(
        material_id=material_id,
        quantity=Decimal(quantity),
    )


def make_payload(
    warehouse_id=1,
    details=None,
    note="Kiểm kê test",
):
    return SimpleNamespace(
        warehouse_id=warehouse_id,
        check_date="2026-09-12",
        note=note,
        details=details or [],
    )


def make_detail(
    material_id,
    actual_quantity,
    note=None,
):
    return SimpleNamespace(
        material_id=material_id,
        actual_quantity=Decimal(actual_quantity),
        note=note,
    )


def setup_service():
    db = MagicMock()
    service = InventoryCheckService(db)

    return db, service


def test_create_inventory_check_decreases_stock():
    db, service = setup_service()

    warehouse = make_warehouse()
    material = make_material(1)

    service._validate_warehouse = MagicMock(return_value=warehouse)
    service._validate_details = MagicMock(
        return_value=[
            (
                material,
                Decimal("97"),
                "Thiếu 3 cái",
            )
        ]
    )
    service._get_system_quantity = MagicMock(return_value=Decimal("100"))
    service._generate_check_no = MagicMock(return_value=1)
    service._generate_transaction_no = MagicMock(return_value=10)

    adjustment_transaction = SimpleNamespace(
        id=10,
    )

    service.inventory_service.apply_adjustment = MagicMock()

    service._create_adjustment_if_needed = MagicMock(
        return_value=adjustment_transaction
    )

    result = service.create(
        make_payload(
            details=[
                make_detail(
                    material_id=1,
                    actual_quantity="97",
                    note="Thiếu 3 cái",
                )
            ]
        )
    )

    assert result.check_no == 1
    assert result.warehouse_id == 1
    assert result.adjustment_transaction_id == 10

    detail = result.details[0]

    assert detail.material_id == 1
    assert detail.system_quantity == Decimal("100")
    assert detail.actual_quantity == Decimal("97")
    assert detail.difference == Decimal("-3")


def test_create_inventory_check_increases_stock():
    db, service = setup_service()

    warehouse = make_warehouse()
    material = make_material(1)

    service._validate_warehouse = MagicMock(return_value=warehouse)
    service._validate_details = MagicMock(
        return_value=[
            (
                material,
                Decimal("105"),
                None,
            )
        ]
    )
    service._get_system_quantity = MagicMock(return_value=Decimal("100"))
    service._generate_check_no = MagicMock(return_value=1)

    adjustment_transaction = SimpleNamespace(id=10)

    service._create_adjustment_if_needed = MagicMock(
        return_value=adjustment_transaction
    )

    result = service.create(
        make_payload(
            details=[
                make_detail(
                    material_id=1,
                    actual_quantity="105",
                )
            ]
        )
    )

    detail = result.details[0]

    assert detail.system_quantity == Decimal("100")
    assert detail.actual_quantity == Decimal("105")
    assert detail.difference == Decimal("5")
    assert result.adjustment_transaction_id == 10


def test_create_inventory_check_with_zero_difference_creates_no_adjustment():
    db, service = setup_service()

    warehouse = make_warehouse()
    material = make_material(1)

    service._validate_warehouse = MagicMock(return_value=warehouse)
    service._validate_details = MagicMock(
        return_value=[
            (
                material,
                Decimal("100"),
                None,
            )
        ]
    )
    service._get_system_quantity = MagicMock(return_value=Decimal("100"))
    service._generate_check_no = MagicMock(return_value=1)

    service._create_adjustment_if_needed = MagicMock(return_value=None)

    result = service.create(
        make_payload(
            details=[
                make_detail(
                    material_id=1,
                    actual_quantity="100",
                )
            ]
        )
    )

    detail = result.details[0]

    assert detail.system_quantity == Decimal("100")
    assert detail.actual_quantity == Decimal("100")
    assert detail.difference == Decimal("0")
    assert result.adjustment_transaction_id is None

    service._create_adjustment_if_needed.assert_called_once()


def test_create_inventory_check_supports_multiple_materials():
    db, service = setup_service()

    warehouse = make_warehouse()

    material_1 = make_material(1)
    material_2 = make_material(2)
    material_3 = make_material(3)

    service._validate_warehouse = MagicMock(return_value=warehouse)
    service._validate_details = MagicMock(
        return_value=[
            (material_1, Decimal("100"), None),
            (material_2, Decimal("197"), None),
            (material_3, Decimal("55"), None),
        ]
    )

    service._get_system_quantity = MagicMock(
        side_effect=[
            Decimal("100"),
            Decimal("200"),
            Decimal("50"),
        ]
    )

    service._generate_check_no = MagicMock(return_value=1)

    adjustment_transaction = SimpleNamespace(id=10)

    service._create_adjustment_if_needed = MagicMock(
        return_value=adjustment_transaction
    )

    result = service.create(
        make_payload(
            details=[
                make_detail(1, "100"),
                make_detail(2, "197"),
                make_detail(3, "55"),
            ]
        )
    )

    assert len(result.details) == 3

    assert result.details[0].difference == Decimal("0")
    assert result.details[1].difference == Decimal("-3")
    assert result.details[2].difference == Decimal("5")

    assert result.adjustment_transaction_id == 10

    service._get_system_quantity.assert_any_call(1)
    service._get_system_quantity.assert_any_call(2)
    service._get_system_quantity.assert_any_call(3)


def test_create_inventory_check_rejects_duplicate_material():
    db, service = setup_service()

    service._validate_warehouse = MagicMock(return_value=make_warehouse())

    with pytest.raises(AppError) as exc_info:
        service._validate_details(
            make_payload(
                details=[
                    make_detail(1, "100"),
                    make_detail(1, "95"),
                ]
            ),
            warehouse_id=1,
        )

    assert exc_info.value.code == "DUPLICATE_MATERIAL"


def test_create_inventory_check_reads_zero_for_missing_balance():
    db, service = setup_service()

    service.db.scalar.return_value = None

    result = service._get_system_quantity(999)

    assert result == Decimal("0")


def test_create_adjustment_if_needed_creates_adjustment_transaction():
    db = MagicMock()
    service = InventoryCheckService(db)

    check = SimpleNamespace(
        id=1,
        note="Kiểm kê thực tế",
    )

    check_detail = SimpleNamespace(
        material_id=1,
        actual_quantity=Decimal("97"),
        note="Thiếu 3 cái",
    )

    material = make_material(
        material_id=1,
        sku="SKU-001",
        name="Test Material",
        unit="Cái",
    )

    service._generate_transaction_no = MagicMock(return_value=10)

    db.scalar.return_value = material

    service.inventory_service.apply_adjustment = MagicMock()

    result = service._create_adjustment_if_needed(
        check=check,
        details=[
            (
                check_detail,
                Decimal("-3"),
            )
        ],
        warehouse_id=1,
        check_date="2026-09-12",
    )

    assert result is not None
    assert result.transaction_no == 10
    assert result.transaction_type == TransactionType.ADJUSTMENT
    assert result.warehouse_id == 1
    assert result.transaction_date == "2026-09-12"

    assert db.add.call_count >= 2

    service.inventory_service.apply_adjustment.assert_called_once()
