from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MaterialCreate(BaseModel):
    warehouse_id: int
    category_id: int
    location_id: int | None = None
    customer_ids: list[int] = Field(default_factory=list)

    sku: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=255)
    unit: str = Field(min_length=1, max_length=50)
    specification: str = Field(min_length=1, max_length=500)

    minimum_stock: Decimal = Field(default=Decimal("0"), ge=0)
    note: str | None = Field(default=None, max_length=1000)

    @field_validator("customer_ids")
    @classmethod
    def validate_customer_ids(cls, value: list[int]) -> list[int]:
        if len(value) != len(set(value)):
            raise ValueError("customer_ids must not contain duplicates")

        if any(customer_id <= 0 for customer_id in value):
            raise ValueError("customer_ids must contain positive integers")

        return value


class MaterialUpdate(BaseModel):
    warehouse_id: int | None = None
    category_id: int | None = None
    location_id: int | None = None
    customer_ids: list[int] | None = None

    sku: str | None = Field(default=None, min_length=1, max_length=100)
    name: str | None = Field(default=None, min_length=1, max_length=255)
    specification: str | None = Field(default=None, min_length=1, max_length=500)

    minimum_stock: Decimal | None = Field(default=None, ge=0)
    note: str | None = Field(default=None, max_length=1000)
    is_active: bool | None = None

    @field_validator("customer_ids")
    @classmethod
    def validate_customer_ids(cls, value: list[int] | None) -> list[int] | None:
        if value is None:
            return None

        if len(value) != len(set(value)):
            raise ValueError("customer_ids must not contain duplicates")

        if any(customer_id <= 0 for customer_id in value):
            raise ValueError("customer_ids must contain positive integers")

        return value


class MaterialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    warehouse_id: int
    category_id: int
    location_id: int | None
    customer_ids: list[int]

    sku: str
    name: str
    unit: str
    specification: str

    minimum_stock: Decimal
    note: str | None
    is_active: bool

    created_at: datetime
    updated_at: datetime
