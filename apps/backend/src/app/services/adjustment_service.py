from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.exceptions import AppError
from app.models.material import Material
from app.models.transaction import Transaction, TransactionType
from app.models.transaction_detail import TransactionDetail
from app.models.warehouse import Warehouse
from app.schemas.transaction import AdjustmentCreate
from app.services.inventory_service import InventoryService


class AdjustmentService:
    def __init__(self, db: Session):
        self.db = db
        self.inventory_service = InventoryService(db)

    def create(self, payload: AdjustmentCreate) -> Transaction:
        self._validate_warehouse(payload.warehouse_id)

        transaction = Transaction(
            transaction_no=self._generate_transaction_no(),
            transaction_type=TransactionType.ADJUSTMENT,
            warehouse_id=payload.warehouse_id,
            transaction_date=payload.transaction_date,
            note=payload.reason,
        )

        self.db.add(transaction)
        self.db.flush()

        transaction_details = []

        for detail in payload.details:
            material = self._get_material(
                material_id=detail.material_id,
                warehouse_id=payload.warehouse_id,
            )

            transaction_detail = TransactionDetail(
                transaction_id=transaction.id,
                material_id=material.id,
                sku_snapshot=material.sku,
                name_snapshot=material.name,
                unit_snapshot=material.unit,
                specification_snapshot=material.specification,
                quantity=detail.actual_quantity,
                unit_price=None,
                total_amount=None,
                note=detail.note,
            )

            self.db.add(transaction_detail)
            transaction_details.append((transaction_detail, detail.actual_quantity))

        self.db.flush()

        for transaction_detail, actual_quantity in transaction_details:
            self.inventory_service.apply_adjustment(
                transaction_detail=transaction_detail,
                actual_quantity=actual_quantity,
            )

        return transaction

    def _generate_transaction_no(self) -> int:
        max_transaction_no = self.db.scalar(
            select(func.max(Transaction.transaction_no))
        )

        return (max_transaction_no or 0) + 1

    def _validate_warehouse(
        self,
        warehouse_id: int,
    ) -> Warehouse:
        warehouse = self.db.scalar(
            select(Warehouse).where(Warehouse.id == warehouse_id)
        )

        if warehouse is None:
            raise AppError(
                "Warehouse not found",
                code="WAREHOUSE_NOT_FOUND",
                status_code=404,
            )

        if not warehouse.is_active:
            raise AppError(
                "Warehouse is inactive",
                code="WAREHOUSE_INACTIVE",
            )

        return warehouse

    def _get_material(
        self,
        material_id: int,
        warehouse_id: int,
    ) -> Material:
        material = self.db.scalar(select(Material).where(Material.id == material_id))

        if material is None:
            raise AppError(
                "Material not found",
                code="MATERIAL_NOT_FOUND",
                status_code=404,
            )

        if not material.is_active:
            raise AppError(
                "Material is inactive",
                code="MATERIAL_INACTIVE",
            )

        if material.warehouse_id != warehouse_id:
            raise AppError(
                "Material does not belong to adjustment warehouse",
                code="MATERIAL_WRONG_WAREHOUSE",
            )

        return material
