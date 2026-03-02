/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      colors: {
        ai: {
          bg: 'var(--ai-bg)',
          surface: 'var(--ai-surface)',
          border: 'var(--ai-border)',
          primary: 'var(--ai-primary)',
          muted: 'var(--ai-muted)',
        },
      },
    },
  },
  plugins: [],
}
