import { apiClient } from "@/lib/api/client";

export interface Warehouse {
  id: number;
  code: string;
  name: string;
  address: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export async function getWarehouses(): Promise<Warehouse[]> {
  return apiClient.get<Warehouse[]>(
    process.env.NEXT_PUBLIC_WAREHOUSES!
  );
}