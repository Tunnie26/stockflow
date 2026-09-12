from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import AppError
from app.models.material import Material
from app.models.stock_movement import StockMovement
from app.models.transaction import Transaction
from app.models.transaction_detail import TransactionDetail
from app.models.warehouse import Warehouse
from app.schemas.movement import MovementQueryParams, MovementResponse


class MovementQueryService:
    def __init__(self, db: Session):
        self.db = db

    def list_movements(
        self,
        params: MovementQueryParams,
    ) -> list[MovementResponse]:
        if (
            params.date_from is not None
            and params.date_to is not None
            and params.date_from > params.date_to
        ):
            raise AppError(
                "date_from must be less than or equal to date_to",
                code="INVALID_DATE_RANGE",
                status_code=400,
            )

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
        )

        if params.material_id is not None:
            statement = statement.where(StockMovement.material_id == params.material_id)

        if params.warehouse_id is not None:
            statement = statement.where(Transaction.warehouse_id == params.warehouse_id)

        if params.transaction_type is not None:
            statement = statement.where(
                Transaction.transaction_type == params.transaction_type
            )

        if params.date_from is not None:
            statement = statement.where(
                Transaction.transaction_date >= params.date_from
            )

        if params.date_to is not None:
            statement = statement.where(Transaction.transaction_date <= params.date_to)

        statement = statement.order_by(
            StockMovement.created_at.desc(),
            StockMovement.id.desc(),
        )

        rows = self.db.execute(statement).mappings().all()

        return [MovementResponse.model_validate(row) for row in rows]
