"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import { useAuth } from "@/features/auth/auth-context";

import { getWarehouses } from "./warehouse-service";
import type { Warehouse } from "./warehouse-service";

const STORAGE_KEY = "stockflow.currentWarehouseId";

interface WarehouseContextValue {
  warehouses: Warehouse[];
  currentWarehouse: Warehouse | null;
  currentWarehouseId: number | null;
  isLoading: boolean;
  error: string | null;
  setCurrentWarehouse: (warehouseId: number) => void;
  refreshWarehouses: () => Promise<void>;
}

const WarehouseContext = createContext<WarehouseContextValue | null>(null);

export function WarehouseProvider({
  children,
}: {
  children: ReactNode;
}) {
  const { token, isAuthenticated } = useAuth();

  const [warehouses, setWarehouses] = useState<Warehouse[]>([]);
  const [currentWarehouseId, setCurrentWarehouseId] = useState<number | null>(
    null,
  );
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refreshWarehouses = useCallback(async () => {
    if (!token || !isAuthenticated) {
      setWarehouses([]);
      setCurrentWarehouseId(null);
      setIsLoading(false);
      setError(null);
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const data = await getWarehouses();

      const activeWarehouses = data.filter(
        (warehouse) => warehouse.is_active,
      );

      setWarehouses(activeWarehouses);

      const storedId = window.localStorage.getItem(STORAGE_KEY);
      const storedWarehouseId = storedId ? Number(storedId) : null;

      const selectedWarehouse =
        activeWarehouses.find(
          (warehouse) => warehouse.id === storedWarehouseId,
        ) ?? activeWarehouses[0];

      if (selectedWarehouse) {
        setCurrentWarehouseId(selectedWarehouse.id);

        window.localStorage.setItem(
          STORAGE_KEY,
          String(selectedWarehouse.id),
        );
      } else {
        setCurrentWarehouseId(null);
        window.localStorage.removeItem(STORAGE_KEY);
      }
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to load warehouses.",
      );
    } finally {
      setIsLoading(false);
    }
  }, [token, isAuthenticated]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    void refreshWarehouses();
  }, [refreshWarehouses]);

  const setCurrentWarehouse = useCallback(
    (warehouseId: number) => {
      const warehouse = warehouses.find(
        (item) => item.id === warehouseId,
      );

      if (!warehouse) {
        return;
      }

      setCurrentWarehouseId(warehouse.id);

      window.localStorage.setItem(
        STORAGE_KEY,
        String(warehouse.id),
      );
    },
    [warehouses],
  );

  const currentWarehouse =
    warehouses.find(
      (warehouse) => warehouse.id === currentWarehouseId,
    ) ?? null;

  const value = useMemo<WarehouseContextValue>(
    () => ({
      warehouses,
      currentWarehouse,
      currentWarehouseId,
      isLoading,
      error,
      setCurrentWarehouse,
      refreshWarehouses,
    }),
    [
      warehouses,
      currentWarehouse,
      currentWarehouseId,
      isLoading,
      error,
      setCurrentWarehouse,
      refreshWarehouses,
    ],
  );

  return (
    <WarehouseContext.Provider value={value}>
      {children}
    </WarehouseContext.Provider>
  );
}

export function useWarehouse() {
  const context = useContext(WarehouseContext);

  if (!context) {
    throw new Error(
      "useWarehouse must be used within a WarehouseProvider.",
    );
  }

  return context;
}