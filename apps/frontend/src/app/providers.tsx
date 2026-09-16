"use client";

import { useState, type ReactNode } from "react";

import { AuthProvider } from "@/features/auth/auth-context";
import { WarehouseProvider } from "@/features/warehouses/warehouse-context";

import { AuthGate } from "@/components/auth/auth-gate";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

export function Providers({ children }: { children: ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 30_000,
            refetchOnWindowFocus: false,
          },
        },
      }),
  );

  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <AuthGate>
          <WarehouseProvider>{children}</WarehouseProvider>
        </AuthGate>
      </AuthProvider>
    </QueryClientProvider>
  );
}
