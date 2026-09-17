export interface DashboardWarehouse {
  id: number;
  code: string;
  name: string;
}

export interface DashboardSummary {
  total_sku: number;
  stock_danger: number;
  stock_warning: number;
  inbound_this_month: number;
  outbound_this_month: number;
}

export interface DashboardStockItem {
  material_id: number;
  sku: string;
  name: string;
  unit: string;
  specification: string;
  quantity: string;
  minimum_stock: string;
  location_code: string | null;
}

export interface DashboardLongTimeNoOutbound {
  material_id: number;
  sku: string;
  name: string;
  unit: string;
  quantity: string;
  last_outbound_date: string | null;
  days_since_last_outbound: number | null;
}

export interface DashboardTransaction {
  transaction_id: number;
  transaction_no: number;
  transaction_type: string;
  transaction_date: string;
  created_at: string;
}

export interface DashboardTopUsedMaterial {
  material_id: number;
  sku: string;
  name: string;
  unit: string;
  outbound_count: number;
}

export interface DashboardData {
  warehouse: DashboardWarehouse;
  summary: DashboardSummary;
  stock_danger_items: DashboardStockItem[];
  stock_warning_items: DashboardStockItem[];
  long_time_no_outbound: DashboardLongTimeNoOutbound[];
  recent_inbound: DashboardTransaction[];
  recent_activities: DashboardTransaction[];
  top_used_materials: DashboardTopUsedMaterial[];
}