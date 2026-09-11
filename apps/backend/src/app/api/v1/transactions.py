from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.response import SuccessResponse
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.transaction_service import TransactionService

router = APIRouter()


@router.post("", response_model=SuccessResponse)
def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db),  # noqa: B008
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
