from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.transaction import Transaction


class TransactionDetail(Base):
    __tablename__ = "transaction_details"

    id: Mapped[int] = mapped_column(primary_key=True)

    transaction_id: Mapped[int] = mapped_column(
        ForeignKey("transactions.id", ondelete="CASCADE"),
        nullable=False,
    )

    material_id: Mapped[int] = mapped_column(
        ForeignKey("materials.id"),
        nullable=False,
    )

    sku_snapshot: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    name_snapshot: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    unit_snapshot: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    specification_snapshot: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 4),
        nullable=False,
    )

    unit_price: Mapped[Decimal | None] = mapped_column(
        Numeric(20, 2),
        nullable=True,
    )

    total_amount: Mapped[Decimal | None] = mapped_column(
        Numeric(20, 2),
        nullable=True,
    )

    note: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    transaction: Mapped["Transaction"] = relationship(
        back_populates="details",
    )
