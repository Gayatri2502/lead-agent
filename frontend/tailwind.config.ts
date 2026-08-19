import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#000000",
        foreground: "#FFFFFF",
        card: "#111111",
        "card-foreground": "#FFFFFF",
        primary: "#3B82F6",
        "primary-foreground": "#FFFFFF",
        secondary: "#6B7280",
        "secondary-foreground": "#FFFFFF",
        destructive: "#EF4444",
        "destructive-foreground": "#FFFFFF",
        muted: "#6B7280",
        "muted-foreground": "#9CA3AF",
        accent: "#3B82F6",
        "accent-foreground": "#FFFFFF",
        border: "#222222",
        input: "#222222",
        ring: "#3B82F6",
        success: "#22C55E",
        warning: "#F59E0B",
      },
      backgroundColor: {
        dark: "#000000",
        "dark-card": "#111111",
        "dark-border": "#222222",
      },
      textColor: {
        dark: "#FFFFFF",
        "dark-secondary": "#9CA3AF",
      },
      borderColor: {
        dark: "#222222",
      },
      fontFamily: {
        sans: ["system-ui", "sans-serif"],
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
