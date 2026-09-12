from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.dashboard import DashboardResponse
from app.schemas.response import SuccessResponse
from app.services.dashboard_service import DashboardQueryService

router = APIRouter()


@router.get("", response_model=SuccessResponse)
def get_dashboard(
    db: Session = Depends(get_db),  # noqa: B008
) -> SuccessResponse:
    service = DashboardQueryService(db)

    dashboard = service.get_dashboard()

    return SuccessResponse(
        data=DashboardResponse.model_validate(dashboard),
    )
