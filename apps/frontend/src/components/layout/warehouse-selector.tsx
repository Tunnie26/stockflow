"use client";

import { Building2, Loader2 } from "lucide-react";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import { useWarehouse } from "@/features/warehouses/warehouse-context";

export function WarehouseSelector() {
  const {
    warehouses,
    currentWarehouse,
    isLoading,
    error,
    setCurrentWarehouse,
  } = useWarehouse();

  if (isLoading) {
    return (
      <div className="flex h-11 w-[220px] items-center gap-2 rounded-lg border border-[#202C43] bg-[#0D1422] px-3.5 text-sm text-[#8490A8]">
        <Loader2 className="size-4 animate-spin" aria-hidden="true" />
        <span>Đang tải kho...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex h-11 items-center rounded-lg border border-[#F0526B]/30 bg-[#F0526B]/10 px-3.5 text-sm text-[#F0526B]">
        Không thể tải danh sách kho
      </div>
    );
  }

  return (
    <Select
      value={currentWarehouse?.name}
      onValueChange={(warehouseName) => {
        const warehouse = warehouses.find(
          (item) => item.name === warehouseName,
        );

        if (warehouse) {
          setCurrentWarehouse(warehouse.id);
        }
      }}
    >
      <SelectTrigger
        className="h-11 w-[220px] cursor-pointer border-[#202C43] bg-[#0D1422] px-3.5 text-[#F4F7FF] shadow-none hover:border-[#385FC4] hover:bg-[#111A2A] focus:border-[#5B82FF] focus:ring-2 focus:ring-[#5B82FF]/20"
        aria-label="Chọn kho"
      >
        <div className="flex min-w-0 items-center gap-2.5">
          <Building2
            className="size-4.5 shrink-0 text-[#6F8FFF]"
            aria-hidden="true"
          />

          <SelectValue placeholder="Chọn kho" />
        </div>
      </SelectTrigger>

      <SelectContent
        side="bottom"
        sideOffset={8}
        align="end"
        alignItemWithTrigger={false}
        className="w-[220px] border-[#2C3A55] bg-[#0D1422] p-1.5 text-[#F4F7FF] shadow-[0_18px_40px_rgba(0,0,0,0.45)]"
      >
        {warehouses.map((warehouse) => (
          <SelectItem
            key={warehouse.id}
            value={warehouse.name}
            className="cursor-pointer rounded-md text-[#B8C2D9] hover:bg-[rgba(79,124,255,0.10)] hover:text-[#F4F7FF] data-highlighted:bg-[rgba(79,124,255,0.16)] data-highlighted:text-[#F4F7FF]"
          >
            <div className="flex w-full items-center gap-2.5">
              <Building2
                className="size-4 shrink-0 text-[#8490A8] data-highlighted:text-[#91AAFF]"
                aria-hidden="true"
              />
              <span className="truncate">{warehouse.name}</span>
            </div>
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}
