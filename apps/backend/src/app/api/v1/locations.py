from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.location import LocationCreate, LocationResponse, LocationUpdate
from app.schemas.response import SuccessResponse
from app.services.location import LocationService

router = APIRouter()


@router.post("", response_model=SuccessResponse)
def create_location(
    data: LocationCreate,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = LocationService(db)

    try:
        location = service.create_location(data)
        db.commit()
        db.refresh(location)

        return SuccessResponse(data=LocationResponse.model_validate(location))
    except Exception:
        db.rollback()
        raise


@router.get("", response_model=SuccessResponse)
def list_locations(
    db: Session = Depends(get_db),  # noqa: B008
):
    service = LocationService(db)

    locations = service.list_locations()

    return SuccessResponse(
        data=[LocationResponse.model_validate(location) for location in locations]
    )


@router.get("/{location_id}", response_model=SuccessResponse)
def get_location(
    location_id: int,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = LocationService(db)

    location = service.get_location(location_id)

    return SuccessResponse(data=LocationResponse.model_validate(location))


@router.patch("/{location_id}", response_model=SuccessResponse)
def update_location(
    location_id: int,
    data: LocationUpdate,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = LocationService(db)

    try:
        location = service.update_location(location_id, data)
        db.commit()
        db.refresh(location)

        return SuccessResponse(data=LocationResponse.model_validate(location))
    except Exception:
        db.rollback()
        raise
