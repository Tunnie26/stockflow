from unittest.mock import MagicMock

import pytest

from app.exceptions import AppError
from app.models.warehouse import Warehouse
from app.schemas.warehouse import WarehouseCreate, WarehouseUpdate
from app.services.warehouse import WarehouseService


def test_create_warehouse_success():
    db = MagicMock()
    db.scalar.return_value = None

    service = WarehouseService(db)

    result = service.create_warehouse(
        WarehouseCreate(
            code="WH-TEST",
            name="Test Warehouse",
        )
    )

    assert isinstance(result, Warehouse)
    assert result.code == "WH-TEST"
    assert result.name == "Test Warehouse"

    db.add.assert_called_once_with(result)
    db.flush.assert_called_once()


def test_create_warehouse_duplicate_code():
    db = MagicMock()
    db.scalar.return_value = MagicMock(id=1)

    service = WarehouseService(db)

    with pytest.raises(AppError) as exc_info:
        service.create_warehouse(
            WarehouseCreate(
                code="WH-TEST",
                name="Test Warehouse",
            )
        )

    assert exc_info.value.code == "WAREHOUSE_CODE_ALREADY_EXISTS"
    db.add.assert_not_called()
    db.flush.assert_not_called()


def test_list_warehouses():
    db = MagicMock()

    warehouse_1 = Warehouse(
        id=1,
        code="WH-001",
        name="Warehouse 1",
        is_active=True,
    )
    warehouse_2 = Warehouse(
        id=2,
        code="WH-002",
        name="Warehouse 2",
        is_active=True,
    )

    db.scalars.return_value.all.return_value = [
        warehouse_1,
        warehouse_2,
    ]

    service = WarehouseService(db)

    result = service.list_warehouses()

    assert result == [warehouse_1, warehouse_2]
    db.scalars.assert_called_once()


def test_get_warehouse_success():
    db = MagicMock()

    warehouse = Warehouse(
        id=1,
        code="WH-001",
        name="Warehouse 1",
        is_active=True,
    )

    db.scalar.return_value = warehouse

    service = WarehouseService(db)

    result = service.get_warehouse(1)

    assert result is warehouse
    db.scalar.assert_called_once()


def test_get_warehouse_not_found():
    db = MagicMock()
    db.scalar.return_value = None

    service = WarehouseService(db)

    with pytest.raises(AppError) as exc_info:
        service.get_warehouse(999)

    assert exc_info.value.code == "WAREHOUSE_NOT_FOUND"


def test_update_warehouse_success():
    db = MagicMock()

    warehouse = Warehouse(
        id=1,
        code="WH-001",
        name="Old Name",
        is_active=True,
    )

    db.scalar.return_value = warehouse

    service = WarehouseService(db)

    result = service.update_warehouse(
        1,
        WarehouseUpdate(
            name="New Name",
        ),
    )

    assert result is warehouse
    assert result.code == "WH-001"
    assert result.name == "New Name"
    assert result.is_active is True

    db.flush.assert_called_once()


def test_update_warehouse_partial():
    db = MagicMock()

    warehouse = Warehouse(
        id=1,
        code="WH-001",
        name="Warehouse",
        is_active=True,
    )

    db.scalar.return_value = warehouse

    service = WarehouseService(db)

    result = service.update_warehouse(
        1,
        WarehouseUpdate(
            is_active=False,
        ),
    )

    assert result.name == "Warehouse"
    assert result.is_active is False

    db.flush.assert_called_once()


def test_update_warehouse_not_found():
    db = MagicMock()
    db.scalar.return_value = None

    service = WarehouseService(db)

    with pytest.raises(AppError) as exc_info:
        service.update_warehouse(
            999,
            WarehouseUpdate(name="New Name"),
        )

    assert exc_info.value.code == "WAREHOUSE_NOT_FOUND"
    db.flush.assert_not_called()