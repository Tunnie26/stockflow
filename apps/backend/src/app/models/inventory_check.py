from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.inventory_check_detail import InventoryCheckDetail


class InventoryCheck(Base):
    __tablename__ = "inventory_checks"

    id: Mapped[int] = mapped_column(primary_key=True)

    check_no: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        nullable=False,
    )

    warehouse_id: Mapped[int] = mapped_column(
        ForeignKey("warehouses.id"),
        nullable=False,
    )

    check_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    note: Mapped[str | None] = mapped_column(
        String(1000),
    )

    adjustment_transaction_id: Mapped[int | None] = mapped_column(
        ForeignKey("transactions.id"),
        nullable=True,
    )

    created_by: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    details: Mapped[list["InventoryCheckDetail"]] = relationship(
        "InventoryCheckDetail",
        back_populates="inventory_check",
        cascade="all, delete-orphan",
    )
