from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Numeric,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.customer import Customer


class Material(Base):
    __tablename__ = "materials"

    __table_args__ = (
        UniqueConstraint(
            "warehouse_id",
            "sku",
            name="uq_materials_warehouse_sku",
        ),
        ForeignKeyConstraint(
            ["warehouse_id", "location_id"],
            ["locations.warehouse_id", "locations.id"],
            name="fk_materials_warehouse_location",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    warehouse_id: Mapped[int] = mapped_column(
        ForeignKey("warehouses.id"),
        nullable=False,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("material_categories.id"),
        nullable=False,
    )

    location_id: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    sku: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    unit: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    specification: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    minimum_stock: Mapped[Decimal] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        default=0,
    )

    note: Mapped[str | None] = mapped_column(
        String(1000),
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    customers: Mapped[list["Customer"]] = relationship(
        "Customer",
        secondary="material_customers",
        back_populates="materials",
    )
