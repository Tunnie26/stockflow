"use client";

import {
  AlertCircle,
  CheckCircle2,
  Info,
  TriangleAlert,
  X,
} from "lucide-react";

import type { AlertInstance } from "./alert-types";

interface AlertToastProps {
  alert: AlertInstance;
  onClose: () => void;
}

const alertConfig = {
  success: {
    icon: CheckCircle2,
    color: "var(--sf-success)",
    glow: "var(--sf-glow-success)",
  },
  error: {
    icon: AlertCircle,
    color: "var(--sf-danger)",
    glow: "var(--sf-glow-danger)",
  },
  warning: {
    icon: TriangleAlert,
    color: "var(--sf-warning)",
    glow: "var(--sf-glow-warning)",
  },
  info: {
    icon: Info,
    color: "var(--sf-info)",
    glow: "var(--sf-glow-accent)",
  },
} as const;

export function AlertToast({ alert, onClose }: AlertToastProps) {
  const config = alertConfig[alert.type as keyof typeof alertConfig];

  if (!config) {
    return null;
  }

  const Icon = config.icon;

  return (
    <div
      role="alert"
      className="animate-in fade-in zoom-in-95 pointer-events-auto w-95 max-w-[calc(100vw-2rem)] rounded-2xl border border-(--sf-border-default) bg-(--sf-surface-elevated) p-4 shadow-(--sf-neumorphism-shadow-large) duration-200"
      style={{
        boxShadow: `${config.glow}, var(--sf-neumorphism-shadow-large)`,
      }}
    >
      <div className="flex items-start gap-3">
        <div
          className="flex size-10 shrink-0 items-center justify-center rounded-xl"
          style={{
            color: config.color,
            backgroundColor: `color-mix(in srgb, ${config.color} 10%, transparent)`,
          }}
        >
          <Icon className="size-5" />
        </div>

        <div className="min-w-0 flex-1">
          <h3 className="text-sm font-semibold text-(--sf-text-primary)">
            {alert.title}
          </h3>

          {alert.message && (
            <p className="mt-1 text-sm leading-5 text-(--sf-text-tertiary)">
              {alert.message}
            </p>
          )}

          {alert.content && <div className="mt-3">{alert.content}</div>}

          {alert.actions && alert.actions.length > 0 && (
            <div className="mt-3 flex flex-wrap gap-2">
              {alert.actions.map((action) => (
                <button
                  key={action.label}
                  type="button"
                  disabled={action.disabled}
                  onClick={() => {
                    void action.onClick?.();
                  }}
                  className="rounded-lg px-3 py-1.5 text-xs font-medium transition-colors disabled:pointer-events-none disabled:opacity-50"
                >
                  {action.label}
                </button>
              ))}
            </div>
          )}
        </div>

        {alert.showClose !== false && (
          <button
            type="button"
            aria-label="Đóng"
            onClick={onClose}
            className="flex size-7 shrink-0 items-center justify-center rounded-lg text-(--sf-text-tertiary) transition-colors hover:bg-(--sf-interaction-hover) hover:text-(--sf-text-primary) focus:outline-none focus-visible:ring-1 focus-visible:ring-(--sf-border-primary)"
          >
            <X className="size-4" />
          </button>
        )}
      </div>
    </div>
  );
}
