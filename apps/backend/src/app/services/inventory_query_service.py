from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import AppError
from app.models.location import Location
from app.models.material import Material
from app.models.stock_balance import StockBalance
from app.models.warehouse import Warehouse
from app.schemas.inventory import InventoryResponse


class InventoryQueryService:
    def __init__(self, db: Session):
        self.db = db

    def list_inventory(self) -> list[InventoryResponse]:
        statement = (
            select(
                Material.id.label("material_id"),
                Material.sku,
                Material.name,
                Material.unit,
                Warehouse.id.label("warehouse_id"),
                Warehouse.code.label("warehouse_code"),
                Warehouse.name.label("warehouse_name"),
                Location.id.label("location_id"),
                Location.code.label("location_code"),
                StockBalance.quantity,
                Material.minimum_stock,
                Material.is_active,
            )
            .join(Warehouse, Warehouse.id == Material.warehouse_id)
            .outerjoin(Location, Location.id == Material.location_id)
            .outerjoin(
                StockBalance,
                StockBalance.material_id == Material.id,
            )
            .order_by(Material.id)
        )

        rows = self.db.execute(statement).mappings().all()

        result = []

        for row in rows:
            data = dict(row)

            if data["quantity"] is None:
                data["quantity"] = Decimal("0")

            result.append(InventoryResponse.model_validate(data))

        return result

    def get_inventory(self, material_id: int) -> InventoryResponse:
        statement = (
            select(
                Material.id.label("material_id"),
                Material.sku,
                Material.name,
                Material.unit,
                Warehouse.id.label("warehouse_id"),
                Warehouse.code.label("warehouse_code"),
                Warehouse.name.label("warehouse_name"),
                Location.id.label("location_id"),
                Location.code.label("location_code"),
                StockBalance.quantity,
                Material.minimum_stock,
                Material.is_active,
            )
            .join(Warehouse, Warehouse.id == Material.warehouse_id)
            .outerjoin(Location, Location.id == Material.location_id)
            .outerjoin(
                StockBalance,
                StockBalance.material_id == Material.id,
            )
            .where(Material.id == material_id)
        )

        row = self.db.execute(statement).mappings().first()

        if row is None:
            raise AppError(
                "Material not found",
                code="NOT_FOUND",
                status_code=404,
            )

        data = dict(row)

        if data["quantity"] is None:
            data["quantity"] = Decimal("0")

        return InventoryResponse.model_validate(data)
