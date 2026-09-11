from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.material import MaterialCreate, MaterialResponse, MaterialUpdate
from app.schemas.response import SuccessResponse
from app.services.material import MaterialService

router = APIRouter()


@router.post(
    "",
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

        return SuccessResponse(
            data=MaterialResponse.model_validate(material),
        )
    except Exception:
        db.rollback()
        raise


@router.get(
    "",
    response_model=SuccessResponse,
)
def list_materials(
    db: Session = Depends(get_db),  # noqa: B008
):
    service = MaterialService(db)
    materials = service.list_materials()

    return SuccessResponse(
        data=[MaterialResponse.model_validate(material) for material in materials],
    )


@router.get(
    "/{material_id}",
    response_model=SuccessResponse,
)
def get_material(
    material_id: int,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = MaterialService(db)
    material = service.get_material(material_id)

    return SuccessResponse(
        data=MaterialResponse.model_validate(material),
    )


@router.patch(
    "/{material_id}",
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

        return SuccessResponse(
            data=MaterialResponse.model_validate(material),
        )
    except Exception:
        db.rollback()
        raise
