"use client";

import { RefreshCw } from "lucide-react";

import { Button } from "@/components/ui/button";

import { DashboardSummary } from "@/components/dashboard/dashboard-summary";
import DashboardLoading from "@/components/dashboard/dashboard-loading";

import { useDashboardQuery } from "@/features/dashboard/dashboard-query";
import { useWarehouse } from "@/features/warehouses/warehouse-context";
import {
  DashboardInsights,
  RecentActivitySection,
  StockStatusSection,
} from "@/components/dashboard";

export default function DashboardPage() {
  const { currentWarehouseId } = useWarehouse();

  const {
    data: dashboard,
    isLoading,
    isFetching,
    isError,
    refetch,
  } = useDashboardQuery(currentWarehouseId);

  if (isLoading) {
    return (
      <div className="space-y-6 px-[20px] py-[20px]">
        <DashboardLoading />
      </div>
    );
  }

  if (isError || !dashboard) {
    return (
      <div className="flex min-h-[500px] flex-col items-center justify-center gap-4">
        <p className="text-sm text-[#F0526B]">
          Không thể tải dữ liệu Dashboard.
        </p>

        <Button
          type="button"
          variant="outline"
          onClick={() => refetch()}
          className="border-[#2C3A55] bg-[#0D1422] text-[#B8C2D9] hover:bg-[#18253A] hover:text-[#F4F7FF]"
        >
          <RefreshCw className="size-4" />
          Thử lại
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6 px-[20px] py-[20px] pb-8">
      <div className="flex items-end justify-between gap-4">
        <h1 className="text-2xl font-semibold tracking-tight text-[#F4F7FF]">
          Thống kê
        </h1>
        {isFetching && (
          <div className="flex items-center gap-2 text-xs text-[#606C84]">
            <RefreshCw className="size-3.5 animate-spin" /> 
            Đang cập nhật
          </div>
        )}
      </div>

      <DashboardSummary summary={dashboard.summary} />

      <StockStatusSection dashboard={dashboard} />

      <RecentActivitySection dashboard={dashboard} />

      <DashboardInsights dashboard={dashboard} />
    </div>
  );
}
