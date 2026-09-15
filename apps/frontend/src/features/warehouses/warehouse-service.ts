import { apiClient } from "@/lib/api/client";

export interface Warehouse {
  id: number;
  code: string;
  name: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export async function getWarehouses(token: string): Promise<Warehouse[]> {
  return apiClient.get<Warehouse[]>("/api/v1/warehouses", {
    token,
  });
}