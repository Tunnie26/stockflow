from unittest.mock import MagicMock

import pytest

from app.exceptions import AppError
from app.models.material_category import MaterialCategory
from app.schemas.material_category import (
    MaterialCategoryCreate,
    MaterialCategoryUpdate,
)
from app.services.material_category import MaterialCategoryService


def make_category(
    category_id: int = 1,
    code: str = "BOX",
    name: str = "Thùng",
    is_active: bool = True,
) -> MaterialCategory:
    return MaterialCategory(
        id=category_id,
        code=code,
        name=name,
        is_active=is_active,
    )


def test_create_material_category_success():
    db = MagicMock()
    db.scalar.return_value = None

    service = MaterialCategoryService(db)

    data = MaterialCategoryCreate(
        code="BOX",
        name="Thùng",
    )

    result = service.create_material_category(data)

    assert result.code == "BOX"
    assert result.name == "Thùng"

    db.add.assert_called_once()
    db.flush.assert_called_once()


def test_create_material_category_duplicate_code():
    db = MagicMock()
    db.scalar.return_value = make_category()

    service = MaterialCategoryService(db)

    data = MaterialCategoryCreate(
        code="BOX",
        name="Thùng",
    )

    with pytest.raises(AppError) as exc_info:
        service.create_material_category(data)

    assert exc_info.value.code == "MATERIAL_CATEGORY_CODE_ALREADY_EXISTS"

    db.add.assert_not_called()
    db.flush.assert_not_called()


def test_list_material_categories():
    db = MagicMock()

    categories = [
        make_category(category_id=1, code="BOX", name="Thùng"),
        make_category(category_id=2, code="BAG", name="Túi"),
    ]

    db.scalars.return_value.all.return_value = categories

    service = MaterialCategoryService(db)

    result = service.list_material_categories()

    assert result == categories


def test_get_material_category_success():
    db = MagicMock()

    category = make_category()
    db.scalar.return_value = category

    service = MaterialCategoryService(db)

    result = service.get_material_category(1)

    assert result == category


def test_get_material_category_not_found():
    db = MagicMock()
    db.scalar.return_value = None

    service = MaterialCategoryService(db)

    with pytest.raises(AppError) as exc_info:
        service.get_material_category(999)

    assert exc_info.value.code == "MATERIAL_CATEGORY_NOT_FOUND"


def test_update_material_category_success():
    db = MagicMock()

    category = make_category()

    db.scalar.return_value = category

    service = MaterialCategoryService(db)

    data = MaterialCategoryUpdate(
        name="Thùng carton",
    )

    result = service.update_material_category(1, data)

    assert result.code == "BOX"
    assert result.name == "Thùng carton"

    db.flush.assert_called_once()


def test_update_material_category_is_active():
    db = MagicMock()

    category = make_category()

    db.scalar.return_value = category

    service = MaterialCategoryService(db)

    data = MaterialCategoryUpdate(
        is_active=False,
    )

    result = service.update_material_category(1, data)

    assert result.code == "BOX"
    assert result.name == "Thùng"
    assert result.is_active is False

    db.flush.assert_called_once()


def test_update_material_category_not_found():
    db = MagicMock()
    db.scalar.return_value = None

    service = MaterialCategoryService(db)

    data = MaterialCategoryUpdate(
        name="Updated",
    )

    with pytest.raises(AppError) as exc_info:
        service.update_material_category(999, data)

    assert exc_info.value.code == "MATERIAL_CATEGORY_NOT_FOUND"

    db.flush.assert_not_called()
