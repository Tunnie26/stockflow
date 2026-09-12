from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.inventory import InventoryQueryParams
from app.schemas.response import SuccessResponse
from app.services.inventory_query_service import InventoryQueryService

router = APIRouter()


@router.get("", response_model=SuccessResponse)
def list_inventory(
    params: InventoryQueryParams = Depends(),  # noqa: B008
    db: Session = Depends(get_db),  # noqa: B008
):
    service = InventoryQueryService(db)

    inventory = service.list_inventory(params)

    return SuccessResponse(data=inventory)


@router.get("/{material_id}", response_model=SuccessResponse)
def get_inventory(
    material_id: int,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = InventoryQueryService(db)
    inventory = service.get_inventory(material_id)

    return SuccessResponse(data=inventory)
