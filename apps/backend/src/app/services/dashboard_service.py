from datetime import date
from decimal import Decimal

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.exceptions import AppError
from app.models.location import Location
from app.models.material import Material
from app.models.stock_balance import StockBalance
from app.models.stock_movement import StockMovement
from app.models.transaction import Transaction, TransactionType
from app.models.transaction_detail import TransactionDetail
from app.models.warehouse import Warehouse
from app.schemas.dashboard import (
    DashboardLongTimeNoOutboundResponse,
    DashboardResponse,
    DashboardStockItemResponse,
    DashboardSummaryResponse,
    DashboardTopUsedMaterialResponse,
    DashboardTransactionResponse,
    DashboardWarehouseResponse,
)


class DashboardQueryService:
    def __init__(self, db: Session):
        self.db = db

    def get_dashboard(self, warehouse_id: int) -> DashboardResponse:
        warehouse = self._get_warehouse(warehouse_id)

        return DashboardResponse(
            warehouse=DashboardWarehouseResponse(
                id=warehouse.id,
                code=warehouse.code,
                name=warehouse.name,
            ),
            summary=self._get_summary(warehouse.id),
            stock_danger_items=self._get_stock_danger(warehouse.id),
            stock_warning_items=self._get_stock_warning(warehouse.id),
            long_time_no_outbound=self._get_long_time_no_outbound(warehouse.id),
            recent_inbound=self._get_recent_inbound(warehouse.id),
            recent_activities=self._get_recent_activities(warehouse.id),
            top_used_materials=self._get_top_used_materials(warehouse.id),
        )

    def _get_warehouse(self, warehouse_id: int) -> Warehouse:
        statement = select(Warehouse).where(
            Warehouse.id == warehouse_id,
            Warehouse.is_active.is_(True),
        )

        warehouse = self.db.execute(statement).scalar_one_or_none()

        if warehouse is None:
            raise AppError(
                "Warehouse not found",
                code="WAREHOUSE_NOT_FOUND",
                status_code=404,
            )

        return warehouse

    def _get_summary(self, warehouse_id: int) -> DashboardSummaryResponse:
        quantity = func.coalesce(
            StockBalance.quantity,
            Decimal("0"),
        )

        today = date.today()
        first_day_of_month = today.replace(day=1)

        if today.month == 12:
            first_day_of_next_month = date(
                today.year + 1,
                1,
                1,
            )
        else:
            first_day_of_next_month = date(
                today.year,
                today.month + 1,
                1,
            )

        inbound_this_month = (
            select(func.count(Transaction.id))
            .where(
                Transaction.warehouse_id == warehouse_id,
                Transaction.transaction_type == TransactionType.INBOUND,
                Transaction.transaction_date >= first_day_of_month,
                Transaction.transaction_date < first_day_of_next_month,
            )
            .scalar_subquery()
        )

        outbound_this_month = (
            select(func.count(Transaction.id))
            .where(
                Transaction.warehouse_id == warehouse_id,
                Transaction.transaction_type == TransactionType.OUTBOUND,
                Transaction.transaction_date >= first_day_of_month,
                Transaction.transaction_date < first_day_of_next_month,
            )
            .scalar_subquery()
        )

        statement = (
            select(
                func.count(Material.id).label("total_sku"),
                func.count(
                    case(
                        (quantity <= Material.minimum_stock, 1),
                    )
                ).label("stock_danger"),
                func.count(
                    case(
                        (
                            (Material.minimum_stock > 0)
                            & (quantity > Material.minimum_stock)
                            & (quantity <= Material.minimum_stock * Decimal("1.20")),
                            1,
                        )
                    )
                ).label("stock_warning"),
                inbound_this_month.label("inbound_this_month"),
                outbound_this_month.label("outbound_this_month"),
            )
            .select_from(Material)
            .outerjoin(
                StockBalance,
                StockBalance.material_id == Material.id,
            )
            .where(
                Material.warehouse_id == warehouse_id,
                Material.is_active.is_(True),
            )
        )

        row = self.db.execute(statement).one()

        return DashboardSummaryResponse(
            total_sku=row.total_sku,
            stock_danger=row.stock_danger,
            stock_warning=row.stock_warning,
            inbound_this_month=row.inbound_this_month,
            outbound_this_month=row.outbound_this_month,
        )

    def _get_stock_danger(
        self,
        warehouse_id: int,
    ) -> list[DashboardStockItemResponse]:
        quantity = func.coalesce(
            StockBalance.quantity,
            Decimal("0"),
        )

        statement = (
            select(
                Material.id.label("material_id"),
                Material.sku,
                Material.name,
                Material.unit,
                Material.specification,
                quantity.label("quantity"),
                Material.minimum_stock,
                Location.code.label("location_code"),
            )
            .select_from(Material)
            .outerjoin(
                StockBalance,
                StockBalance.material_id == Material.id,
            )
            .outerjoin(
                Location,
                Location.id == Material.location_id,
            )
            .where(
                Material.warehouse_id == warehouse_id,
                Material.is_active.is_(True),
                quantity <= Material.minimum_stock,
            )
            .order_by(
                quantity.asc(),
                Material.id.asc(),
            )
            .limit(5)
        )

        rows = self.db.execute(statement).mappings().all()

        return [DashboardStockItemResponse.model_validate(row) for row in rows]

    def _get_stock_warning(
        self,
        warehouse_id: int,
    ) -> list[DashboardStockItemResponse]:
        quantity = func.coalesce(
            StockBalance.quantity,
            Decimal("0"),
        )

        warning_limit = Material.minimum_stock * Decimal("1.20")

        statement = (
            select(
                Material.id.label("material_id"),
                Material.sku,
                Material.name,
                Material.unit,
                Material.specification,
                quantity.label("quantity"),
                Material.minimum_stock,
                Location.code.label("location_code"),
            )
            .select_from(Material)
            .outerjoin(
                StockBalance,
                StockBalance.material_id == Material.id,
            )
            .outerjoin(
                Location,
                Location.id == Material.location_id,
            )
            .where(
                Material.warehouse_id == warehouse_id,
                Material.is_active.is_(True),
                Material.minimum_stock > 0,
                quantity > Material.minimum_stock,
                quantity <= warning_limit,
            )
            .order_by(
                (quantity - Material.minimum_stock).asc(),
                Material.id.asc(),
            )
            .limit(5)
        )

        rows = self.db.execute(statement).mappings().all()

        return [DashboardStockItemResponse.model_validate(row) for row in rows]

    def _get_long_time_no_outbound(
        self,
        warehouse_id: int,
    ) -> list[DashboardLongTimeNoOutboundResponse]:
        latest_outbound = (
            select(
                StockMovement.material_id,
                func.max(Transaction.transaction_date).label("last_outbound_date"),
            )
            .join(
                Transaction,
                Transaction.id == StockMovement.transaction_id,
            )
            .where(
                Transaction.warehouse_id == warehouse_id,
                Transaction.transaction_type == TransactionType.OUTBOUND,
            )
            .group_by(
                StockMovement.material_id,
            )
            .subquery()
        )

        quantity = func.coalesce(
            StockBalance.quantity,
            Decimal("0"),
        )

        statement = (
            select(
                Material.id.label("material_id"),
                Material.sku,
                Material.name,
                Material.unit,
                quantity.label("quantity"),
                latest_outbound.c.last_outbound_date,
            )
            .select_from(Material)
            .outerjoin(
                StockBalance,
                StockBalance.material_id == Material.id,
            )
            .outerjoin(
                latest_outbound,
                latest_outbound.c.material_id == Material.id,
            )
            .where(
                Material.warehouse_id == warehouse_id,
                Material.is_active.is_(True),
            )
            .order_by(
                latest_outbound.c.last_outbound_date.asc().nullsfirst(),
                Material.id.asc(),
            )
            .limit(5)
        )

        rows = self.db.execute(statement).mappings().all()

        today = date.today()

        return [
            DashboardLongTimeNoOutboundResponse(
                material_id=row["material_id"],
                sku=row["sku"],
                name=row["name"],
                unit=row["unit"],
                quantity=row["quantity"],
                last_outbound_date=row["last_outbound_date"],
                days_since_last_outbound=(
                    (today - row["last_outbound_date"]).days
                    if row["last_outbound_date"] is not None
                    else None
                ),
            )
            for row in rows
        ]

    def _get_recent_inbound(
        self,
        warehouse_id: int,
    ) -> list[DashboardTransactionResponse]:
        statement = (
            select(
                Transaction.id.label("transaction_id"),
                Transaction.transaction_no,
                Transaction.transaction_type,
                Transaction.transaction_date,
                Transaction.created_at,
            )
            .where(
                Transaction.warehouse_id == warehouse_id,
                Transaction.transaction_type == TransactionType.INBOUND,
            )
            .order_by(
                Transaction.created_at.desc(),
                Transaction.id.desc(),
            )
            .limit(5)
        )

        rows = self.db.execute(statement).mappings().all()

        return [DashboardTransactionResponse.model_validate(row) for row in rows]

    def _get_recent_activities(
        self,
        warehouse_id: int,
    ) -> list[DashboardTransactionResponse]:
        statement = (
            select(
                Transaction.id.label("transaction_id"),
                Transaction.transaction_no,
                Transaction.transaction_type,
                Transaction.transaction_date,
                Transaction.created_at,
            )
            .where(
                Transaction.warehouse_id == warehouse_id,
                Transaction.transaction_type.in_(
                    [
                        TransactionType.OUTBOUND,
                        TransactionType.TRANSFER,
                        TransactionType.ADJUSTMENT,
                    ]
                ),
            )
            .order_by(
                Transaction.created_at.desc(),
                Transaction.id.desc(),
            )
            .limit(5)
        )

        rows = self.db.execute(statement).mappings().all()

        return [DashboardTransactionResponse.model_validate(row) for row in rows]

    def _get_top_used_materials(
        self,
        warehouse_id: int,
    ) -> list[DashboardTopUsedMaterialResponse]:
        statement = (
            select(
                Material.id.label("material_id"),
                Material.sku,
                Material.name,
                Material.unit,
                func.count(func.distinct(Transaction.id)).label("outbound_count"),
            )
            .select_from(Material)
            .join(
                TransactionDetail,
                TransactionDetail.material_id == Material.id,
            )
            .join(
                Transaction,
                Transaction.id == TransactionDetail.transaction_id,
            )
            .where(
                Material.warehouse_id == warehouse_id,
                Material.is_active.is_(True),
                Transaction.warehouse_id == warehouse_id,
                Transaction.transaction_type == TransactionType.OUTBOUND,
            )
            .group_by(
                Material.id,
                Material.sku,
                Material.name,
                Material.unit,
            )
            .order_by(
                func.count(func.distinct(Transaction.id)).desc(),
                Material.id.asc(),
            )
            .limit(5)
        )

        rows = self.db.execute(statement).mappings().all()

        return [DashboardTopUsedMaterialResponse.model_validate(row) for row in rows]
