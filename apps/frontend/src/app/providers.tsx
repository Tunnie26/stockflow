"use client";

import type { ReactNode } from "react";

import { AuthProvider } from "@/features/auth/auth-context";
import { WarehouseProvider } from "@/features/warehouses/warehouse-context";

import { AuthGate } from "@/components/auth/auth-gate";

export function Providers({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <AuthProvider>
      <AuthGate>
        <WarehouseProvider>
          {children}
        </WarehouseProvider>
      </AuthGate>
    </AuthProvider>
  );
}