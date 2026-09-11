from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import AppError
from app.models.material_category import MaterialCategory
from app.schemas.material_category import MaterialCategoryCreate, MaterialCategoryUpdate


class MaterialCategoryService:
    def __init__(self, db: Session):
        self.db = db

    def create_material_category(
        self,
        data: MaterialCategoryCreate,
    ) -> MaterialCategory:
        existing_category = self.db.scalar(
            select(MaterialCategory).where(MaterialCategory.code == data.code)
        )

        if existing_category is not None:
            raise AppError(
                "Material category code already exists",
                code="MATERIAL_CATEGORY_CODE_ALREADY_EXISTS",
            )

        category = MaterialCategory(
            code=data.code,
            name=data.name,
        )

        self.db.add(category)
        self.db.flush()

        return category

    def list_material_categories(self) -> list[MaterialCategory]:
        statement = select(MaterialCategory).order_by(MaterialCategory.id)

        return list(self.db.scalars(statement).all())

    def get_material_category(
        self,
        category_id: int,
    ) -> MaterialCategory:
        category = self.db.scalar(
            select(MaterialCategory).where(MaterialCategory.id == category_id)
        )

        if category is None:
            raise AppError(
                "Material category not found",
                code="MATERIAL_CATEGORY_NOT_FOUND",
            )

        return category

    def update_material_category(
        self,
        category_id: int,
        data: MaterialCategoryUpdate,
    ) -> MaterialCategory:
        category = self.get_material_category(category_id)

        update_data = data.model_dump(exclude_unset=True)

        if "code" in update_data:
            existing_category = self.db.scalar(
                select(MaterialCategory).where(
                    MaterialCategory.code == update_data["code"],
                    MaterialCategory.id != category.id,
                )
            )

            if existing_category is not None:
                raise AppError(
                    "Material category code already exists",
                    code="MATERIAL_CATEGORY_CODE_ALREADY_EXISTS",
                )

        for field, value in update_data.items():
            setattr(category, field, value)

        self.db.flush()

        return category
