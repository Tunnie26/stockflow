import { useQuery } from "@tanstack/react-query";

import { getDashboard } from "./dashboard-service";

export const dashboardQueryKeys = {
  all: ["dashboard"] as const,

  detail: (warehouseId: number) =>
    [...dashboardQueryKeys.all, warehouseId] as const,
};

export function useDashboardQuery(warehouseId: number | null) {
  return useQuery({
    queryKey:
      warehouseId === null
        ? dashboardQueryKeys.all
        : dashboardQueryKeys.detail(warehouseId),

    queryFn: () => {
      if (warehouseId === null) {
        throw new Error("Warehouse ID is required");
      }

      return getDashboard(warehouseId);
    },

    enabled: warehouseId !== null,
  });
}
