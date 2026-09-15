"use client";

import type { ReactNode } from "react";

import { AuthProvider } from "@/features/auth/auth-context";
import { WarehouseProvider } from "@/features/warehouses/warehouse-context";

interface ProvidersProps {
  children: ReactNode;
}

export function Providers({ children }: ProvidersProps) {
  return (
    <AuthProvider>
      <WarehouseProvider>
        {children}
      </WarehouseProvider>
    </AuthProvider>
  )
}