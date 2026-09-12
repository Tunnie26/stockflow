from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class InventoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    material_id: int
    sku: str
    name: str
    unit: str

    warehouse_id: int
    warehouse_code: str
    warehouse_name: str

    location_id: int | None
    location_code: str | None

    quantity: Decimal
    minimum_stock: Decimal
    is_active: bool


class InventoryQueryParams(BaseModel):
    warehouse_id: int | None = Field(default=None, gt=0)
    category_id: int | None = Field(default=None, gt=0)
    customer_id: int | None = Field(default=None, gt=0)
    search: str | None = Field(default=None, min_length=1)
    low_stock: bool | None = None
