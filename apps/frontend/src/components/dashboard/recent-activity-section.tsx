import {
  ArrowDownToLine,
  ArrowLeftRight,
  ArrowUpFromLine,
  ClipboardList,
  Settings2,
} from "lucide-react";

import type { DashboardData } from "@/features/dashboard/dashboard-types";
import { DataList } from "@/components/shared/data-list";
import { DataPanel } from "@/components/shared/data-panel";
import { EmptyState } from "@/components/shared/empty-state";

interface RecentActivitySectionProps {
  dashboard: DashboardData;
}

function getTransactionIcon(transactionType: string) {
  switch (transactionType) {
    case "INBOUND":
      return ArrowDownToLine;

    case "OUTBOUND":
      return ArrowUpFromLine;

    case "TRANSFER":
      return ArrowLeftRight;

    case "ADJUSTMENT":
      return Settings2;

    default:
      return ClipboardList;
  }
}

function getTransactionLabel(transactionType: string) {
  switch (transactionType) {
    case "INBOUND":
      return "Nhập kho";

    case "OUTBOUND":
      return "Xuất kho";

    case "TRANSFER":
      return "Điều chuyển";

    case "ADJUSTMENT":
      return "Điều chỉnh";

    default:
      return transactionType;
  }
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat("vi-VN", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}

export function RecentActivitySection({
  dashboard,
}: RecentActivitySectionProps) {
  const { recent_inbound, recent_activities } = dashboard;

  return (
    <section className="grid grid-cols-1 gap-4 xl:grid-cols-2">
      {/* Recent Inbound */}
      <DataPanel
        title="Nhập kho gần đây"
        description="Các phiếu nhập kho mới nhất"
        icon={ArrowDownToLine}
      >
        <DataList
          items={recent_inbound}
          keyExtractor={(item) => item.transaction_id}
          emptyState={
            <EmptyState
              title="Chưa có phiếu nhập"
              description="Chưa có hoạt động nhập kho gần đây."
            />
          }
          renderItem={(item) => {
            const Icon = getTransactionIcon(item.transaction_type);

            return (
              <div className="flex items-center gap-3 rounded-xl border border-[#202C43] bg-[#090E1A] px-4 py-3 transition-colors hover:bg-[rgba(79,124,255,0.04)]">
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-[rgba(34,211,238,0.12)] text-[#22D3EE]">
                  <Icon className="h-4 w-4" />
                </div>

                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium text-[#F4F7FF]">
                    Phiếu #{item.transaction_no}
                  </p>

                  <p className="mt-1 text-xs text-[#8490A8]">
                    {getTransactionLabel(item.transaction_type)}
                  </p>
                </div>

                <div className="shrink-0 text-right">
                  <p className="text-xs text-[#B8C2D9]">
                    {formatDate(item.transaction_date)}
                  </p>
                </div>
              </div>
            );
          }}
        />
      </DataPanel>

      {/* Recent Activities */}
      <DataPanel
        title="Hoạt động gần đây"
        description="Các giao dịch mới nhất trong kho"
        icon={ClipboardList}
      >
        <DataList
          items={recent_activities}
          keyExtractor={(item) => item.transaction_id}
          emptyState={
            <EmptyState
              title="Chưa có hoạt động"
              description="Chưa có giao dịch nào gần đây."
            />
          }
          renderItem={(item) => {
            const Icon = getTransactionIcon(item.transaction_type);

            return (
              <div className="flex items-center gap-3 rounded-xl border border-[#202C43] bg-[#090E1A] px-4 py-3 transition-colors hover:bg-[rgba(79,124,255,0.04)]">
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-[rgba(79,124,255,0.12)] text-[#4F7CFF]">
                  <Icon className="h-4 w-4" />
                </div>

                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium text-[#F4F7FF]">
                    {getTransactionLabel(item.transaction_type)}
                  </p>

                  <p className="mt-1 text-xs text-[#8490A8]">
                    Phiếu #{item.transaction_no}
                  </p>
                </div>

                <div className="shrink-0 text-right">
                  <p className="text-xs text-[#B8C2D9]">
                    {formatDate(item.created_at)}
                  </p>
                </div>
              </div>
            );
          }}
        />
      </DataPanel>
    </section>
  );
}
