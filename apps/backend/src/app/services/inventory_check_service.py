from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.exceptions import AppError
from app.models.inventory_check import InventoryCheck
from app.models.inventory_check_detail import InventoryCheckDetail
from app.models.material import Material
from app.models.stock_balance import StockBalance
from app.models.transaction import Transaction, TransactionType
from app.models.transaction_detail import TransactionDetail
from app.models.warehouse import Warehouse
from app.schemas.inventory_check import InventoryCheckCreate
from app.services.inventory_service import InventoryService


class InventoryCheckService:
    def __init__(self, db: Session):
        self.db = db
        self.inventory_service = InventoryService(db)

    def create(self, payload: InventoryCheckCreate) -> InventoryCheck:
        warehouse = self._validate_warehouse(payload.warehouse_id)

        validated_details = self._validate_details(
            payload=payload,
            warehouse_id=warehouse.id,
        )

        check = InventoryCheck(
            check_no=self._generate_check_no(),
            warehouse_id=warehouse.id,
            check_date=payload.check_date,
            note=payload.note,
        )

        self.db.add(check)
        self.db.flush()

        snapshots: list[tuple[InventoryCheckDetail, Decimal]] = []

        for material, actual_quantity, note in validated_details:
            system_quantity = self._get_system_quantity(material.id)
            difference = actual_quantity - system_quantity

            check_detail = InventoryCheckDetail(
                inventory_check_id=check.id,
                material_id=material.id,
                system_quantity=system_quantity,
                actual_quantity=actual_quantity,
                difference=difference,
                note=note,
            )

            check.details.append(check_detail)
            self.db.add(check_detail)
            snapshots.append((check_detail, difference))

        self.db.flush()

        adjustment_transaction = self._create_adjustment_if_needed(
            check=check,
            details=snapshots,
            warehouse_id=warehouse.id,
            check_date=payload.check_date,
        )

        if adjustment_transaction is not None:
            check.adjustment_transaction_id = adjustment_transaction.id
            self.db.flush()

        return check

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

    def _validate_details(
        self,
        payload: InventoryCheckCreate,
        warehouse_id: int,
    ) -> list[tuple[Material, Decimal, str | None]]:
        material_ids = [detail.material_id for detail in payload.details]

        if len(material_ids) != len(set(material_ids)):
            raise AppError(
                "Duplicate material in inventory check",
                code="DUPLICATE_MATERIAL",
            )

        validated_details = []

        for detail in payload.details:
            material = self._get_material(
                material_id=detail.material_id,
                warehouse_id=warehouse_id,
            )

            validated_details.append(
                (
                    material,
                    detail.actual_quantity,
                    detail.note,
                )
            )

        return validated_details

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
                "Material does not belong to inventory check warehouse",
                code="MATERIAL_WRONG_WAREHOUSE",
            )

        return material

    def _get_system_quantity(
        self,
        material_id: int,
    ) -> Decimal:
        balance = self.db.scalar(
            select(StockBalance).where(
                StockBalance.material_id == material_id,
            )
        )

        if balance is None:
            return Decimal("0")

        return balance.quantity

    def _create_adjustment_if_needed(
        self,
        check: InventoryCheck,
        details: list[tuple[InventoryCheckDetail, Decimal]],
        warehouse_id: int,
        check_date,
    ) -> Transaction | None:
        changed_details = [
            detail for detail, difference in details if difference != Decimal("0")
        ]

        if not changed_details:
            return None

        transaction = Transaction(
            transaction_no=self._generate_transaction_no(),
            transaction_type=TransactionType.ADJUSTMENT,
            warehouse_id=warehouse_id,
            transaction_date=check_date,
            note=check.note or "Inventory check adjustment",
        )

        self.db.add(transaction)
        self.db.flush()

        for check_detail in changed_details:
            material = self.db.scalar(
                select(Material).where(
                    Material.id == check_detail.material_id,
                )
            )

            transaction_detail = TransactionDetail(
                transaction_id=transaction.id,
                material_id=material.id,
                sku_snapshot=material.sku,
                name_snapshot=material.name,
                unit_snapshot=material.unit,
                specification_snapshot=material.specification,
                quantity=check_detail.actual_quantity,
                unit_price=None,
                total_amount=None,
                note=check_detail.note,
            )

            self.db.add(transaction_detail)
            self.db.flush()

            self.inventory_service.apply_adjustment(
                transaction_detail=transaction_detail,
                actual_quantity=check_detail.actual_quantity,
            )

        return transaction

    def _generate_check_no(self) -> int:
        max_check_no = self.db.scalar(select(func.max(InventoryCheck.check_no)))

        return (max_check_no or 0) + 1

    def _generate_transaction_no(self) -> int:
        max_transaction_no = self.db.scalar(
            select(func.max(Transaction.transaction_no))
        )

        return (max_transaction_no or 0) + 1
