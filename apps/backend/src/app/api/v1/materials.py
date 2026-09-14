from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db, require_user
from app.models.user import User
from app.schemas.material import MaterialCreate, MaterialUpdate
from app.schemas.response import SuccessResponse
from app.services.material import MaterialService, to_response

router = APIRouter()


@router.get(
    "",
    response_model=SuccessResponse,
)
def list_materials(
    db: Session = Depends(get_db),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    service = MaterialService(db)
    materials = service.list_materials()

    return SuccessResponse(
        data=[to_response(material) for material in materials],
    )


@router.get(
    "/{material_id}",
    response_model=SuccessResponse,
)
def get_material(
    material_id: int,
    db: Session = Depends(get_db),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    service = MaterialService(db)
    material = service.get_material(material_id)

    return SuccessResponse(
        data=to_response(material),
    )


@router.post(
    "",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_material(
    data: MaterialCreate,
    db: Session = Depends(get_db),  # noqa: B008
    current_user: User = Depends(require_user()),  # noqa: B008
):
    service = MaterialService(db)

    try:
        material = service.create_material(data)
        db.commit()
        db.refresh(material)

        return SuccessResponse(data=to_response(material))
    except Exception:
        db.rollback()
        raise


@router.patch(
    "/{material_id}",
    response_model=SuccessResponse,
)
def update_material(
    material_id: int,
    data: MaterialUpdate,
    db: Session = Depends(get_db),  # noqa: B008
    current_user: User = Depends(require_user()),  # noqa: B008
):
    service = MaterialService(db)

    try:
        material = service.update_material(material_id, data)
        db.commit()
        db.refresh(material)

        return SuccessResponse(
            data=to_response(material),
        )
    except Exception:
        db.rollback()
        raise
