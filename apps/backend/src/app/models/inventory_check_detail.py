from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.inventory_check import InventoryCheck


class InventoryCheckDetail(Base):
    __tablename__ = "inventory_check_details"

    __table_args__ = (
        UniqueConstraint(
            "inventory_check_id",
            "material_id",
            name="uq_inventory_check_details_check_material",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    inventory_check_id: Mapped[int] = mapped_column(
        ForeignKey(
            "inventory_checks.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    material_id: Mapped[int] = mapped_column(
        ForeignKey("materials.id"),
        nullable=False,
    )

    system_quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 4),
        nullable=False,
    )

    actual_quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 4),
        nullable=False,
    )

    difference: Mapped[Decimal] = mapped_column(
        Numeric(18, 4),
        nullable=False,
    )

    note: Mapped[str | None] = mapped_column(
        String(1000),
    )

    inventory_check: Mapped["InventoryCheck"] = relationship(
        "InventoryCheck",
        back_populates="details",
    )
