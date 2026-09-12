from decimal import Decimal

from sqlalchemy import exists, func, or_, select
from sqlalchemy.orm import Session

from app.exceptions import AppError
from app.models.location import Location
from app.models.material import Material
from app.models.material_customer import MaterialCustomer
from app.models.stock_balance import StockBalance
from app.models.warehouse import Warehouse
from app.schemas.inventory import InventoryQueryParams, InventoryResponse


class InventoryQueryService:
    def __init__(self, db: Session):
        self.db = db

    def list_inventory(
        self,
        params: InventoryQueryParams,
    ) -> list[InventoryResponse]:
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
                Warehouse.id.label("warehouse_id"),
                Warehouse.code.label("warehouse_code"),
                Warehouse.name.label("warehouse_name"),
                Location.id.label("location_id"),
                Location.code.label("location_code"),
                quantity.label("quantity"),
                Material.minimum_stock,
                Material.is_active,
            )
            .join(
                Warehouse,
                Warehouse.id == Material.warehouse_id,
            )
            .outerjoin(
                Location,
                Location.id == Material.location_id,
            )
            .outerjoin(
                StockBalance,
                StockBalance.material_id == Material.id,
            )
        )

        if params.warehouse_id is not None:
            statement = statement.where(Material.warehouse_id == params.warehouse_id)

        if params.category_id is not None:
            statement = statement.where(Material.category_id == params.category_id)

        if params.customer_id is not None:
            statement = statement.where(
                exists().where(
                    MaterialCustomer.material_id == Material.id,
                    MaterialCustomer.customer_id == params.customer_id,
                )
            )

        if params.search is not None:
            search_pattern = f"%{params.search}%"

            statement = statement.where(
                or_(
                    Material.sku.ilike(search_pattern),
                    Material.name.ilike(search_pattern),
                )
            )

        if params.low_stock is True:
            statement = statement.where(quantity <= Material.minimum_stock)

        statement = statement.order_by(Material.id)

        rows = self.db.execute(statement).mappings().all()

        return [InventoryResponse.model_validate(row) for row in rows]

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
