/**
 * StockFlow Color System
 *
 * Design Direction:
 * - Dark-first
 * - Cosmic / Astral
 * - Futuristic / Sci-fi
 * - Medium Neumorphism
 * - Medium Astral Glow
 * - Accessibility-first contrast
 *
 * Concept:
 * "Astral Command Center for Warehouse Operations"
 */

export const colors = {
  // SPACE
  // Deepest layers of the application.
  space: {
    950: "#03050A",
    900: "#050812",
    850: "#070B14",
    800: "#090E1A",
    750: "#0B111E",
    700: "#0D1422",
  },

  // SURFACE
  // Layered surfaces used to create depth in dark mode.
  surface: {
    base: "#090E1A",
    subtle: "#0B111E",
    default: "#0D1422",
    elevated: "#111A2A",
    high: "#152033",
    interactive: "#18253A",
  },

  // TEXT
  // High-contrast typography hierarchy for readability.
  text: {
    primary: "#F4F7FF",
    secondary: "#B8C2D9",
    tertiary: "#8490A8",
    muted: "#606C84",
    disabled: "#4B556B",
    inverse: "#050812",
  },

  // BORDER
  // Structural borders and focus indicators.
  border: {
    subtle: "#172136",
    default: "#202C43",
    strong: "#2C3A55",
    primary: "#385FC4",
    focus: "#5B82FF",
  },

  // PRIMARY
  // StockFlow's main identity color for actions and navigation.
  primary: {
    50: "#EEF3FF",
    100: "#DCE6FF",
    200: "#B9CAFF",
    300: "#91AAFF",
    400: "#6F8FFF",
    500: "#4F7CFF",
    600: "#3F68E6",
    700: "#3455BF",
    800: "#2C4799",
    900: "#253B78",
    DEFAULT: "#4F7CFF",
  },

  // SECONDARY
  // Astral purple used for secondary actions and special states.
  secondary: {
    50: "#F5F1FF",
    100: "#E9E0FF",
    200: "#D5C5FF",
    300: "#BCA4FF",
    400: "#9D7FFF",
    500: "#7C5CFF",
    600: "#6847E6",
    700: "#563AC2",
    800: "#46339A",
    900: "#382B73",
    DEFAULT: "#7C5CFF",
  },

  // ACCENT
  // Cyan represents information, realtime activity and system energy.
  accent: {
    50: "#ECFEFF",
    100: "#CFFAFE",
    200: "#A5F3FC",
    300: "#67E8F9",
    400: "#38D9F2",
    500: "#22D3EE",
    600: "#12AFCB",
    700: "#0E8EA8",
    800: "#117287",
    900: "#155E70",
    DEFAULT: "#22D3EE",
  },

  // SEMANTIC
  // Astral-inspired semantic colors for system feedback.
  semantic: {
    success: "#10D9A0",
    warning: "#F5B82E",
    danger: "#F0526B",
    info: "#22D3EE",
  },

  // STATUS
  // Business-specific status mapping for warehouse operations.
  status: {
    normal: "#10D9A0",
    lowStock: "#F5B82E",
    outOfStock: "#F0526B",

    pending: "#7C5CFF",
    processing: "#4F7CFF",
    completed: "#10D9A0",
    cancelled: "#F0526B",

    discrepancy: "#F5B82E",
    draft: "#8490A8",
  },

  // TRANSACTION
  // Color mapping for warehouse transaction types.
  transaction: {
    import: "#22D3EE",
    export: "#4F7CFF",
    transfer: "#7C5CFF",
    adjustment: "#F5B82E",
    return: "#10D9A0",
    borrow: "#F5B82E",
  },

  // GRADIENT
  // Signature gradients for major visual and interactive elements.
  gradient: {
    primary: "linear-gradient(135deg, #4F7CFF 0%, #7C5CFF 100%)",

    primarySoft:
      "linear-gradient(135deg, rgba(79, 124, 255, 0.18) 0%, rgba(124, 92, 255, 0.18) 100%)",

    astral:
      "linear-gradient(135deg, #22D3EE 0%, #4F7CFF 50%, #7C5CFF 100%)",

    surface:
      "linear-gradient(145deg, #111A2A 0%, #0B111E 100%)",

    cosmic:
      "radial-gradient(circle at top right, rgba(124, 92, 255, 0.16), transparent 45%), linear-gradient(145deg, #050812 0%, #0D1422 100%)",
  },

  // GLOW
  // Medium-intensity Astral glow reserved for important visual states.
  glow: {
    primary: "0 0 24px rgba(79, 124, 255, 0.28)",
    secondary: "0 0 24px rgba(124, 92, 255, 0.28)",
    accent: "0 0 24px rgba(34, 211, 238, 0.25)",
    success: "0 0 20px rgba(16, 217, 160, 0.20)",
    warning: "0 0 20px rgba(245, 184, 46, 0.20)",
    danger: "0 0 20px rgba(240, 82, 107, 0.20)",
  },

  // NEUMORPHISM
  // Soft shadows used to create depth without excessive visual noise.
  neumorphism: {
    light: "rgba(255, 255, 255, 0.035)",
    dark: "rgba(0, 0, 0, 0.45)",

    shadow:
      "8px 8px 18px rgba(0, 0, 0, 0.45), -6px -6px 16px rgba(255, 255, 255, 0.025)",

    shadowSmall:
      "4px 4px 10px rgba(0, 0, 0, 0.40), -3px -3px 8px rgba(255, 255, 255, 0.02)",

    shadowLarge:
      "14px 14px 30px rgba(0, 0, 0, 0.50), -10px -10px 24px rgba(255, 255, 255, 0.025)",

    inset:
      "inset 5px 5px 12px rgba(0, 0, 0, 0.40), inset -4px -4px 10px rgba(255, 255, 255, 0.02)",
  },

  // INTERACTIVE
  // Interactive states for buttons, navigation and selectable elements.
  interaction: {
    hover: "rgba(79, 124, 255, 0.08)",
    active: "rgba(79, 124, 255, 0.14)",
    selected: "rgba(79, 124, 255, 0.16)",
    focus: "rgba(79, 124, 255, 0.22)",
    disabled: "rgba(255, 255, 255, 0.04)",
  },

  // OVERLAY
  // Transparency layers for dialogs, drawers and modal surfaces.
  overlay: {
    subtle: "rgba(5, 8, 18, 0.55)",
    default: "rgba(5, 8, 18, 0.72)",
    strong: "rgba(3, 5, 10, 0.88)",
  },

  // CHART
  // High-contrast visualization palette optimized for dark backgrounds.
  chart: {
    blue: "#4F7CFF",
    purple: "#7C5CFF",
    cyan: "#22D3EE",
    green: "#10D9A0",
    amber: "#F5B82E",
    red: "#F0526B",

    indigo: "#6366F1",
    violet: "#A78BFA",
    teal: "#2DD4BF",
    sky: "#38BDF8",
  },

  // BASE
  // Primitive colors for opacity-based utilities and low-level styling.
  base: {
    white: "#FFFFFF",
    black: "#000000",
  },
} as const;

export type Colors = typeof colors;