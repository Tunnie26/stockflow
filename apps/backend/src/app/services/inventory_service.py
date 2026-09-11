from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.stock_balance import StockBalance
from app.models.stock_movement import StockMovement
from app.models.transaction_detail import TransactionDetail


class InventoryService:
    def __init__(self, db: Session):
        self.db = db

    def apply_inbound(
        self,
        transaction_detail: TransactionDetail,
    ) -> StockMovement:
        return self._increase_stock(
            transaction_detail=transaction_detail,
            quantity=transaction_detail.quantity,
        )

    def apply_outbound(
        self,
        transaction_detail: TransactionDetail,
    ) -> StockMovement:
        return self._decrease_stock(
            transaction_detail=transaction_detail,
            quantity=transaction_detail.quantity,
        )

    def apply_transfer(
        self,
        transaction_detail: TransactionDetail,
    ) -> StockMovement:
        return self._decrease_stock(
            transaction_detail=transaction_detail,
            quantity=transaction_detail.quantity,
        )

    def apply_adjustment(
        self,
        transaction_detail: TransactionDetail,
        actual_quantity: Decimal,
    ) -> StockMovement:
        balance = self._get_or_create_balance(
            transaction_detail.material_id,
        )

        difference = actual_quantity - balance.quantity

        balance.quantity = actual_quantity

        movement = StockMovement(
            transaction_id=transaction_detail.transaction_id,
            transaction_detail_id=transaction_detail.id,
            material_id=transaction_detail.material_id,
            quantity=difference,
        )

        self.db.add(movement)
        self.db.flush()

        return movement

    def _increase_stock(
        self,
        transaction_detail: TransactionDetail,
        quantity: Decimal,
    ) -> StockMovement:
        balance = self._get_or_create_balance(
            transaction_detail.material_id,
        )

        balance.quantity += quantity

        movement = StockMovement(
            transaction_id=transaction_detail.transaction_id,
            transaction_detail_id=transaction_detail.id,
            material_id=transaction_detail.material_id,
            quantity=quantity,
        )

        self.db.add(movement)
        self.db.flush()

        return movement

    def _decrease_stock(
        self,
        transaction_detail: TransactionDetail,
        quantity: Decimal,
    ) -> StockMovement:
        balance = self._get_or_create_balance(
            transaction_detail.material_id,
        )

        balance.quantity -= quantity

        movement = StockMovement(
            transaction_id=transaction_detail.transaction_id,
            transaction_detail_id=transaction_detail.id,
            material_id=transaction_detail.material_id,
            quantity=-quantity,
        )

        self.db.add(movement)
        self.db.flush()

        return movement

    def _get_or_create_balance(
        self,
        material_id: int,
    ) -> StockBalance:
        balance = self.db.scalar(
            select(StockBalance).where(StockBalance.material_id == material_id)
        )

        if balance is None:
            balance = StockBalance(
                material_id=material_id,
                quantity=Decimal("0"),
            )
            self.db.add(balance)
            self.db.flush()

        return balance
