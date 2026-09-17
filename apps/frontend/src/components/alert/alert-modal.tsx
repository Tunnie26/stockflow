"use client";

import {
  AlertCircle,
  CheckCircle2,
  Info,
  TriangleAlert,
  X,
} from "lucide-react";

import type { AlertInstance } from "./alert-types";

interface AlertModalProps {
  alert: AlertInstance;
  onClose: () => void;
  onConfirm: () => Promise<void>;
  onCancel: () => Promise<void>;
}

const iconConfig = {
  success: {
    icon: CheckCircle2,
    color: "var(--sf-success)",
  },
  error: {
    icon: AlertCircle,
    color: "var(--sf-danger)",
  },
  warning: {
    icon: TriangleAlert,
    color: "var(--sf-warning)",
  },
  info: {
    icon: Info,
    color: "var(--sf-info)",
  },
  confirm: {
    icon: TriangleAlert,
    color: "var(--sf-primary)",
  },
};

const sizeClasses = {
  sm: "max-w-sm",
  md: "max-w-md",
  lg: "max-w-lg",
};

export function AlertModal({
  alert,
  onClose,
  onConfirm,
  onCancel,
}: AlertModalProps) {
  const config = iconConfig[alert.type];
  const Icon = config.icon;

  const handleOverlayClick = () => {
    if (!alert.dismissible || alert.loading) {
      return;
    }

    void onCancel();
  };

  const handleClose = () => {
    if (alert.loading) {
      return;
    }

    onClose();
  };

  return (
    <div
      className="fixed inset-0 z-[100 flex items-center justify-center p-4"
      role="presentation"
    >
      <button
        type="button"
        aria-label="Đóng"
        tabIndex={-1}
        onClick={handleOverlayClick}
        className="absolute inset-0 cursor-default bg-(--sf-overlay-default) backdrop-blur-[2px"
      />

      <div
        role="alertdialog"
        aria-modal="true"
        aria-labelledby={`alert-title-${alert.id}`}
        aria-describedby={
          alert.message
            ? `alert-description-${alert.id}`
            : undefined
        }
        className={[
          "animate-in fade-in zoom-in-95",
          "relative z-10 w-full",
          "rounded-2xl",
          "border border-(--sf-border-default)",
          "bg-(--sf-surface-elevated)",
          "shadow-(--sf-neumorphism-shadow-large)",
          "duration-200",
          sizeClasses[alert.size ?? "md"],
        ].join(" ")}
      >
        <div className="flex items-start gap-4 px-6 pb-4 pt-6">
          <div
            className="flex size-11 shrink-0 items-center justify-center rounded-xl"
            style={{
              color: config.color,
              backgroundColor: `color-mix(in srgb, ${config.color} 10%, transparent)`,
            }}
          >
            <Icon className="size-5" />
          </div>

          <div className="min-w-0 flex-1">
            <h2
              id={`alert-title-${alert.id}`}
              className="text-base font-semibold text-(--sf-text-primary)"
            >
              {alert.title}
            </h2>

            {alert.message && (
              <p
                id={`alert-description-${alert.id}`}
                className="mt-1.5 text-sm leading-5 text-(--sf-text-tertiary)"
              >
                {alert.message}
              </p>
            )}
          </div>

          {alert.showClose !== false && (
            <button
              type="button"
              aria-label="Đóng"
              disabled={alert.loading}
              onClick={handleClose}
              className="cursor-pointer flex size-8 shrink-0 items-center justify-center rounded-lg text-(--sf-text-tertiary) transition-colors hover:bg-(--sf-interaction-hover) hover:text-(--sf-text-primary) focus:outline-none focus-visible:ring-1 focus-visible:ring-(--sf-border-primary) disabled:pointer-events-none disabled:opacity-50"
            >
              <X className="size-4" />
            </button>
          )}
        </div>

        {(alert.content || alert.loading) && (
          <div className="px-6 pb-5">
            {alert.content}

            {alert.loading && (
              <div className="flex items-center gap-3 rounded-xl border border-(--sf-border-subtle) bg-(--sf-space-800) px-4 py-3">
                <span className="size-4 animate-spin rounded-full border-2 border-(--sf-border-strong) border-t-(--sf-primary)" />

                <span className="text-sm text-(--sf-text-secondary)">
                  {alert.loadingText ?? "Đang xử lý..."}
                </span>
              </div>
            )}
          </div>
        )}

        <div className="flex items-center justify-end gap-2 border-t border-(--sf-border-subtle) bg-(--sf-space-800) px-6 py-4">
          <button
            type="button"
            disabled={alert.loading}
            onClick={() => {
              void onCancel();
            }}
            className="cursor-pointer rounded-lg border border-(--sf-border-default) bg-(--sf-surface-default) px-4 py-2 text-sm font-medium text-(--sf-text-secondary) transition-colors hover:bg-(--sf-surface-interactive) hover:text-(--sf-text-primary) focus:outline-none focus-visible:ring-1 focus-visible:ring-(--sf-border-primary) disabled:pointer-events-none disabled:opacity-50"
          >
            {alert.cancelText ?? "Hủy"}
          </button>

          <button
            type="button"
            disabled={alert.loading}
            onClick={() => {
              void onConfirm();
            }}
            className="cursor-pointer rounded-lg bg-(--sf-primary) px-4 py-2 text-sm font-medium text-(--sf-text-primary) transition-all hover:bg-(--sf-primary-600) focus:outline-none focus-visible:ring-1 focus-visible:ring-(--sf-border-primary) disabled:pointer-events-none disabled:opacity-50"
          >
            {alert.loading
              ? alert.loadingText ?? "Đang xử lý..."
              : alert.confirmText ?? "Xác nhận"}
          </button>
        </div>
      </div>
    </div>
  );
}