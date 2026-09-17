import { colors } from "@/constains/colors";
import type { CSSProperties } from "react";

type StockFlowCSSVariables = CSSProperties & {
  [key: `--sf-${string}`]: string;
};

export const stockFlowTheme: StockFlowCSSVariables = {
  // Space
  "--sf-space-950": colors.space[950],
  "--sf-space-900": colors.space[900],
  "--sf-space-850": colors.space[850],
  "--sf-space-800": colors.space[800],
  "--sf-space-750": colors.space[750],
  "--sf-space-700": colors.space[700],

  // Surface
  "--sf-surface-base": colors.surface.base,
  "--sf-surface-subtle": colors.surface.subtle,
  "--sf-surface-default": colors.surface.default,
  "--sf-surface-elevated": colors.surface.elevated,
  "--sf-surface-high": colors.surface.high,
  "--sf-surface-interactive": colors.surface.interactive,

  // Text
  "--sf-text-primary": colors.text.primary,
  "--sf-text-secondary": colors.text.secondary,
  "--sf-text-tertiary": colors.text.tertiary,
  "--sf-text-muted": colors.text.muted,
  "--sf-text-disabled": colors.text.disabled,
  "--sf-text-inverse": colors.text.inverse,

  // Border
  "--sf-border-subtle": colors.border.subtle,
  "--sf-border-default": colors.border.default,
  "--sf-border-strong": colors.border.strong,
  "--sf-border-primary": colors.border.primary,
  "--sf-border-focus": colors.border.focus,

  // Primary
  "--sf-primary-50": colors.primary[50],
  "--sf-primary-100": colors.primary[100],
  "--sf-primary-200": colors.primary[200],
  "--sf-primary-300": colors.primary[300],
  "--sf-primary-400": colors.primary[400],
  "--sf-primary-500": colors.primary[500],
  "--sf-primary-600": colors.primary[600],
  "--sf-primary-700": colors.primary[700],
  "--sf-primary-800": colors.primary[800],
  "--sf-primary-900": colors.primary[900],
  "--sf-primary": colors.primary.DEFAULT,

  // Secondary
  "--sf-secondary-50": colors.secondary[50],
  "--sf-secondary-100": colors.secondary[100],
  "--sf-secondary-200": colors.secondary[200],
  "--sf-secondary-300": colors.secondary[300],
  "--sf-secondary-400": colors.secondary[400],
  "--sf-secondary-500": colors.secondary[500],
  "--sf-secondary-600": colors.secondary[600],
  "--sf-secondary-700": colors.secondary[700],
  "--sf-secondary-800": colors.secondary[800],
  "--sf-secondary-900": colors.secondary[900],
  "--sf-secondary": colors.secondary.DEFAULT,

  // Accent
  "--sf-accent-50": colors.accent[50],
  "--sf-accent-100": colors.accent[100],
  "--sf-accent-200": colors.accent[200],
  "--sf-accent-300": colors.accent[300],
  "--sf-accent-400": colors.accent[400],
  "--sf-accent-500": colors.accent[500],
  "--sf-accent-600": colors.accent[600],
  "--sf-accent-700": colors.accent[700],
  "--sf-accent-800": colors.accent[800],
  "--sf-accent-900": colors.accent[900],
  "--sf-accent": colors.accent.DEFAULT,

  // Semantic
  "--sf-success": colors.semantic.success,
  "--sf-warning": colors.semantic.warning,
  "--sf-danger": colors.semantic.danger,
  "--sf-info": colors.semantic.info,

  // Interaction
  "--sf-interaction-hover": colors.interaction.hover,
  "--sf-interaction-active": colors.interaction.active,
  "--sf-interaction-selected": colors.interaction.selected,
  "--sf-interaction-focus": colors.interaction.focus,
  "--sf-interaction-disabled": colors.interaction.disabled,

  // Overlay
  "--sf-overlay-subtle": colors.overlay.subtle,
  "--sf-overlay-default": colors.overlay.default,
  "--sf-overlay-strong": colors.overlay.strong,

  // Glow
  "--sf-glow-primary": colors.glow.primary,
  "--sf-glow-secondary": colors.glow.secondary,
  "--sf-glow-accent": colors.glow.accent,
  "--sf-glow-success": colors.glow.success,
  "--sf-glow-warning": colors.glow.warning,
  "--sf-glow-danger": colors.glow.danger,

  // Neumorphism
  "--sf-neumorphism-light": colors.neumorphism.light,
  "--sf-neumorphism-dark": colors.neumorphism.dark,
  "--sf-neumorphism-shadow": colors.neumorphism.shadow,
  "--sf-neumorphism-shadow-small": colors.neumorphism.shadowSmall,
  "--sf-neumorphism-shadow-large": colors.neumorphism.shadowLarge,
  "--sf-neumorphism-inset": colors.neumorphism.inset,

  // Chart
  "--sf-chart-blue": colors.chart.blue,
  "--sf-chart-purple": colors.chart.purple,
  "--sf-chart-cyan": colors.chart.cyan,
  "--sf-chart-green": colors.chart.green,
  "--sf-chart-amber": colors.chart.amber,
  "--sf-chart-red": colors.chart.red,
  "--sf-chart-indigo": colors.chart.indigo,
  "--sf-chart-violet": colors.chart.violet,
  "--sf-chart-teal": colors.chart.teal,
  "--sf-chart-sky": colors.chart.sky,
};