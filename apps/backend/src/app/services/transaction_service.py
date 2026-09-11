from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.exceptions import AppError
from app.models.material import Material
from app.models.receiving_unit import ReceivingUnit
from app.models.supplier import Supplier
from app.models.transaction import Transaction, TransactionType
from app.models.transaction_detail import TransactionDetail
from app.models.warehouse import Warehouse
from app.schemas.transaction import TransactionCreate


class TransactionService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: TransactionCreate) -> Transaction:
        self._validate_business_rules(payload)

        transaction = Transaction(
            transaction_no=self._generate_transaction_no(),
            transaction_type=payload.transaction_type,
            warehouse_id=payload.warehouse_id,
            destination_warehouse_id=payload.destination_warehouse_id,
            supplier_id=payload.supplier_id,
            receiving_unit_id=payload.receiving_unit_id,
            other_recipient=payload.other_recipient,
            transaction_date=payload.transaction_date,
            note=payload.note,
        )

        self.db.add(transaction)
        self.db.flush()

        for detail in payload.details:
            material = self._get_material(
                material_id=detail.material_id,
                warehouse_id=payload.warehouse_id,
            )

            total_amount = (
                detail.quantity * detail.unit_price
                if detail.unit_price is not None
                else None
            )

            transaction_detail = TransactionDetail(
                transaction_id=transaction.id,
                material_id=material.id,
                sku_snapshot=material.sku,
                name_snapshot=material.name,
                unit_snapshot=material.unit,
                specification_snapshot=material.specification,
                quantity=detail.quantity,
                unit_price=detail.unit_price,
                total_amount=total_amount,
                note=detail.note,
            )

            self.db.add(transaction_detail)

        self.db.flush()

        return transaction

    def _generate_transaction_no(self) -> int:
        max_transaction_no = self.db.scalar(
            select(func.max(Transaction.transaction_no))
        )

        return (max_transaction_no or 0) + 1

    def _validate_business_rules(
        self,
        payload: TransactionCreate,
    ) -> None:
        self._validate_warehouse(payload.warehouse_id)

        if payload.transaction_type == TransactionType.INBOUND:
            self._validate_inbound(payload)

        elif payload.transaction_type == TransactionType.OUTBOUND:
            self._validate_outbound(payload)

        elif payload.transaction_type == TransactionType.TRANSFER:
            self._validate_transfer(payload)

        elif payload.transaction_type == TransactionType.ADJUSTMENT:
            raise AppError(
                "Adjustment must use the adjustment workflow",
                code="INVALID_TRANSACTION_TYPE",
            )

    def _validate_inbound(
        self,
        payload: TransactionCreate,
    ) -> None:
        if payload.supplier_id is None:
            raise AppError(
                "Supplier is required for inbound transaction",
                code="SUPPLIER_REQUIRED",
            )

        self._validate_supplier(payload.supplier_id)

        if payload.destination_warehouse_id is not None:
            raise AppError(
                "Destination warehouse is not allowed for inbound transaction",
                code="INVALID_DESTINATION_WAREHOUSE",
            )

        if payload.receiving_unit_id is not None:
            raise AppError(
                "Receiving unit is not allowed for inbound transaction",
                code="INVALID_RECEIVING_UNIT",
            )

        if payload.other_recipient is not None:
            raise AppError(
                "Recipient is not allowed for inbound transaction",
                code="INVALID_RECIPIENT",
            )

    def _validate_outbound(
        self,
        payload: TransactionCreate,
    ) -> None:
        if payload.receiving_unit_id is None and not payload.other_recipient:
            raise AppError(
                "Receiving unit or other recipient is required "
                "for outbound transaction",
                code="RECIPIENT_REQUIRED",
            )

        if payload.receiving_unit_id is not None:
            self._validate_receiving_unit(payload.receiving_unit_id)

        if payload.supplier_id is not None:
            raise AppError(
                "Supplier is not allowed for outbound transaction",
                code="INVALID_SUPPLIER",
            )

        if payload.destination_warehouse_id is not None:
            raise AppError(
                "Destination warehouse is not allowed for outbound transaction",
                code="INVALID_DESTINATION_WAREHOUSE",
            )

    def _validate_transfer(
        self,
        payload: TransactionCreate,
    ) -> None:
        if payload.destination_warehouse_id is None:
            raise AppError(
                "Destination warehouse is required for transfer transaction",
                code="DESTINATION_WAREHOUSE_REQUIRED",
            )

        if payload.warehouse_id == payload.destination_warehouse_id:
            raise AppError(
                "Source and destination warehouses must be different",
                code="INVALID_TRANSFER",
            )

        self._validate_warehouse(payload.destination_warehouse_id)

        if payload.supplier_id is not None:
            raise AppError(
                "Supplier is not allowed for transfer transaction",
                code="INVALID_SUPPLIER",
            )

        if payload.receiving_unit_id is not None:
            raise AppError(
                "Receiving unit is not allowed for transfer transaction",
                code="INVALID_RECEIVING_UNIT",
            )

        if payload.other_recipient is not None:
            raise AppError(
                "Recipient is not allowed for transfer transaction",
                code="INVALID_RECIPIENT",
            )

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

    def _validate_supplier(
        self,
        supplier_id: int,
    ) -> Supplier:
        supplier = self.db.scalar(select(Supplier).where(Supplier.id == supplier_id))

        if supplier is None:
            raise AppError(
                "Supplier not found",
                code="SUPPLIER_NOT_FOUND",
                status_code=404,
            )

        if not supplier.is_active:
            raise AppError(
                "Supplier is inactive",
                code="SUPPLIER_INACTIVE",
            )

        return supplier

    def _validate_receiving_unit(
        self,
        receiving_unit_id: int,
    ) -> ReceivingUnit:
        receiving_unit = self.db.scalar(
            select(ReceivingUnit).where(ReceivingUnit.id == receiving_unit_id)
        )

        if receiving_unit is None:
            raise AppError(
                "Receiving unit not found",
                code="RECEIVING_UNIT_NOT_FOUND",
                status_code=404,
            )

        if not receiving_unit.is_active:
            raise AppError(
                "Receiving unit is inactive",
                code="RECEIVING_UNIT_INACTIVE",
            )

        return receiving_unit

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
                "Material does not belong to transaction warehouse",
                code="MATERIAL_WRONG_WAREHOUSE",
            )

        return material
