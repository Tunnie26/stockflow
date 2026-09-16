import { apiClient } from "@/lib/api/client";
import type { DashboardData } from "./dashboard-types";

export async function getDashboard(
  warehouseId: number,
): Promise<DashboardData> {
  return apiClient.get<DashboardData>(
    `/api/v1/dashboard?warehouse_id=${warehouseId}`,
  );
}