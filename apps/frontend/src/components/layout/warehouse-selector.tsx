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
    currentWarehouseId,
    isLoading,
    error,
    setCurrentWarehouse,
  } = useWarehouse();

  if (isLoading) {
    return (
      <div className="flex h-9 items-center gap-2 rounded-md border px-3 text-sm text-muted-foreground">
        <Loader2 className="size-4 animate-spin" />
        <span>Đang tải kho...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex h-9 items-center rounded-md border px-3 text-sm text-destructive">
        Không thể tải danh sách kho
      </div>
    );
  }

  if (warehouses.length === 0) {
    return (
      <div className="flex h-9 items-center gap-2 rounded-md border px-3 text-sm text-muted-foreground">
        <Building2 className="size-4" />
        <span>Chưa có kho</span>
      </div>
    );
  }

  const currentWarehouse = warehouses.find(
    (warehouse) => warehouse.id === currentWarehouseId,
  );

  return (
    <Select
      value={currentWarehouse?.name}
      onValueChange={(value) => {
        const warehouse = warehouses.find((item) => item.name === value);

        if (warehouse) {
          setCurrentWarehouse(warehouse.id);
        }
      }}
    >
      <SelectTrigger className="w-[220px]">
        <Building2 className="size-4 text-muted-foreground" />
        <SelectValue placeholder="Chọn kho" />
      </SelectTrigger>

      <SelectContent>
        {warehouses.map((warehouse) => (
          <SelectItem key={warehouse.id} value={warehouse.name}>
            <span className="ml-2 text-muted-foreground">{warehouse.name}</span>
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}
