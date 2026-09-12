from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.material import Material
from app.models.stock_movement import StockMovement
from app.models.transaction import Transaction
from app.models.transaction_detail import TransactionDetail
from app.models.warehouse import Warehouse
from app.schemas.movement import MovementResponse


class MovementQueryService:
    def __init__(self, db: Session):
        self.db = db

    def list_movements(self) -> list[MovementResponse]:
        statement = (
            select(
                StockMovement.id.label("movement_id"),
                StockMovement.transaction_id,
                Transaction.transaction_no,
                Transaction.transaction_type,
                Transaction.transaction_date,
                StockMovement.material_id,
                TransactionDetail.sku_snapshot.label("sku"),
                TransactionDetail.name_snapshot.label("name"),
                TransactionDetail.unit_snapshot.label("unit"),
                Warehouse.id.label("warehouse_id"),
                Warehouse.code.label("warehouse_code"),
                StockMovement.quantity,
                StockMovement.created_at,
            )
            .join(
                Transaction,
                Transaction.id == StockMovement.transaction_id,
            )
            .join(
                TransactionDetail,
                TransactionDetail.id == StockMovement.transaction_detail_id,
            )
            .join(
                Material,
                Material.id == StockMovement.material_id,
            )
            .join(
                Warehouse,
                Warehouse.id == Transaction.warehouse_id,
            )
            .order_by(
                StockMovement.created_at.desc(),
                StockMovement.id.desc(),
            )
        )

        rows = self.db.execute(statement).mappings().all()

        return [MovementResponse.model_validate(row) for row in rows]
