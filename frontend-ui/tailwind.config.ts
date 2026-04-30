import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#FFFFFF",
        card: "#FFFFFF",
        "card-muted": "#F5F5F5",
        border: "#E5E5E5",
        reco: {
          red: "#C41E3A", // Deeper red from screenshot
          "red-hover": "#A01830",
          light: "#FFF5F5",
        },
        text: {
          primary: "#1A1A1A",
          secondary: "#4A4A4A",
          muted: "#888888",
        }
      },
      borderRadius: {
        "3xl": "2rem",
      },
      boxShadow: {
        'premium': '0 20px 50px -12px rgba(0, 0, 0, 0.15)',
      }
    },
  },
  plugins: [],
};
export default config;
