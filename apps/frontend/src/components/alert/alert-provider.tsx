"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from "react";

import { AlertModal } from "./alert-modal";
import { AlertToast } from "./alert-toast";

import type {
  AlertInstance,
  AlertOptions,
} from "./alert-types";

interface AlertContextValue {
  showAlert: (options: AlertOptions) => Promise<boolean>;
  closeAlert: () => void;
}

const AlertContext = createContext<AlertContextValue | null>(
  null,
);

export function AlertProvider({
  children,
}: {
  children: ReactNode;
}) {
  const [alert, setAlert] = useState<AlertInstance | null>(
    null,
  );

  const resolverRef = useRef<
    ((value: boolean) => void) | null
  >(null);

  const timeoutRef = useRef<ReturnType<
    typeof setTimeout
  > | null>(null);

  const clearAlertTimeout = useCallback(() => {
    if (timeoutRef.current !== null) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
  }, []);

  const resolveAlert = useCallback(
    (result: boolean) => {
      clearAlertTimeout();

      const resolver = resolverRef.current;

      resolverRef.current = null;

      setAlert(null);

      resolver?.(result);
    },
    [clearAlertTimeout],
  );

  const showAlert = useCallback(
    (options: AlertOptions): Promise<boolean> => {
      clearAlertTimeout();

      if (resolverRef.current) {
        resolverRef.current(false);
        resolverRef.current = null;
      }

      return new Promise<boolean>((resolve) => {
        resolverRef.current = resolve;

        const id = crypto.randomUUID();

        const nextAlert: AlertInstance = {
          ...options,
          id,
        };

        setAlert(nextAlert);

        if (
          options.type !== "confirm" &&
          options.duration !== 0
        ) {
          timeoutRef.current = setTimeout(() => {
            resolveAlert(false);
          }, options.duration ?? 4000);
        }
      });
    },
    [clearAlertTimeout, resolveAlert],
  );

  const closeAlert = useCallback(() => {
    resolveAlert(false);
  }, [resolveAlert]);

  const handleConfirm = useCallback(async () => {
    if (!alert || alert.type !== "confirm") {
      return;
    }

    try {
      await alert.onConfirm?.();
      resolveAlert(true);
    } catch {
      return;
    }
  }, [alert, resolveAlert]);

  const handleCancel = useCallback(async () => {
    if (!alert || alert.loading) {
      return;
    }

    try {
      await alert.onCancel?.();
    } finally {
      resolveAlert(false);
    }
  }, [alert, resolveAlert]);

  useEffect(() => {
    if (!alert || alert.type !== "confirm") {
      return;
    }

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key !== "Escape") {
        return;
      }

      event.preventDefault();
      void handleCancel();
    };

    window.addEventListener("keydown", handleKeyDown);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [alert, handleCancel]);

  useEffect(() => {
    return () => {
      clearAlertTimeout();

      resolverRef.current?.(false);
      resolverRef.current = null;
    };
  }, [clearAlertTimeout]);

  const value = useMemo<AlertContextValue>(
    () => ({
      showAlert,
      closeAlert,
    }),
    [showAlert, closeAlert],
  );

  const isToast =
    alert !== null &&
    ["success", "error", "warning", "info"].includes(
      alert.type,
    );

  return (
    <AlertContext.Provider value={value}>
      {children}

      {isToast && alert && (
        <div className="pointer-events-none fixed bottom-5 right-5 z-100 flex flex-col items-end gap-3">
          <AlertToast alert={alert} onClose={closeAlert} />
        </div>
      )}

      {alert?.type === "confirm" && (
        <AlertModal
          alert={alert}
          onClose={closeAlert}
          onConfirm={handleConfirm}
          onCancel={handleCancel}
        />
      )}
    </AlertContext.Provider>
  );
}

export function useAlert() {
  const context = useContext(AlertContext);

  if (!context) {
    throw new Error(
      "useAlert must be used within an AlertProvider.",
    );
  }

  return context;
}