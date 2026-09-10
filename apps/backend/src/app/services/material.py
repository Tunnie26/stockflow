from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import AppError
from app.models.location import Location
from app.models.material import Material
from app.models.material_category import MaterialCategory
from app.models.stock_movement import StockMovement
from app.models.warehouse import Warehouse
from app.schemas.material import MaterialCreate, MaterialUpdate


class MaterialService:
    def __init__(self, db: Session):
        self.db = db

    # CREATE

    def create_material(self, data: MaterialCreate) -> Material:
        warehouse = self.db.scalar(
            select(Warehouse).where(Warehouse.id == data.warehouse_id)
        )

        if warehouse is None:
            raise AppError(
                "Warehouse not found",
                code="WAREHOUSE_NOT_FOUND",
            )

        if not warehouse.is_active:
            raise AppError(
                "Warehouse is inactive",
                code="WAREHOUSE_INACTIVE",
            )

        category = self.db.scalar(
            select(MaterialCategory).where(MaterialCategory.id == data.category_id)
        )

        if category is None:
            raise AppError(
                "Material category not found",
                code="CATEGORY_NOT_FOUND",
            )

        if not category.is_active:
            raise AppError(
                "Material category is inactive",
                code="CATEGORY_INACTIVE",
            )

        if data.location_id is not None:
            location = self.db.scalar(
                select(Location).where(Location.id == data.location_id)
            )

            if location is None:
                raise AppError(
                    "Location not found",
                    code="LOCATION_NOT_FOUND",
                )

            if not location.is_active:
                raise AppError(
                    "Location is inactive",
                    code="LOCATION_INACTIVE",
                )

            if location.warehouse_id != data.warehouse_id:
                raise AppError(
                    "Location does not belong to the selected warehouse",
                    code="LOCATION_WAREHOUSE_MISMATCH",
                )

        existing_material = self.db.scalar(
            select(Material).where(
                Material.warehouse_id == data.warehouse_id,
                Material.sku == data.sku,
            )
        )

        if existing_material is not None:
            raise AppError(
                "SKU already exists in this warehouse",
                code="SKU_ALREADY_EXISTS",
            )

        material = Material(
            warehouse_id=data.warehouse_id,
            category_id=data.category_id,
            location_id=data.location_id,
            sku=data.sku,
            name=data.name,
            unit=data.unit,
            specification=data.specification,
            minimum_stock=data.minimum_stock,
            note=data.note,
        )

        self.db.add(material)
        self.db.flush()

        return material

    def list_materials(self) -> list[Material]:
        statement = select(Material).order_by(Material.id)
        return list(self.db.scalars(statement).all())

    def get_material(self, material_id: int) -> Material:
        material = self.db.scalar(select(Material).where(Material.id == material_id))

        if material is None:
            raise AppError(
                "Material not found",
                code="MATERIAL_NOT_FOUND",
            )

        return material

    # UPDATE

    def update_material(
        self,
        material_id: int,
        data: MaterialUpdate,
    ) -> Material:
        material = self.db.scalar(select(Material).where(Material.id == material_id))

        if material is None:
            raise AppError(
                "Material not found",
                code="MATERIAL_NOT_FOUND",
            )

        update_data = data.model_dump(exclude_unset=True)

        if "warehouse_id" in update_data:
            warehouse_id = update_data["warehouse_id"]

            warehouse = self.db.scalar(
                select(Warehouse).where(Warehouse.id == warehouse_id)
            )

            if warehouse is None:
                raise AppError(
                    "Warehouse not found",
                    code="WAREHOUSE_NOT_FOUND",
                )

            if not warehouse.is_active:
                raise AppError(
                    "Warehouse is inactive",
                    code="WAREHOUSE_INACTIVE",
                )

            if warehouse_id != material.warehouse_id:
                has_movement = self.db.scalar(
                    select(StockMovement.id)
                    .where(StockMovement.material_id == material.id)
                    .limit(1)
                )

                if has_movement is not None:
                    raise AppError(
                        "Material warehouse cannot be changed after inventory history exists",
                        code="MATERIAL_WAREHOUSE_CHANGE_FORBIDDEN",
                    )

        warehouse_id = update_data.get(
            "warehouse_id",
            material.warehouse_id,
        )

        if "category_id" in update_data:
            category = self.db.scalar(
                select(MaterialCategory).where(
                    MaterialCategory.id == update_data["category_id"]
                )
            )

            if category is None:
                raise AppError(
                    "Material category not found",
                    code="CATEGORY_NOT_FOUND",
                )

            if not category.is_active:
                raise AppError(
                    "Material category is inactive",
                    code="CATEGORY_INACTIVE",
                )

        if "location_id" in update_data:
            location_id = update_data["location_id"]

            if location_id is not None:
                location = self.db.scalar(
                    select(Location).where(Location.id == location_id)
                )

                if location is None:
                    raise AppError(
                        "Location not found",
                        code="LOCATION_NOT_FOUND",
                    )

                if not location.is_active:
                    raise AppError(
                        "Location is inactive",
                        code="LOCATION_INACTIVE",
                    )

                if location.warehouse_id != warehouse_id:
                    raise AppError(
                        "Location does not belong to the selected warehouse",
                        code="LOCATION_WAREHOUSE_MISMATCH",
                    )

        if "sku" in update_data:
            new_sku = update_data["sku"]

            existing_material = self.db.scalar(
                select(Material).where(
                    Material.warehouse_id == warehouse_id,
                    Material.sku == new_sku,
                    Material.id != material.id,
                )
            )

            if existing_material is not None:
                raise AppError(
                    "SKU already exists in this warehouse",
                    code="SKU_ALREADY_EXISTS",
                )

        for field, value in update_data.items():
            setattr(material, field, value)

        self.db.flush()

        return material
