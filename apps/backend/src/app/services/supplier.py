from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import AppError
from app.models.supplier import Supplier
from app.schemas.supplier import SupplierCreate, SupplierUpdate


class SupplierService:
    def __init__(self, db: Session):
        self.db = db

    def create_supplier(self, data: SupplierCreate) -> Supplier:
        existing_supplier = self.db.scalar(
            select(Supplier).where(Supplier.code == data.code)
        )

        if existing_supplier is not None:
            raise AppError(
                "Supplier code already exists",
                code="SUPPLIER_CODE_ALREADY_EXISTS",
            )

        supplier = Supplier(
            code=data.code,
            name=data.name,
            tax_code=data.tax_code,
            phone=data.phone,
            email=data.email,
            address=data.address,
            contact_person=data.contact_person,
            note=data.note,
        )

        self.db.add(supplier)
        self.db.flush()

        return supplier

    def list_suppliers(self) -> list[Supplier]:
        statement = select(Supplier).order_by(Supplier.id)
        return list(self.db.scalars(statement).all())

    def get_supplier(self, supplier_id: int) -> Supplier:
        supplier = self.db.scalar(select(Supplier).where(Supplier.id == supplier_id))

        if supplier is None:
            raise AppError(
                "Supplier not found",
                code="SUPPLIER_NOT_FOUND",
                status_code=404,
            )

        return supplier

    def update_supplier(
        self,
        supplier_id: int,
        data: SupplierUpdate,
    ) -> Supplier:
        supplier = self.get_supplier(supplier_id)

        update_data = data.model_dump(exclude_unset=True)

        if "code" in update_data:
            existing_supplier = self.db.scalar(
                select(Supplier).where(
                    Supplier.code == update_data["code"],
                    Supplier.id != supplier.id,
                )
            )

            if existing_supplier is not None:
                raise AppError(
                    "Supplier code already exists",
                    code="SUPPLIER_CODE_ALREADY_EXISTS",
                )

        for field, value in update_data.items():
            setattr(supplier, field, value)

        self.db.flush()

        return supplier
