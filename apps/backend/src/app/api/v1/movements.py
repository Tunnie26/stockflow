from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.movement import MovementQueryParams
from app.schemas.response import SuccessResponse
from app.services.movement_query_service import MovementQueryService

router = APIRouter()


@router.get("", response_model=SuccessResponse)
def list_movements(
    params: MovementQueryParams = Depends(),  # noqa: B008
    db: Session = Depends(get_db),  # noqa: B008
):
    service = MovementQueryService(db)

    movements = service.list_movements(params)

    return SuccessResponse(data=movements)
