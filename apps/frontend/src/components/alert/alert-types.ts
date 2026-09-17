import type { ReactNode } from "react";

export type AlertType = "success" | "error" | "warning" | "info" | "confirm";

export type AlertSize = "sm" | "md" | "lg";

export interface AlertAction {
  label: string;
  onClick?: () => void | Promise<void>;
  variant?: "primary" | "secondary" | "danger";
  disabled?: boolean;
}

export interface AlertOptions {
  type: AlertType;

  title: string;
  message?: string;

  content?: ReactNode;

  confirmText?: string;
  cancelText?: string;

  actions?: AlertAction[];

  duration?: number;

  showClose?: boolean;

  dismissible?: boolean;

  size?: AlertSize;

  loading?: boolean;
  loadingText?: string;

  onConfirm?: () => void | Promise<void>;
  onCancel?: () => void | Promise<void>;
}

export interface AlertInstance extends AlertOptions {
  id: string;
  resolve?: (value: boolean) => void;
}
