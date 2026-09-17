from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, require_admin, require_user
from app.models.transaction import TransactionType
from app.models.user import User
from app.schemas.response import SuccessResponse
from app.schemas.transaction import (
    AdjustmentCreate,
    TransactionCreate,
    TransactionResponse
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


@router.get("", response_model=SuccessResponse)
def list_transactions(
    warehouse_id: int | None = Query(default=None, gt=0),
    transaction_type: TransactionType | None = None,
    supplier_id: int | None = Query(default=None, gt=0),
    date_from: date | None = None,
    date_to: date | None = None,
    search: str | None = Query(default=None, max_length=100),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),  # noqa: B008
    current_user: User = Depends(require_user()),  # noqa: B008
):
    service = TransactionService(db)

    result = service.list_transactions(
        warehouse_id=warehouse_id,
        transaction_type=transaction_type,
        supplier_id=supplier_id,
        date_from=date_from,
        date_to=date_to,
        search=search,
        page=page,
        page_size=page_size,
    )

    return SuccessResponse(data=result)


@router.get(
    "/{transaction_id}",
    response_model=SuccessResponse,
)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),  # noqa: B008
    current_user: User = Depends(require_user()),  # noqa: B008
):
    service = TransactionService(db)

    transaction = service.get_transaction(transaction_id)

    return SuccessResponse(data=TransactionResponse.model_validate(transaction))


@router.post("/adjustments", response_model=SuccessResponse)
def create_adjustment(
    data: AdjustmentCreate,
    db: Session = Depends(get_db),  # noqa: B008
    current_user: User = Depends(require_admin()),  # noqa: B008
):
    service = AdjustmentService(db)

    try:
        adjustment = service.create(data)

        db.commit()
        db.refresh(adjustment)

        return SuccessResponse(
            data=TransactionResponse.model_validate(adjustment)
        )

    except Exception:
        db.rollback()
        raise