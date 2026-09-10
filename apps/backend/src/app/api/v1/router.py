from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.material import MaterialCreate, MaterialResponse, MaterialUpdate
from app.schemas.response import SuccessResponse
from app.services.material import MaterialService

router = APIRouter()


@router.get("/db-check")
def database_check(db: Session = Depends(get_db)):  # noqa: B008
    result = db.execute(text("SELECT 1"))
    return {"database": result.scalar_one()}


@router.post(
    "/materials",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_material(
    data: MaterialCreate,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = MaterialService(db)

    try:
        material = service.create_material(data)
        db.commit()
        db.refresh(material)

        return {"data": MaterialResponse.model_validate(material)}

    except Exception:
        db.rollback()
        raise


@router.get(
    "/materials",
    response_model=SuccessResponse,
)
def list_materials(
    db: Session = Depends(get_db),  # noqa: B008
):
    service = MaterialService(db)
    materials = service.list_materials()

    return {
        "data": [MaterialResponse.model_validate(material) for material in materials]
    }


@router.get(
    "/materials/{material_id}",
    response_model=SuccessResponse,
)
def get_material(
    material_id: int,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = MaterialService(db)
    material = service.get_material(material_id)

    return {"data": MaterialResponse.model_validate(material)}


@router.patch(
    "/materials/{material_id}",
    response_model=SuccessResponse,
)
def update_material(
    material_id: int,
    data: MaterialUpdate,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = MaterialService(db)

    try:
        material = service.update_material(material_id, data)
        db.commit()
        db.refresh(material)

        return {"data": MaterialResponse.model_validate(material)}

    except Exception:
        db.rollback()
        raise
