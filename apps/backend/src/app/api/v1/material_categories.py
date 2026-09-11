from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.material_category import (
    MaterialCategoryCreate,
    MaterialCategoryResponse,
    MaterialCategoryUpdate,
)
from app.schemas.response import SuccessResponse
from app.services.material_category import MaterialCategoryService

router = APIRouter()


@router.post("", response_model=SuccessResponse)
def create_material_category(
    data: MaterialCategoryCreate,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = MaterialCategoryService(db)

    try:
        category = service.create_material_category(data)
        db.commit()
        db.refresh(category)

        return SuccessResponse(data=MaterialCategoryResponse.model_validate(category))
    except Exception:
        db.rollback()
        raise


@router.get("", response_model=SuccessResponse)
def list_material_categories(
    db: Session = Depends(get_db),  # noqa: B008
):
    service = MaterialCategoryService(db)

    categories = service.list_material_categories()

    return SuccessResponse(
        data=[
            MaterialCategoryResponse.model_validate(category) for category in categories
        ]
    )


@router.get(
    "/{category_id}",
    response_model=SuccessResponse,
)
def get_material_category(
    category_id: int,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = MaterialCategoryService(db)

    category = service.get_material_category(category_id)

    return SuccessResponse(data=MaterialCategoryResponse.model_validate(category))


@router.patch(
    "/{category_id}",
    response_model=SuccessResponse,
)
def update_material_category(
    category_id: int,
    data: MaterialCategoryUpdate,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = MaterialCategoryService(db)

    try:
        category = service.update_material_category(category_id, data)
        db.commit()
        db.refresh(category)

        return SuccessResponse(data=MaterialCategoryResponse.model_validate(category))
    except Exception:
        db.rollback()
        raise
