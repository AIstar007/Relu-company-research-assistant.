/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        canvas: "#0a0a0a",
        panel: "#141414",
        border: "#232323",
        amber: {
          400: "#f5a623",
          500: "#e8940f",
        },
      },
    },
  },
  plugins: [],
};
