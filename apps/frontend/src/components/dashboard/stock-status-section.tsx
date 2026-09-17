import { AlertTriangle, PackageX } from "lucide-react";

import type { DashboardData } from "@/features/dashboard/dashboard-types";
import {
  DataTable,
  type DataTableColumn,
} from "@/components/shared/data-table";
import { DataPanel } from "@/components/shared/data-panel";
import { EmptyState } from "@/components/shared/empty-state";
import { formatQuantity } from "@/utils/format-quantity";

interface StockStatusSectionProps {
  dashboard: DashboardData;
}

export function StockStatusSection({ dashboard }: StockStatusSectionProps) {
  const { stock_danger_items, stock_warning_items } = dashboard;

  const dangerColumns: DataTableColumn<(typeof stock_danger_items)[number]>[] =
    [
      {
        key: "sku",
        header: "SKU",
        headerClassName: "w-[90px] whitespace-nowrap !text-left",
        className: "w-[90px] !text-left",
        render: (item) => (
          <span className="whitespace-nowrap font-medium text-[#F4F7FF]">
            {item.sku}
          </span>
        ),
      },
      {
        key: "name",
        header: "Tên",
        headerClassName: "w-[220px] whitespace-nowrap !text-left",
        className: "w-[220px] !text-left",
        render: (item) => (
          <span className="block truncate text-[#B8C2D9]" title={item.name}>
            {item.name}
          </span>
        ),
      },
      {
        key: "unit",
        header: "ĐVT",
        headerClassName: "w-[80px] whitespace-nowrap !text-center",
        className: "w-[80px] whitespace-nowrap !text-center",
        render: (item) => item.unit,
      },
      {
        key: "specification",
        header: "Quy cách",
        headerClassName: "w-[150px] whitespace-nowrap !text-center",
        className: "w-[150px] !text-center",
        render: (item) => (
          <span className="block truncate" title={item.specification}>
            {item.specification}
          </span>
        ),
      },
      {
        key: "quantity",
        header: "Tồn kho",
        headerClassName: "w-[100px] whitespace-nowrap !text-center",
        className: "w-[100px] !text-center",
        render: (item) => (
          <span className="font-semibold text-[#F0526B]">
            {formatQuantity(item.quantity)}
          </span>
        ),
      },
      {
        key: "minimum_stock",
        header: "Tối thiểu",
        headerClassName: "w-[100px] whitespace-nowrap !text-center",
        className: "w-[100px] !text-center",
        render: (item) => (
          <span className="text-[#8490A8]">
            {formatQuantity(item.minimum_stock)}
          </span>
        ),
      },
      {
        key: "location",
        header: "Vị trí",
        headerClassName: "w-[100px] whitespace-nowrap !text-center",
        className: "w-[100px] !text-center",
        render: (item) => (
          <span className="whitespace-nowrap text-[#8490A8]">
            {item.location_code ?? "-"}
          </span>
        ),
      },
    ];

  const warningColumns: DataTableColumn<
    (typeof stock_warning_items)[number]
  >[] = [
    {
      key: "sku",
      header: "SKU",
      headerClassName: "w-[110px] whitespace-nowrap text-left",
      className: "w-[110px] whitespace-nowrap text-left",
      render: (item) => (
        <span className="font-medium text-[#F4F7FF]">{item.sku}</span>
      ),
    },
    {
      key: "name",
      header: "Tên vật tư",
      headerClassName: "w-[230px] whitespace-nowrap text-left",
      className: "w-[230px] text-left",
      render: (item) => (
        <span className="block truncate text-[#B8C2D9]" title={item.name}>
          {item.name}
        </span>
      ),
    },
    {
      key: "unit",
      header: "ĐVT",
      headerClassName: "w-[80px] whitespace-nowrap text-center",
      className: "w-[80px] whitespace-nowrap text-center",
      render: (item) => item.unit,
    },
    {
      key: "specification",
      header: "Quy cách",
      headerClassName: "w-[150px] whitespace-nowrap !text-center",
      className: "w-[150px] !text-center",
      render: (item) => (
        <span className="block truncate" title={item.specification}>
          {item.specification}
        </span>
      ),
    },
    {
      key: "quantity",
      header: "Tồn kho",
      headerClassName: "w-[100px] whitespace-nowrap text-center",
      className: "w-[100px] whitespace-nowrap text-center",
      render: (item) => (
        <span className="font-semibold text-[#F5B82E]">
          {formatQuantity(item.quantity)}
        </span>
      ),
    },
    {
      key: "minimum_stock",
      header: "Tối thiểu",
      headerClassName: "w-[100px] whitespace-nowrap text-center",
      className: "w-[100px] whitespace-nowrap text-center",
      render: (item) => (
        <span className="text-[#8490A8]">
          {formatQuantity(item.minimum_stock)}
        </span>
      ),
    },
    {
      key: "location",
      header: "Vị trí",
      headerClassName: "w-[100px] whitespace-nowrap text-center",
      className: "w-[100px] whitespace-nowrap text-center",
      render: (item) => (
        <span className="text-[#8490A8]">{item.location_code ?? "-"}</span>
      ),
    },
  ];

  return (
    <section className="grid grid-cols-1 gap-4 xl:grid-cols-2">
      <DataPanel
        title="Sắp hết hàng"
        description="Các SKU đang dưới mức tồn kho tối thiểu"
        icon={PackageX}
      >
        <DataTable
          data={stock_danger_items}
          columns={dangerColumns}
          keyExtractor={(item) => item.material_id}
          emptyState={
            <EmptyState
              title="Không có SKU sắp hết hàng"
              description="Tất cả SKU đang có mức tồn kho an toàn."
            />
          }
        />
      </DataPanel>

      <DataPanel
        title="Cảnh báo tồn kho"
        description="Các SKU cần được theo dõi"
        icon={AlertTriangle}
      >
        <DataTable
          data={stock_warning_items}
          columns={warningColumns}
          keyExtractor={(item) => item.material_id}
          emptyState={
            <EmptyState
              title="Không có cảnh báo"
              description="Hiện chưa có SKU nào cần theo dõi."
            />
          }
        />
      </DataPanel>
    </section>
  );
}
