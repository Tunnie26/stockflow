"use client";

import { SidebarTrigger } from "@/components/ui/sidebar";
import { WarehouseSelector } from "./warehouse-selector";

export function AppHeader() {
  return (
    <header className="flex h-14 shrink-0 items-center border-b bg-background px-4">
      <SidebarTrigger />

      <div className="ml-auto">
        <WarehouseSelector />
      </div>
    </header>
  );
}