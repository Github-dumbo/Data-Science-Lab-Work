/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        darkBg: "#0F172A",
        primaryTeal: "#14B8A6",
        secondaryPurple: "#8B5CF6",
        accentGreen: "#22C55E",
      }
    },
  },
  plugins: [],
}
