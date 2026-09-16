from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.dashboard import DashboardResponse
from app.schemas.response import SuccessResponse
from app.services.dashboard_service import DashboardQueryService

router = APIRouter()


@router.get("", response_model=SuccessResponse)
def get_dashboard(
    warehouse_id: int = Query(..., gt=0),
    db: Session = Depends(get_db),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
) -> SuccessResponse:
    service = DashboardQueryService(db)

    dashboard = service.get_dashboard(warehouse_id)

    return SuccessResponse(
        data=DashboardResponse.model_validate(dashboard),
    )
