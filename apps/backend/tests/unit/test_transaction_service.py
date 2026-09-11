from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from app.exceptions import AppError
from app.models.transaction import Transaction, TransactionType
from app.schemas.transaction import (
    TransactionCreate,
    TransactionDetailCreate,
)
from app.services.transaction_service import TransactionService


def make_detail(
    material_id: int = 1,
    quantity: str = "10",
    unit_price: str | None = None,
) -> TransactionDetailCreate:
    return TransactionDetailCreate(
        material_id=material_id,
        quantity=Decimal(quantity),
        unit_price=(Decimal(unit_price) if unit_price is not None else None),
    )


def make_payload(
    transaction_type: TransactionType,
    warehouse_id: int = 1,
    details: list[TransactionDetailCreate] | None = None,
    **overrides,
) -> TransactionCreate:
    data = {
        "transaction_type": transaction_type,
        "warehouse_id": warehouse_id,
        "destination_warehouse_id": None,
        "supplier_id": None,
        "receiving_unit_id": None,
        "other_recipient": None,
        "transaction_date": "2026-09-11",
        "note": None,
        "details": details or [make_detail()],
    }

    data.update(overrides)

    return TransactionCreate(**data)


def make_warehouse(
    warehouse_id: int = 1,
    is_active: bool = True,
) -> MagicMock:
    return MagicMock(
        id=warehouse_id,
        is_active=is_active,
    )


def make_supplier(
    supplier_id: int = 1,
    is_active: bool = True,
) -> MagicMock:
    return MagicMock(
        id=supplier_id,
        is_active=is_active,
    )


def make_receiving_unit(
    receiving_unit_id: int = 1,
    is_active: bool = True,
) -> MagicMock:
    return MagicMock(
        id=receiving_unit_id,
        is_active=is_active,
    )


def make_material(
    material_id: int = 1,
    warehouse_id: int = 1,
    is_active: bool = True,
) -> MagicMock:
    return MagicMock(
        id=material_id,
        warehouse_id=warehouse_id,
        sku="MAT-001",
        name="Test Material",
        unit="Cái",
        specification="Test specification",
        is_active=is_active,
    )


def test_create_inbound_success():
    db = MagicMock()

    warehouse = make_warehouse()
    supplier = make_supplier()
    material = make_material()

    db.scalar.side_effect = [
        warehouse,
        supplier,
        10,
        material,
    ]

    service = TransactionService(db)

    payload = make_payload(
        TransactionType.INBOUND,
        supplier_id=supplier.id,
        details=[
            make_detail(
                material_id=material.id,
                quantity="100",
                unit_price="12.50",
            )
        ],
    )

    result = service.create(payload)

    assert isinstance(result, Transaction)
    assert result.transaction_no == 11
    assert result.transaction_type == TransactionType.INBOUND
    assert result.warehouse_id == warehouse.id
    assert result.supplier_id == supplier.id
    assert result.destination_warehouse_id is None

    db.add.assert_called()
    assert db.add.call_count == 2
    assert db.flush.call_count == 2


def test_create_outbound_success():
    db = MagicMock()

    warehouse = make_warehouse()
    receiving_unit = make_receiving_unit()
    material = make_material()

    db.scalar.side_effect = [
        warehouse,
        receiving_unit,
        20,
        material,
    ]

    service = TransactionService(db)

    payload = make_payload(
        TransactionType.OUTBOUND,
        receiving_unit_id=receiving_unit.id,
        details=[
            make_detail(
                material_id=material.id,
                quantity="25",
            )
        ],
    )

    result = service.create(payload)

    assert isinstance(result, Transaction)
    assert result.transaction_no == 21
    assert result.transaction_type == TransactionType.OUTBOUND
    assert result.warehouse_id == warehouse.id
    assert result.receiving_unit_id == receiving_unit.id


def test_create_outbound_with_other_recipient_success():
    db = MagicMock()

    warehouse = make_warehouse()
    material = make_material()

    db.scalar.side_effect = [
        warehouse,
        30,
        material,
    ]

    service = TransactionService(db)

    payload = make_payload(
        TransactionType.OUTBOUND,
        other_recipient="External Partner",
        details=[
            make_detail(material_id=material.id),
        ],
    )

    result = service.create(payload)

    assert result.transaction_type == TransactionType.OUTBOUND
    assert result.other_recipient == "External Partner"


def test_create_transfer_success():
    db = MagicMock()

    source_warehouse = make_warehouse(1)
    destination_warehouse = make_warehouse(2)
    material = make_material(warehouse_id=1)

    db.scalar.side_effect = [
        source_warehouse,
        destination_warehouse,
        40,
        material,
    ]

    service = TransactionService(db)

    payload = make_payload(
        TransactionType.TRANSFER,
        warehouse_id=source_warehouse.id,
        destination_warehouse_id=destination_warehouse.id,
        details=[
            make_detail(
                material_id=material.id,
                quantity="20",
            )
        ],
    )

    result = service.create(payload)

    assert isinstance(result, Transaction)
    assert result.transaction_no == 41
    assert result.transaction_type == TransactionType.TRANSFER
    assert result.warehouse_id == source_warehouse.id
    assert result.destination_warehouse_id == destination_warehouse.id


def test_create_inbound_without_supplier():
    db = MagicMock()

    db.scalar.return_value = make_warehouse()

    service = TransactionService(db)

    payload = make_payload(TransactionType.INBOUND)

    with pytest.raises(AppError) as exc_info:
        service.create(payload)

    assert exc_info.value.code == "SUPPLIER_REQUIRED"
    db.add.assert_not_called()
    db.flush.assert_not_called()


def test_create_inbound_with_invalid_destination_warehouse():
    db = MagicMock()

    db.scalar.side_effect = [
        make_warehouse(),
        make_supplier(),
    ]

    service = TransactionService(db)

    payload = make_payload(
        TransactionType.INBOUND,
        supplier_id=1,
        destination_warehouse_id=2,
    )

    with pytest.raises(AppError) as exc_info:
        service.create(payload)

    assert exc_info.value.code == "INVALID_DESTINATION_WAREHOUSE"
    db.add.assert_not_called()


def test_create_inbound_with_receiving_unit():
    db = MagicMock()

    db.scalar.side_effect = [
        make_warehouse(),
        make_supplier(),
    ]

    service = TransactionService(db)

    payload = make_payload(
        TransactionType.INBOUND,
        supplier_id=1,
        receiving_unit_id=1,
    )

    with pytest.raises(AppError) as exc_info:
        service.create(payload)

    assert exc_info.value.code == "INVALID_RECEIVING_UNIT"


def test_create_outbound_without_recipient():
    db = MagicMock()

    db.scalar.return_value = make_warehouse()

    service = TransactionService(db)

    payload = make_payload(TransactionType.OUTBOUND)

    with pytest.raises(AppError) as exc_info:
        service.create(payload)

    assert exc_info.value.code == "RECIPIENT_REQUIRED"
    db.add.assert_not_called()
    db.flush.assert_not_called()


def test_create_outbound_with_supplier():
    db = MagicMock()

    db.scalar.return_value = make_warehouse()

    service = TransactionService(db)

    payload = make_payload(
        TransactionType.OUTBOUND,
        supplier_id=1,
        other_recipient="Partner",
    )

    with pytest.raises(AppError) as exc_info:
        service.create(payload)

    assert exc_info.value.code == "INVALID_SUPPLIER"


def test_create_outbound_with_destination_warehouse():
    db = MagicMock()

    db.scalar.return_value = make_warehouse()

    service = TransactionService(db)

    payload = make_payload(
        TransactionType.OUTBOUND,
        receiving_unit_id=1,
        destination_warehouse_id=2,
    )

    with pytest.raises(AppError) as exc_info:
        service.create(payload)

    assert exc_info.value.code == "INVALID_DESTINATION_WAREHOUSE"


def test_create_transfer_without_destination():
    db = MagicMock()

    db.scalar.return_value = make_warehouse()

    service = TransactionService(db)

    payload = make_payload(TransactionType.TRANSFER)

    with pytest.raises(AppError) as exc_info:
        service.create(payload)

    assert exc_info.value.code == "DESTINATION_WAREHOUSE_REQUIRED"
    db.add.assert_not_called()
    db.flush.assert_not_called()


def test_create_transfer_to_same_warehouse():
    db = MagicMock()

    db.scalar.return_value = make_warehouse(1)

    service = TransactionService(db)

    payload = make_payload(
        TransactionType.TRANSFER,
        warehouse_id=1,
        destination_warehouse_id=1,
    )

    with pytest.raises(AppError) as exc_info:
        service.create(payload)

    assert exc_info.value.code == "INVALID_TRANSFER"


def test_create_transfer_with_supplier():
    db = MagicMock()

    db.scalar.side_effect = [
        make_warehouse(1),
        make_warehouse(2),
    ]

    service = TransactionService(db)

    payload = make_payload(
        TransactionType.TRANSFER,
        destination_warehouse_id=2,
        supplier_id=1,
    )

    with pytest.raises(AppError) as exc_info:
        service.create(payload)

    assert exc_info.value.code == "INVALID_SUPPLIER"


def test_create_transfer_with_receiving_unit():
    db = MagicMock()

    db.scalar.side_effect = [
        make_warehouse(1),
        make_warehouse(2),
    ]

    service = TransactionService(db)

    payload = make_payload(
        TransactionType.TRANSFER,
        destination_warehouse_id=2,
        receiving_unit_id=1,
    )

    with pytest.raises(AppError) as exc_info:
        service.create(payload)

    assert exc_info.value.code == "INVALID_RECEIVING_UNIT"


def test_create_transfer_with_other_recipient():
    db = MagicMock()

    db.scalar.side_effect = [
        make_warehouse(1),
        make_warehouse(2),
    ]

    service = TransactionService(db)

    payload = make_payload(
        TransactionType.TRANSFER,
        destination_warehouse_id=2,
        other_recipient="Partner",
    )

    with pytest.raises(AppError) as exc_info:
        service.create(payload)

    assert exc_info.value.code == "INVALID_RECIPIENT"


def test_warehouse_not_found():
    db = MagicMock()
    db.scalar.return_value = None

    service = TransactionService(db)

    payload = make_payload(TransactionType.INBOUND)

    with pytest.raises(AppError) as exc_info:
        service.create(payload)

    assert exc_info.value.code == "WAREHOUSE_NOT_FOUND"
    assert exc_info.value.status_code == 404
    db.add.assert_not_called()


def test_warehouse_inactive():
    db = MagicMock()
    db.scalar.return_value = make_warehouse(
        is_active=False,
    )

    service = TransactionService(db)

    payload = make_payload(TransactionType.INBOUND)

    with pytest.raises(AppError) as exc_info:
        service.create(payload)

    assert exc_info.value.code == "WAREHOUSE_INACTIVE"
    db.add.assert_not_called()


def test_supplier_not_found():
    db = MagicMock()

    db.scalar.side_effect = [
        make_warehouse(),
        None,
    ]

    service = TransactionService(db)

    payload = make_payload(
        TransactionType.INBOUND,
        supplier_id=999,
    )

    with pytest.raises(AppError) as exc_info:
        service.create(payload)

    assert exc_info.value.code == "SUPPLIER_NOT_FOUND"
    assert exc_info.value.status_code == 404
    db.add.assert_not_called()


def test_supplier_inactive():
    db = MagicMock()

    db.scalar.side_effect = [
        make_warehouse(),
        make_supplier(is_active=False),
    ]

    service = TransactionService(db)

    payload = make_payload(
        TransactionType.INBOUND,
        supplier_id=1,
    )

    with pytest.raises(AppError) as exc_info:
        service.create(payload)

    assert exc_info.value.code == "SUPPLIER_INACTIVE"
    db.add.assert_not_called()


def test_receiving_unit_not_found():
    db = MagicMock()

    db.scalar.side_effect = [
        make_warehouse(),
        None,
    ]

    service = TransactionService(db)

    payload = make_payload(
        TransactionType.OUTBOUND,
        receiving_unit_id=999,
    )

    with pytest.raises(AppError) as exc_info:
        service.create(payload)

    assert exc_info.value.code == "RECEIVING_UNIT_NOT_FOUND"
    assert exc_info.value.status_code == 404
    db.add.assert_not_called()


def test_receiving_unit_inactive():
    db = MagicMock()

    db.scalar.side_effect = [
        make_warehouse(),
        make_receiving_unit(is_active=False),
    ]

    service = TransactionService(db)

    payload = make_payload(
        TransactionType.OUTBOUND,
        receiving_unit_id=1,
    )

    with pytest.raises(AppError) as exc_info:
        service.create(payload)

    assert exc_info.value.code == "RECEIVING_UNIT_INACTIVE"
    db.add.assert_not_called()


def test_material_not_found():
    db = MagicMock()

    db.scalar.side_effect = [
        make_warehouse(),
        make_supplier(),
        50,
        None,
    ]

    service = TransactionService(db)

    payload = make_payload(
        TransactionType.INBOUND,
        supplier_id=1,
    )

    with pytest.raises(AppError) as exc_info:
        service.create(payload)

    assert exc_info.value.code == "MATERIAL_NOT_FOUND"
    assert exc_info.value.status_code == 404


def test_material_inactive():
    db = MagicMock()

    db.scalar.side_effect = [
        make_warehouse(),
        make_supplier(),
        60,
        make_material(is_active=False),
    ]

    service = TransactionService(db)

    payload = make_payload(
        TransactionType.INBOUND,
        supplier_id=1,
    )

    with pytest.raises(AppError) as exc_info:
        service.create(payload)

    assert exc_info.value.code == "MATERIAL_INACTIVE"


def test_material_wrong_warehouse():
    db = MagicMock()

    db.scalar.side_effect = [
        make_warehouse(1),
        make_supplier(),
        70,
        make_material(warehouse_id=2),
    ]

    service = TransactionService(db)

    payload = make_payload(
        TransactionType.INBOUND,
        warehouse_id=1,
        supplier_id=1,
    )

    with pytest.raises(AppError) as exc_info:
        service.create(payload)

    assert exc_info.value.code == "MATERIAL_WRONG_WAREHOUSE"


def test_material_snapshot_and_total_amount():
    db = MagicMock()

    material = make_material()

    db.scalar.side_effect = [
        make_warehouse(),
        make_supplier(),
        80,
        material,
    ]

    service = TransactionService(db)

    payload = make_payload(
        TransactionType.INBOUND,
        supplier_id=1,
        details=[
            make_detail(
                material_id=material.id,
                quantity="8",
                unit_price="15.25",
            )
        ],
    )

    result = service.create(payload)

    added_objects = [call.args[0] for call in db.add.call_args_list]

    detail = next(
        obj for obj in added_objects if obj.__class__.__name__ == "TransactionDetail"
    )

    assert result.transaction_no == 81

    assert detail.material_id == material.id
    assert detail.sku_snapshot == material.sku
    assert detail.name_snapshot == material.name
    assert detail.unit_snapshot == material.unit
    assert detail.specification_snapshot == material.specification
    assert detail.quantity == Decimal("8")
    assert detail.unit_price == Decimal("15.25")
    assert detail.total_amount == Decimal("122.00")


def test_total_amount_is_none_without_unit_price():
    db = MagicMock()

    material = make_material()

    db.scalar.side_effect = [
        make_warehouse(),
        make_supplier(),
        90,
        material,
    ]

    service = TransactionService(db)

    payload = make_payload(
        TransactionType.INBOUND,
        supplier_id=1,
        details=[
            make_detail(
                material_id=material.id,
                quantity="10",
            )
        ],
    )

    service.create(payload)

    added_objects = [call.args[0] for call in db.add.call_args_list]

    detail = next(
        obj for obj in added_objects if obj.__class__.__name__ == "TransactionDetail"
    )

    assert detail.total_amount is None


def test_transaction_number_starts_from_one():
    db = MagicMock()

    db.scalar.side_effect = [
        make_warehouse(),
        make_supplier(),
        None,
        make_material(),
    ]

    service = TransactionService(db)

    payload = make_payload(
        TransactionType.INBOUND,
        supplier_id=1,
    )

    result = service.create(payload)

    assert result.transaction_no == 1


def test_adjustment_rejected_by_generic_transaction_service():
    db = MagicMock()

    db.scalar.return_value = make_warehouse()

    service = TransactionService(db)

    payload = make_payload(
        TransactionType.ADJUSTMENT,
    )

    with pytest.raises(AppError) as exc_info:
        service.create(payload)

    assert exc_info.value.code == "INVALID_TRANSACTION_TYPE"
    db.add.assert_not_called()
    db.flush.assert_not_called()
