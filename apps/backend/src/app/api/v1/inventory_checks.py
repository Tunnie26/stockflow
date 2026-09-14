from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db, require_user
from app.models.user import User
from app.schemas.inventory_check import (
    InventoryCheckCreate,
)
from app.schemas.response import SuccessResponse
from app.services.inventory_check_query_service import (
    InventoryCheckQueryService,
)
from app.services.inventory_check_service import InventoryCheckService

router = APIRouter()


@router.post("", response_model=SuccessResponse)
def create_inventory_check(
    data: InventoryCheckCreate,
    db: Session = Depends(get_db),  # noqa: B008
    current_user: User = Depends(require_user()),  # noqa: B008
):
    service = InventoryCheckService(db)

    try:
        inventory_check = service.create(data)
        db.commit()

        query_service = InventoryCheckQueryService(db)

        return SuccessResponse(
            data=query_service.get_inventory_check(
                inventory_check.id,
            )
        )
    except Exception:
        db.rollback()
        raise


@router.get("", response_model=SuccessResponse)
def list_inventory_checks(
    db: Session = Depends(get_db),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    service = InventoryCheckQueryService(db)

    return SuccessResponse(
        data=service.list_inventory_checks(),
    )


@router.get("/{inventory_check_id}", response_model=SuccessResponse)
def get_inventory_check(
    inventory_check_id: int,
    db: Session = Depends(get_db),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    service = InventoryCheckQueryService(db)

    return SuccessResponse(
        data=service.get_inventory_check(
            inventory_check_id,
        ),
    )
