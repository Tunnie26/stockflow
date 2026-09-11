from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from app.schemas.response import SuccessResponse
from app.services.customer import CustomerService

router = APIRouter()


@router.post("", response_model=SuccessResponse)
def create_customer(
    data: CustomerCreate,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = CustomerService(db)

    try:
        customer = service.create_customer(data)
        db.commit()
        db.refresh(customer)

        return SuccessResponse(data=CustomerResponse.model_validate(customer))
    except Exception:
        db.rollback()
        raise


@router.get("", response_model=SuccessResponse)
def list_customers(
    db: Session = Depends(get_db),  # noqa: B008
):
    service = CustomerService(db)
    customers = service.list_customers()

    return SuccessResponse(
        data=[CustomerResponse.model_validate(customer) for customer in customers]
    )


@router.get(
    "/{customer_id}",
    response_model=SuccessResponse,
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = CustomerService(db)
    customer = service.get_customer(customer_id)

    return SuccessResponse(data=CustomerResponse.model_validate(customer))


@router.patch(
    "/{customer_id}",
    response_model=SuccessResponse,
)
def update_customer(
    customer_id: int,
    data: CustomerUpdate,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = CustomerService(db)

    try:
        customer = service.update_customer(customer_id, data)
        db.commit()
        db.refresh(customer)

        return SuccessResponse(data=CustomerResponse.model_validate(customer))
    except Exception:
        db.rollback()
        raise
