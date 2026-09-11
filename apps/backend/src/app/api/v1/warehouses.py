from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.response import SuccessResponse
from app.schemas.warehouse import WarehouseCreate, WarehouseResponse, WarehouseUpdate
from app.services.warehouse import WarehouseService

router = APIRouter()


@router.post("", response_model=SuccessResponse)
def create_warehouse(
    data: WarehouseCreate,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = WarehouseService(db)

    try:
        warehouse = service.create_warehouse(data)
        db.commit()
        db.refresh(warehouse)

        return SuccessResponse(data=WarehouseResponse.model_validate(warehouse))
    except Exception:
        db.rollback()
        raise


@router.get("", response_model=SuccessResponse)
def list_warehouses(
    db: Session = Depends(get_db),  # noqa: B008
):
    service = WarehouseService(db)

    warehouses = service.list_warehouses()

    return SuccessResponse(
        data=[WarehouseResponse.model_validate(warehouse) for warehouse in warehouses]
    )


@router.get("/{warehouse_id}", response_model=SuccessResponse)
def get_warehouse(
    warehouse_id: int,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = WarehouseService(db)

    warehouse = service.get_warehouse(warehouse_id)

    return SuccessResponse(data=WarehouseResponse.model_validate(warehouse))


@router.patch("/{warehouse_id}", response_model=SuccessResponse)
def update_warehouse(
    warehouse_id: int,
    data: WarehouseUpdate,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = WarehouseService(db)

    try:
        warehouse = service.update_warehouse(warehouse_id, data)
        db.commit()
        db.refresh(warehouse)

        return SuccessResponse(data=WarehouseResponse.model_validate(warehouse))
    except Exception:
        db.rollback()
        raise
