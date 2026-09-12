from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import AppError
from app.models.customer import Customer
from app.models.location import Location
from app.models.material import Material
from app.models.material_category import MaterialCategory
from app.models.stock_movement import StockMovement
from app.models.warehouse import Warehouse
from app.schemas.material import MaterialCreate, MaterialResponse, MaterialUpdate


class MaterialService:
    def __init__(self, db: Session):
        self.db = db

    def _get_active_customers(
        self,
        customer_ids: list[int],
    ) -> list[Customer]:
        if not customer_ids:
            return []

        customers = list(
            self.db.scalars(
                select(Customer).where(
                    Customer.id.in_(customer_ids),
                    Customer.is_active.is_(True),
                )
            ).all()
        )

        found_ids = {customer.id for customer in customers}
        missing_ids = set(customer_ids) - found_ids

        if missing_ids:
            raise AppError(
                f"Customer not found or inactive: {sorted(missing_ids)}",
                code="CUSTOMER_NOT_FOUND",
                status_code=404,
            )

        return customers

    # CREATE

    def create_material(self, data: MaterialCreate) -> Material:
        warehouse = self.db.scalar(
            select(Warehouse).where(
                Warehouse.id == data.warehouse_id,
            )
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
            select(MaterialCategory).where(
                MaterialCategory.id == data.category_id,
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

        if data.location_id is not None:
            location = self.db.scalar(
                select(Location).where(
                    Location.id == data.location_id,
                )
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

        customers = self._get_active_customers(data.customer_ids)

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

        material.customers = customers

        self.db.add(material)
        self.db.flush()

        return material

    def list_materials(self) -> list[Material]:
        statement = select(Material).order_by(Material.id)

        return list(self.db.scalars(statement).all())

    def get_material(self, material_id: int) -> Material:
        material = self.db.scalar(
            select(Material).where(
                Material.id == material_id,
            )
        )

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
        material = self.db.scalar(
            select(Material).where(
                Material.id == material_id,
            )
        )

        if material is None:
            raise AppError(
                "Material not found",
                code="MATERIAL_NOT_FOUND",
            )

        update_data = data.model_dump(exclude_unset=True)

        # Validate warehouse

        if "warehouse_id" in update_data:
            warehouse_id = update_data["warehouse_id"]

            warehouse = self.db.scalar(
                select(Warehouse).where(
                    Warehouse.id == warehouse_id,
                )
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
                    .where(
                        StockMovement.material_id == material.id,
                    )
                    .limit(1)
                )

                if has_movement is not None:
                    raise AppError(
                        "Material warehouse cannot be changed after "
                        "inventory history exists",
                        code="MATERIAL_WAREHOUSE_CHANGE_FORBIDDEN",
                    )

        warehouse_id = update_data.get(
            "warehouse_id",
            material.warehouse_id,
        )

        # Validate category

        if "category_id" in update_data:
            category = self.db.scalar(
                select(MaterialCategory).where(
                    MaterialCategory.id == update_data["category_id"],
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

        # Validate location

        if "location_id" in update_data:
            location_id = update_data["location_id"]

            if location_id is not None:
                location = self.db.scalar(
                    select(Location).where(
                        Location.id == location_id,
                    )
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

        # Validate SKU

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

        # Validate Customer association

        if "customer_ids" in update_data:
            customer_ids = update_data.pop("customer_ids")

            customers = self._get_active_customers(customer_ids)

            material.customers = customers

        # Update normal Material fields

        for field, value in update_data.items():
            setattr(material, field, value)

        self.db.flush()

        return material


def to_response(material: Material) -> MaterialResponse:
    return MaterialResponse(
        id=material.id,
        warehouse_id=material.warehouse_id,
        category_id=material.category_id,
        location_id=material.location_id,
        customer_ids=[customer.id for customer in material.customers],
        sku=material.sku,
        name=material.name,
        unit=material.unit,
        specification=material.specification,
        minimum_stock=material.minimum_stock,
        note=material.note,
        is_active=material.is_active,
        created_at=material.created_at,
        updated_at=material.updated_at,
    )
