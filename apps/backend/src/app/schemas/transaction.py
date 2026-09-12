from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.transaction import TransactionType


class TransactionDetailCreate(BaseModel):
    material_id: int
    quantity: Decimal = Field(gt=0)
    unit_price: Decimal | None = Field(default=None, ge=0)
    note: str | None = Field(default=None, max_length=1000)


class TransactionCreate(BaseModel):
    transaction_type: TransactionType
    warehouse_id: int
    destination_warehouse_id: int | None = None

    supplier_id: int | None = None
    receiving_unit_id: int | None = None
    other_recipient: str | None = Field(default=None, max_length=255)

    transaction_date: date
    note: str | None = Field(default=None, max_length=1000)

    details: list[TransactionDetailCreate] = Field(min_length=1)


class TransactionDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    material_id: int

    sku_snapshot: str
    name_snapshot: str
    unit_snapshot: str
    specification_snapshot: str

    quantity: Decimal
    unit_price: Decimal | None
    total_amount: Decimal | None
    note: str | None


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    transaction_no: int
    transaction_type: TransactionType
    warehouse_id: int
    destination_warehouse_id: int | None

    supplier_id: int | None
    receiving_unit_id: int | None
    other_recipient: str | None

    transaction_date: date
    note: str | None
    created_by: int | None
    created_at: datetime

    details: list[TransactionDetailResponse]


class AdjustmentDetailCreate(BaseModel):
    material_id: int
    actual_quantity: Decimal = Field(ge=0)
    note: str | None = Field(default=None, max_length=1000)


class AdjustmentCreate(BaseModel):
    warehouse_id: int
    transaction_date: date
    reason: str = Field(min_length=1, max_length=1000)
    details: list[AdjustmentDetailCreate] = Field(min_length=1)
