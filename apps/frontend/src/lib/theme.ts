import { colors } from "@/constains/colors";

type StockFlowCSSVariables = React.CSSProperties & {
  [key: `--sf-${string}`]: string;
};

export const stockFlowTheme: StockFlowCSSVariables = {
  /* Space */
  "--sf-space-950": colors.space[950],
  "--sf-space-900": colors.space[900],
  "--sf-space-850": colors.space[850],
  "--sf-space-800": colors.space[800],
  "--sf-space-750": colors.space[750],
  "--sf-space-700": colors.space[700],

  /* Surface */
  "--sf-surface-base": colors.surface.base,
  "--sf-surface-subtle": colors.surface.subtle,
  "--sf-surface-default": colors.surface.default,
  "--sf-surface-elevated": colors.surface.elevated,
  "--sf-surface-high": colors.surface.high,
  "--sf-surface-interactive": colors.surface.interactive,

  /* Text */
  "--sf-text-primary": colors.text.primary,
  "--sf-text-secondary": colors.text.secondary,
  "--sf-text-tertiary": colors.text.tertiary,
  "--sf-text-muted": colors.text.muted,
  "--sf-text-disabled": colors.text.disabled,
  "--sf-text-inverse": colors.text.inverse,

  /* Border */
  "--sf-border-subtle": colors.border.subtle,
  "--sf-border-default": colors.border.default,
  "--sf-border-strong": colors.border.strong,
  "--sf-border-primary": colors.border.primary,
  "--sf-border-focus": colors.border.focus,

  /* Brand */
  "--sf-primary": colors.primary.DEFAULT,
  "--sf-secondary": colors.secondary.DEFAULT,
  "--sf-accent": colors.accent.DEFAULT,

  /* Semantic */
  "--sf-success": colors.semantic.success,
  "--sf-warning": colors.semantic.warning,
  "--sf-danger": colors.semantic.danger,
  "--sf-info": colors.semantic.info,

  /* Interaction */
  "--sf-interaction-hover": colors.interaction.hover,
  "--sf-interaction-active": colors.interaction.active,
  "--sf-interaction-selected": colors.interaction.selected,
  "--sf-interaction-focus": colors.interaction.focus,
  "--sf-interaction-disabled": colors.interaction.disabled,

  /* Chart */
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