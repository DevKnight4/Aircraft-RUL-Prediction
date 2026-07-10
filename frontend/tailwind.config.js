/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        aviationBlue: '#1E3A8A',
        aviationLight: '#F8FAFC',
      }
    },
  },
  plugins: [],
}
