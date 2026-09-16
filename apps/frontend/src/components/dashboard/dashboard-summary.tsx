import {
  ArrowDownToLine,
  ArrowUpFromLine,
  Package,
  TriangleAlert,
} from "lucide-react";

import type { DashboardSummary as DashboardSummaryData } from "@/features/dashboard/dashboard-types";

import {
  StatCard,
  type StatCardProps,
} from "@/components/shared/stat-card";

interface DashboardSummaryProps {
  summary: DashboardSummaryData;
}

export function DashboardSummary({
  summary,
}: DashboardSummaryProps) {
  const cards: StatCardProps[] = [
    {
      title: "Tổng SKU",
      value: summary.total_sku,
      description: "SKU đang hoạt động",
      icon: Package,
      iconClassName:
        "bg-[rgba(79,124,255,0.12)] text-[#4F7CFF]",
    },
    {
      title: "Sắp hết hàng",
      value: summary.stock_danger,
      description: "SKU dưới mức tồn tối thiểu",
      icon: TriangleAlert,
      iconClassName:
        "bg-[rgba(240,82,107,0.12)] text-[#F0526B]",
    },
    {
      title: "Phiếu nhập",
      value: summary.inbound_this_month,
      description: "Trong tháng này",
      icon: ArrowDownToLine,
      iconClassName:
        "bg-[rgba(34,211,238,0.12)] text-[#22D3EE]",
    },
    {
      title: "Phiếu xuất",
      value: summary.outbound_this_month,
      description: "Trong tháng này",
      icon: ArrowUpFromLine,
      iconClassName:
        "bg-[rgba(124,92,255,0.12)] text-[#7C5CFF]",
    },
  ];

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {cards.map((card) => (
        <StatCard
          key={card.title}
          {...card}
        />
      ))}
    </div>
  );
}