from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_db,
    require_admin,
    require_user,
)
from app.models.user import User
from app.schemas.response import SuccessResponse
from app.schemas.transaction import (
    AdjustmentCreate,
    TransactionCreate,
    TransactionResponse,
)
from app.services.adjustment_service import AdjustmentService
from app.services.transaction_service import TransactionService

router = APIRouter()


@router.post("", response_model=SuccessResponse)
def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db),  # noqa: B008
    current_user: User = Depends(require_user()),  # noqa: B008
):
    service = TransactionService(db)

    try:
        transaction = service.create(data)
        db.commit()

        db.refresh(transaction)

        return SuccessResponse(data=TransactionResponse.model_validate(transaction))
    except Exception:
        db.rollback()
        raise


@router.post("/adjustments", response_model=SuccessResponse)
def create_adjustment(
    data: AdjustmentCreate,
    db: Session = Depends(get_db),  # noqa: B008
    current_user: User = Depends(require_admin()),  # noqa: B008
):
    service = AdjustmentService(db)

    try:
        transaction = service.create(data)
        db.commit()

        db.refresh(transaction)

        return SuccessResponse(data=TransactionResponse.model_validate(transaction))
    except Exception:
        db.rollback()
        raise
