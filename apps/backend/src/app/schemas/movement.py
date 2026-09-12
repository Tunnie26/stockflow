from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


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
