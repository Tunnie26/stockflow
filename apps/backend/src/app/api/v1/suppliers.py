from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.response import SuccessResponse
from app.schemas.supplier import SupplierCreate, SupplierResponse, SupplierUpdate
from app.services.supplier import SupplierService

router = APIRouter()


@router.post("", response_model=SuccessResponse)
def create_supplier(
    data: SupplierCreate,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = SupplierService(db)

    try:
        supplier = service.create_supplier(data)
        db.commit()
        db.refresh(supplier)

        return SuccessResponse(data=SupplierResponse.model_validate(supplier))
    except Exception:
        db.rollback()
        raise


@router.get("", response_model=SuccessResponse)
def list_suppliers(
    db: Session = Depends(get_db),  # noqa: B008
):
    service = SupplierService(db)
    suppliers = service.list_suppliers()

    return SuccessResponse(
        data=[SupplierResponse.model_validate(supplier) for supplier in suppliers]
    )


@router.get(
    "/{supplier_id}",
    response_model=SuccessResponse,
)
def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = SupplierService(db)
    supplier = service.get_supplier(supplier_id)

    return SuccessResponse(data=SupplierResponse.model_validate(supplier))


@router.patch(
    "/{supplier_id}",
    response_model=SuccessResponse,
)
def update_supplier(
    supplier_id: int,
    data: SupplierUpdate,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = SupplierService(db)

    try:
        supplier = service.update_supplier(supplier_id, data)
        db.commit()
        db.refresh(supplier)

        return SuccessResponse(data=SupplierResponse.model_validate(supplier))
    except Exception:
        db.rollback()
        raise
