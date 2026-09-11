from unittest.mock import MagicMock

import pytest

from app.exceptions import AppError
from app.models.location import Location
from app.models.warehouse import Warehouse
from app.schemas.location import LocationCreate, LocationUpdate
from app.services.location import LocationService


def make_warehouse(
    warehouse_id: int = 1,
    code: str = "WH-TEST",
    name: str = "Test Warehouse",
    is_active: bool = True,
) -> Warehouse:
    return Warehouse(
        id=warehouse_id,
        code=code,
        name=name,
        is_active=is_active,
    )


def make_location(
    location_id: int = 1,
    warehouse_id: int = 1,
    code: str = "A01",
    name: str = "Location A01",
    description: str | None = None,
    is_active: bool = True,
) -> Location:
    return Location(
        id=location_id,
        warehouse_id=warehouse_id,
        code=code,
        name=name,
        description=description,
        is_active=is_active,
    )


def test_create_location_success():
    db = MagicMock()
    warehouse = make_warehouse()

    db.scalar.side_effect = [
        warehouse,
        None,
    ]

    service = LocationService(db)

    data = LocationCreate(
        warehouse_id=1,
        code="A01",
        name="Location A01",
    )

    result = service.create_location(data)

    assert result.warehouse_id == 1
    assert result.code == "A01"
    assert result.name == "Location A01"

    db.add.assert_called_once()
    db.flush.assert_called_once()


def test_create_location_warehouse_not_found():
    db = MagicMock()

    db.scalar.return_value = None

    service = LocationService(db)

    data = LocationCreate(
        warehouse_id=999,
        code="A01",
        name="Location A01",
    )

    with pytest.raises(AppError) as exc_info:
        service.create_location(data)

    assert exc_info.value.code == "WAREHOUSE_NOT_FOUND"
    db.add.assert_not_called()
    db.flush.assert_not_called()


def test_create_location_warehouse_inactive():
    db = MagicMock()

    db.scalar.return_value = make_warehouse(is_active=False)

    service = LocationService(db)

    data = LocationCreate(
        warehouse_id=1,
        code="A01",
        name="Location A01",
    )

    with pytest.raises(AppError) as exc_info:
        service.create_location(data)

    assert exc_info.value.code == "WAREHOUSE_INACTIVE"
    db.add.assert_not_called()
    db.flush.assert_not_called()


def test_create_location_duplicate_code():
    db = MagicMock()

    warehouse = make_warehouse()
    existing_location = make_location()

    db.scalar.side_effect = [
        warehouse,
        existing_location,
    ]

    service = LocationService(db)

    data = LocationCreate(
        warehouse_id=1,
        code="A01",
        name="Another Location",
    )

    with pytest.raises(AppError) as exc_info:
        service.create_location(data)

    assert exc_info.value.code == "LOCATION_CODE_ALREADY_EXISTS"
    db.add.assert_not_called()
    db.flush.assert_not_called()


def test_list_locations():
    db = MagicMock()

    locations = [
        make_location(location_id=1, code="A01"),
        make_location(location_id=2, code="A02"),
    ]

    db.scalars.return_value.all.return_value = locations

    service = LocationService(db)

    result = service.list_locations()

    assert result == locations


def test_get_location_success():
    db = MagicMock()

    location = make_location()
    db.scalar.return_value = location

    service = LocationService(db)

    result = service.get_location(1)

    assert result == location


def test_get_location_not_found():
    db = MagicMock()
    db.scalar.return_value = None

    service = LocationService(db)

    with pytest.raises(AppError) as exc_info:
        service.get_location(999)

    assert exc_info.value.code == "LOCATION_NOT_FOUND"


def test_update_location_success():
    db = MagicMock()

    location = make_location()
    db.scalar.return_value = None

    service = LocationService(db)

    data = LocationUpdate(
        name="Updated Location",
        description="Updated description",
    )

    # get_location() needs to return the existing location first,
    # then the duplicate-code query must return None.
    db.scalar.side_effect = [
        location,
        None,
    ]

    result = service.update_location(1, data)

    assert result.name == "Updated Location"
    assert result.description == "Updated description"

    db.flush.assert_called_once()


def test_update_location_code_duplicate():
    db = MagicMock()

    location = make_location(
        location_id=1,
        warehouse_id=1,
        code="A01",
    )

    duplicate_location = make_location(
        location_id=2,
        warehouse_id=1,
        code="A02",
    )

    db.scalar.side_effect = [
        location,
        duplicate_location,
    ]

    service = LocationService(db)

    data = LocationUpdate(
        code="A02",
    )

    with pytest.raises(AppError) as exc_info:
        service.update_location(1, data)

    assert exc_info.value.code == "LOCATION_CODE_ALREADY_EXISTS"
    db.flush.assert_not_called()


def test_update_location_not_found():
    db = MagicMock()
    db.scalar.return_value = None

    service = LocationService(db)

    data = LocationUpdate(
        name="Updated Location",
    )

    with pytest.raises(AppError) as exc_info:
        service.update_location(999, data)

    assert exc_info.value.code == "LOCATION_NOT_FOUND"
    db.flush.assert_not_called()
