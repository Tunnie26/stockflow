from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.receiving_unit import (
    ReceivingUnitCreate,
    ReceivingUnitResponse,
    ReceivingUnitUpdate,
)
from app.schemas.response import SuccessResponse
from app.services.receiving_unit import ReceivingUnitService

router = APIRouter()


@router.post("", response_model=SuccessResponse)
def create_receiving_unit(
    data: ReceivingUnitCreate,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = ReceivingUnitService(db)

    try:
        unit = service.create_receiving_unit(data)
        db.commit()
        db.refresh(unit)

        return SuccessResponse(data=ReceivingUnitResponse.model_validate(unit))
    except Exception:
        db.rollback()
        raise


@router.get("", response_model=SuccessResponse)
def list_receiving_units(
    db: Session = Depends(get_db),  # noqa: B008
):
    service = ReceivingUnitService(db)
    units = service.list_receiving_units()

    return SuccessResponse(
        data=[ReceivingUnitResponse.model_validate(unit) for unit in units]
    )


@router.get(
    "/{receiving_unit_id}",
    response_model=SuccessResponse,
)
def get_receiving_unit(
    receiving_unit_id: int,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = ReceivingUnitService(db)
    unit = service.get_receiving_unit(receiving_unit_id)

    return SuccessResponse(data=ReceivingUnitResponse.model_validate(unit))


@router.patch(
    "/{receiving_unit_id}",
    response_model=SuccessResponse,
)
def update_receiving_unit(
    receiving_unit_id: int,
    data: ReceivingUnitUpdate,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = ReceivingUnitService(db)

    try:
        unit = service.update_receiving_unit(
            receiving_unit_id,
            data,
        )
        db.commit()
        db.refresh(unit)

        return SuccessResponse(data=ReceivingUnitResponse.model_validate(unit))
    except Exception:
        db.rollback()
        raise
