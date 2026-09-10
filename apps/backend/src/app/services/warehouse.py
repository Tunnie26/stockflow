from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import AppError
from app.models.warehouse import Warehouse
from app.schemas.warehouse import WarehouseCreate, WarehouseUpdate


class WarehouseService:
    def __init__(self, db: Session):
        self.db = db

    def create_warehouse(self, data: WarehouseCreate) -> Warehouse:
        existing_warehouse = self.db.scalar(
            select(Warehouse).where(Warehouse.code == data.code)
        )

        if existing_warehouse is not None:
            raise AppError(
                "Warehouse code already exists",
                code="WAREHOUSE_CODE_ALREADY_EXISTS",
            )

        warehouse = Warehouse(
            code=data.code,
            name=data.name,
        )

        self.db.add(warehouse)
        self.db.flush()

        return warehouse

    def list_warehouses(self) -> list[Warehouse]:
        statement = select(Warehouse).order_by(Warehouse.id)
        return list(self.db.scalars(statement).all())

    def get_warehouse(self, warehouse_id: int) -> Warehouse:
        warehouse = self.db.scalar(
            select(Warehouse).where(Warehouse.id == warehouse_id)
        )

        if warehouse is None:
            raise AppError(
                "Warehouse not found",
                code="WAREHOUSE_NOT_FOUND",
            )

        return warehouse

    def update_warehouse(
        self,
        warehouse_id: int,
        data: WarehouseUpdate,
    ) -> Warehouse:
        warehouse = self.get_warehouse(warehouse_id)

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(warehouse, field, value)

        self.db.flush()

        return warehouse