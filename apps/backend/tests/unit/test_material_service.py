from unittest.mock import MagicMock

import pytest

from app.exceptions import AppError
from app.models.material import Material
from app.schemas.material import MaterialCreate, MaterialUpdate
from app.services.material import MaterialService


def make_material_data(**overrides) -> MaterialCreate:
    data = {
        "warehouse_id": 1,
        "category_id": 1,
        "location_id": None,
        "sku": "MAT-001",
        "name": "Test Material",
        "unit": "Cái",
        "specification": "Test specification",
        "minimum_stock": 0,
        "note": None,
    }
    data.update(overrides)
    return MaterialCreate(**data)


def test_create_material_success():
    db = MagicMock()

    warehouse = MagicMock(id=1, is_active=True)
    category = MagicMock(id=1, is_active=True)

    db.scalar.side_effect = [
        warehouse,
        category,
        None,
    ]

    service = MaterialService(db)

    result = service.create_material(make_material_data())

    assert isinstance(result, Material)
    assert result.warehouse_id == 1
    assert result.category_id == 1
    assert result.sku == "MAT-001"
    assert result.name == "Test Material"
    assert result.unit == "Cái"

    db.add.assert_called_once_with(result)
    db.flush.assert_called_once()


def test_create_material_warehouse_not_found():
    db = MagicMock()
    db.scalar.return_value = None

    service = MaterialService(db)

    with pytest.raises(AppError) as exc_info:
        service.create_material(make_material_data())

    assert exc_info.value.code == "WAREHOUSE_NOT_FOUND"
    db.add.assert_not_called()
    db.flush.assert_not_called()


def test_create_material_warehouse_inactive():
    db = MagicMock()

    db.scalar.return_value = MagicMock(
        id=1,
        is_active=False,
    )

    service = MaterialService(db)

    with pytest.raises(AppError) as exc_info:
        service.create_material(make_material_data())

    assert exc_info.value.code == "WAREHOUSE_INACTIVE"
    db.add.assert_not_called()
    db.flush.assert_not_called()


def test_create_material_category_not_found():
    db = MagicMock()

    db.scalar.side_effect = [
        MagicMock(id=1, is_active=True),
        None,
    ]

    service = MaterialService(db)

    with pytest.raises(AppError) as exc_info:
        service.create_material(make_material_data())

    assert exc_info.value.code == "CATEGORY_NOT_FOUND"
    db.add.assert_not_called()
    db.flush.assert_not_called()


def test_create_material_category_inactive():
    db = MagicMock()

    db.scalar.side_effect = [
        MagicMock(id=1, is_active=True),
        MagicMock(id=1, is_active=False),
    ]

    service = MaterialService(db)

    with pytest.raises(AppError) as exc_info:
        service.create_material(make_material_data())

    assert exc_info.value.code == "CATEGORY_INACTIVE"
    db.add.assert_not_called()
    db.flush.assert_not_called()


def test_create_material_location_not_found():
    db = MagicMock()

    db.scalar.side_effect = [
        MagicMock(id=1, is_active=True),
        MagicMock(id=1, is_active=True),
        None,
    ]

    service = MaterialService(db)

    with pytest.raises(AppError) as exc_info:
        service.create_material(make_material_data(location_id=10))

    assert exc_info.value.code == "LOCATION_NOT_FOUND"
    db.add.assert_not_called()
    db.flush.assert_not_called()


def test_create_material_location_inactive():
    db = MagicMock()

    db.scalar.side_effect = [
        MagicMock(id=1, is_active=True),
        MagicMock(id=1, is_active=True),
        MagicMock(id=10, warehouse_id=1, is_active=False),
    ]

    service = MaterialService(db)

    with pytest.raises(AppError) as exc_info:
        service.create_material(make_material_data(location_id=10))

    assert exc_info.value.code == "LOCATION_INACTIVE"
    db.add.assert_not_called()
    db.flush.assert_not_called()


def test_create_material_location_warehouse_mismatch():
    db = MagicMock()

    db.scalar.side_effect = [
        MagicMock(id=1, is_active=True),
        MagicMock(id=1, is_active=True),
        MagicMock(id=10, warehouse_id=2, is_active=True),
    ]

    service = MaterialService(db)

    with pytest.raises(AppError) as exc_info:
        service.create_material(make_material_data(location_id=10))

    assert exc_info.value.code == "LOCATION_WAREHOUSE_MISMATCH"
    db.add.assert_not_called()
    db.flush.assert_not_called()


def test_create_material_duplicate_sku():
    db = MagicMock()

    db.scalar.side_effect = [
        MagicMock(id=1, is_active=True),
        MagicMock(id=1, is_active=True),
        MagicMock(id=99),
    ]

    service = MaterialService(db)

    with pytest.raises(AppError) as exc_info:
        service.create_material(make_material_data())

    assert exc_info.value.code == "SKU_ALREADY_EXISTS"
    db.add.assert_not_called()
    db.flush.assert_not_called()


def test_create_material_same_sku_different_warehouse():
    db = MagicMock()

    db.scalar.side_effect = [
        MagicMock(id=2, is_active=True),
        MagicMock(id=1, is_active=True),
        None,
    ]

    service = MaterialService(db)

    result = service.create_material(make_material_data(warehouse_id=2))

    assert result.warehouse_id == 2
    assert result.sku == "MAT-001"

    db.add.assert_called_once_with(result)
    db.flush.assert_called_once()


def test_list_materials_returns_materials():
    db = MagicMock()

    material_1 = Material(
        id=1,
        warehouse_id=1,
        category_id=1,
        sku="SKU001",
        name="Material 1",
        unit="pcs",
        specification="Spec 1",
        minimum_stock=0,
        is_active=True,
    )
    material_2 = Material(
        id=2,
        warehouse_id=1,
        category_id=1,
        sku="SKU002",
        name="Material 2",
        unit="pcs",
        specification="Spec 2",
        minimum_stock=0,
        is_active=True,
    )

    db.scalars.return_value.all.return_value = [
        material_1,
        material_2,
    ]

    service = MaterialService(db)

    result = service.list_materials()

    assert result == [material_1, material_2]
    db.scalars.assert_called_once()


def test_get_material_returns_material():
    db = MagicMock()

    material = Material(
        id=1,
        warehouse_id=1,
        category_id=1,
        sku="SKU001",
        name="Material 1",
        unit="pcs",
        specification="Spec 1",
        minimum_stock=0,
        is_active=True,
    )

    db.scalar.return_value = material

    service = MaterialService(db)

    result = service.get_material(1)

    assert result is material

    db.scalar.assert_called_once()


def test_get_material_not_found():
    db = MagicMock()
    db.scalar.return_value = None

    service = MaterialService(db)

    with pytest.raises(AppError) as exc_info:
        service.get_material(999)

    assert exc_info.value.code == "MATERIAL_NOT_FOUND"
    assert str(exc_info.value) == "Material not found"


def test_update_material_success():
    db = MagicMock()

    material = Material(
        id=1,
        warehouse_id=1,
        category_id=1,
        sku="MAT-001",
        name="Old Name",
        unit="Cái",
        specification="Old Spec",
        minimum_stock=0,
        is_active=True,
    )

    db.scalar.side_effect = [
        material,
        MagicMock(id=1, is_active=True),
        MagicMock(id=1, is_active=True),
        None,
    ]

    service = MaterialService(db)

    result = service.update_material(
        1,
        MaterialUpdate(
            name="New Name",
            category_id=1,
            location_id=None,
            specification="New Spec",
            minimum_stock=10,
        ),
    )

    assert result is material
    assert result.name == "New Name"
    assert result.specification == "New Spec"
    assert result.minimum_stock == 10

    db.flush.assert_called_once()


def test_update_material_not_found():
    db = MagicMock()
    db.scalar.return_value = None

    service = MaterialService(db)

    with pytest.raises(AppError) as exc_info:
        service.update_material(
            999,
            MaterialUpdate(name="New Name"),
        )

    assert exc_info.value.code == "MATERIAL_NOT_FOUND"
    db.flush.assert_not_called()


def test_update_material_warehouse_not_found():
    db = MagicMock()

    material = MagicMock(
        id=1,
        warehouse_id=1,
    )

    db.scalar.side_effect = [
        material,
        None,
    ]

    service = MaterialService(db)

    with pytest.raises(AppError) as exc_info:
        service.update_material(
            1,
            MaterialUpdate(warehouse_id=2),
        )

    assert exc_info.value.code == "WAREHOUSE_NOT_FOUND"
    db.flush.assert_not_called()


def test_update_material_warehouse_inactive():
    db = MagicMock()

    material = MagicMock(
        id=1,
        warehouse_id=1,
    )

    db.scalar.side_effect = [
        material,
        MagicMock(id=2, is_active=False),
    ]

    service = MaterialService(db)

    with pytest.raises(AppError) as exc_info:
        service.update_material(
            1,
            MaterialUpdate(warehouse_id=2),
        )

    assert exc_info.value.code == "WAREHOUSE_INACTIVE"
    db.flush.assert_not_called()


def test_update_material_warehouse_change_forbidden_with_history():
    db = MagicMock()

    material = MagicMock(
        id=1,
        warehouse_id=1,
    )

    db.scalar.side_effect = [
        material,
        MagicMock(id=2, is_active=True),
        MagicMock(id=100),
    ]

    service = MaterialService(db)

    with pytest.raises(AppError) as exc_info:
        service.update_material(
            1,
            MaterialUpdate(warehouse_id=2),
        )

    assert exc_info.value.code == "MATERIAL_WAREHOUSE_CHANGE_FORBIDDEN"
    db.flush.assert_not_called()


def test_update_material_category_not_found():
    db = MagicMock()

    material = MagicMock(
        id=1,
        warehouse_id=1,
    )

    db.scalar.side_effect = [
        material,
        None,
    ]

    service = MaterialService(db)

    with pytest.raises(AppError) as exc_info:
        service.update_material(
            1,
            MaterialUpdate(category_id=2),
        )

    assert exc_info.value.code == "CATEGORY_NOT_FOUND"
    db.flush.assert_not_called()


def test_update_material_category_inactive():
    db = MagicMock()

    material = MagicMock(
        id=1,
        warehouse_id=1,
    )

    db.scalar.side_effect = [
        material,
        MagicMock(id=2, is_active=False),
    ]

    service = MaterialService(db)

    with pytest.raises(AppError) as exc_info:
        service.update_material(
            1,
            MaterialUpdate(category_id=2),
        )

    assert exc_info.value.code == "CATEGORY_INACTIVE"
    db.flush.assert_not_called()


def test_update_material_location_not_found():
    db = MagicMock()

    material = MagicMock(
        id=1,
        warehouse_id=1,
    )

    db.scalar.side_effect = [
        material,
        None,
    ]

    service = MaterialService(db)

    with pytest.raises(AppError) as exc_info:
        service.update_material(
            1,
            MaterialUpdate(location_id=10),
        )

    assert exc_info.value.code == "LOCATION_NOT_FOUND"
    db.flush.assert_not_called()


def test_update_material_location_inactive():
    db = MagicMock()

    material = MagicMock(
        id=1,
        warehouse_id=1,
    )

    db.scalar.side_effect = [
        material,
        MagicMock(
            id=10,
            warehouse_id=1,
            is_active=False,
        ),
    ]

    service = MaterialService(db)

    with pytest.raises(AppError) as exc_info:
        service.update_material(
            1,
            MaterialUpdate(location_id=10),
        )

    assert exc_info.value.code == "LOCATION_INACTIVE"
    db.flush.assert_not_called()


def test_update_material_location_warehouse_mismatch():
    db = MagicMock()

    material = MagicMock(
        id=1,
        warehouse_id=1,
    )

    db.scalar.side_effect = [
        material,
        MagicMock(
            id=10,
            warehouse_id=2,
            is_active=True,
        ),
    ]

    service = MaterialService(db)

    with pytest.raises(AppError) as exc_info:
        service.update_material(
            1,
            MaterialUpdate(location_id=10),
        )

    assert exc_info.value.code == "LOCATION_WAREHOUSE_MISMATCH"
    db.flush.assert_not_called()


def test_update_material_duplicate_sku():
    db = MagicMock()

    material = MagicMock(
        id=1,
        warehouse_id=1,
    )

    db.scalar.side_effect = [
        material,
        MagicMock(id=99),
    ]

    service = MaterialService(db)

    with pytest.raises(AppError) as exc_info:
        service.update_material(
            1,
            MaterialUpdate(sku="MAT-002"),
        )

    assert exc_info.value.code == "SKU_ALREADY_EXISTS"
    db.flush.assert_not_called()


def test_update_material_allows_warehouse_change_without_history():
    db = MagicMock()

    material = MagicMock(
        id=1,
        warehouse_id=1,
        sku="MAT-001",
    )

    db.scalar.side_effect = [
        material,
        MagicMock(id=2, is_active=True),
        None,
    ]

    service = MaterialService(db)

    result = service.update_material(
        1,
        MaterialUpdate(warehouse_id=2),
    )

    assert result.warehouse_id == 2
    db.flush.assert_called_once()


def test_update_material_can_clear_location():
    db = MagicMock()

    material = MagicMock(
        id=1,
        warehouse_id=1,
        location_id=10,
    )

    db.scalar.return_value = material

    service = MaterialService(db)

    result = service.update_material(
        1,
        MaterialUpdate(location_id=None),
    )

    assert result.location_id is None
    db.flush.assert_called_once()
