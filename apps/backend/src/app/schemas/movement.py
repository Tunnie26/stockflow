from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field, model_validator

from app.models.transaction import TransactionType


class MovementResponse(BaseModel):
    movement_id: int

    transaction_id: int
    transaction_no: int
    transaction_type: str
    transaction_date: date

    material_id: int
    sku: str
    name: str
    unit: str

    warehouse_id: int
    warehouse_code: str

    quantity: Decimal
    created_at: datetime


class MovementQueryParams(BaseModel):
    material_id: int | None = Field(default=None, gt=0)
    warehouse_id: int | None = Field(default=None, gt=0)
    transaction_type: TransactionType | None = None
    date_from: date | None = None
    date_to: date | None = None

    @model_validator(mode="after")
    def validate_date_range(self):
        if (
            self.date_from is not None
            and self.date_to is not None
            and self.date_from > self.date_to
        ):
            raise ValueError("date_from must be less than or equal to date_to")

        return self
