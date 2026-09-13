from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class InventoryCheckDetailCreate(BaseModel):
    material_id: int = Field(gt=0)
    actual_quantity: Decimal = Field(ge=0)
    note: str | None = Field(default=None, max_length=1000)


class InventoryCheckCreate(BaseModel):
    warehouse_id: int = Field(gt=0)
    check_date: date
    note: str | None = Field(default=None, max_length=1000)
    details: list[InventoryCheckDetailCreate] = Field(min_length=1)


class InventoryCheckDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    material_id: int
    sku: str
    name: str
    unit: str
    system_quantity: Decimal
    actual_quantity: Decimal
    difference: Decimal
    note: str | None


class InventoryCheckResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    check_no: int
    warehouse_id: int
    check_date: date
    note: str | None
    adjustment_transaction_id: int | None
    created_by: int | None
    created_at: datetime
    details: list[InventoryCheckDetailResponse]
