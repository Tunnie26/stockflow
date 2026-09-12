from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class DashboardWarehouseResponse(BaseModel):
    id: int
    code: str
    name: str


class DashboardSummaryResponse(BaseModel):
    total_sku: int
    stock_danger: int
    stock_warning: int


class DashboardStockItemResponse(BaseModel):
    material_id: int
    sku: str
    name: str
    unit: str
    quantity: Decimal
    minimum_stock: Decimal
    location_code: str | None


class DashboardLongTimeNoOutboundResponse(BaseModel):
    material_id: int
    sku: str
    name: str
    unit: str
    quantity: Decimal
    last_outbound_date: date | None
    days_since_last_outbound: int | None


class DashboardTransactionResponse(BaseModel):
    transaction_id: int
    transaction_no: int
    transaction_type: str
    transaction_date: date
    created_at: datetime


class DashboardTopUsedMaterialResponse(BaseModel):
    material_id: int
    sku: str
    name: str
    unit: str
    outbound_count: int


class DashboardResponse(BaseModel):
    warehouse: DashboardWarehouseResponse
    summary: DashboardSummaryResponse
    stock_danger_items: list[DashboardStockItemResponse]
    stock_warning_items: list[DashboardStockItemResponse]
    long_time_no_outbound: list[DashboardLongTimeNoOutboundResponse]
    recent_inbound: list[DashboardTransactionResponse]
    recent_activities: list[DashboardTransactionResponse]
    top_used_materials: list[DashboardTopUsedMaterialResponse]
