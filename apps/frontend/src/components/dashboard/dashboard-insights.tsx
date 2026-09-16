import { Clock3, TrendingUp } from "lucide-react";

import type { DashboardData } from "@/features/dashboard/dashboard-types";
import { DataList } from "@/components/shared/data-list";
import { DataPanel } from "@/components/shared/data-panel";
import { EmptyState } from "@/components/shared/empty-state";

interface DashboardInsightsProps {
  dashboard: DashboardData;
}

function formatDate(value: string | null) {
  if (!value) {
    return "Chưa từng xuất";
  }

  return new Intl.DateTimeFormat("vi-VN", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  }).format(new Date(value));
}

export function DashboardInsights({ dashboard }: DashboardInsightsProps) {
  const { long_time_no_outbound, top_used_materials } = dashboard;

  return (
    <section className="grid grid-cols-1 gap-4 xl:grid-cols-2">
      {/* Long Time No Outbound */}
      <DataPanel
        title="Không xuất lâu ngày"
        description="Các SKU chưa phát sinh xuất kho trong thời gian dài"
        icon={Clock3}
      >
        <DataList
          items={long_time_no_outbound}
          keyExtractor={(item) => item.material_id}
          emptyState={
            <EmptyState
              title="Không có dữ liệu"
              description="Hiện chưa có SKU nào cần theo dõi."
            />
          }
          renderItem={(item) => (
            <div className="flex items-center justify-between gap-4 rounded-xl border border-[#202C43] bg-[#090E1A] px-4 py-3 transition-colors hover:bg-[rgba(79,124,255,0.04)]">
              <div className="min-w-0">
                <p className="truncate text-sm font-medium text-[#F4F7FF]">
                  {item.name}
                </p>

                <div className="mt-1 flex items-center gap-2 text-xs text-[#8490A8]">
                  <span>{item.sku}</span>

                  <span className="text-[#4B556B]">•</span>

                  <span>{item.unit}</span>
                </div>
              </div>

              <div className="shrink-0 text-right">
                {item.days_since_last_outbound !== null ? (
                  <>
                    <p className="text-sm font-semibold text-[#F5B82E]">
                      {item.days_since_last_outbound} ngày
                    </p>

                    <p className="mt-1 text-xs text-[#606C84]">
                      {formatDate(item.last_outbound_date)}
                    </p>
                  </>
                ) : (
                  <>
                    <p className="text-sm font-semibold text-[#F5B82E]">
                      Chưa xuất
                    </p>

                    <p className="mt-1 text-xs text-[#606C84]">
                      Chưa từng xuất kho
                    </p>
                  </>
                )}
              </div>
            </div>
          )}
        />
      </DataPanel>

      {/* Top Used Materials */}
      <DataPanel
        title="Top vật tư sử dụng"
        description="Các vật tư có số lần xuất kho cao nhất"
        icon={TrendingUp}
      >
        <DataList
          items={top_used_materials}
          keyExtractor={(item) => item.material_id}
          emptyState={
            <EmptyState
              title="Chưa có dữ liệu"
              description="Chưa có đủ dữ liệu để thống kê."
            />
          }
          renderItem={(item, index) => (
            <div className="flex items-center gap-3 rounded-xl border border-[#202C43] bg-[#090E1A] px-4 py-3 transition-colors hover:bg-[rgba(79,124,255,0.04)]">
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-[rgba(124,92,255,0.12)] text-sm font-semibold text-[#7C5CFF]">
                {index + 1}
              </div>

              <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-medium text-[#F4F7FF]">
                  {item.name}
                </p>

                <div className="mt-1 flex items-center gap-2 text-xs text-[#8490A8]">
                  <span>{item.sku}</span>

                  <span className="text-[#4B556B]">•</span>

                  <span>{item.unit}</span>
                </div>
              </div>

              <div className="shrink-0 text-right">
                <p className="text-sm font-semibold text-[#7C5CFF]">
                  {item.outbound_count}
                </p>

                <p className="mt-1 text-xs text-[#606C84]">lần xuất</p>
              </div>
            </div>
          )}
        />
      </DataPanel>
    </section>
  );
}
