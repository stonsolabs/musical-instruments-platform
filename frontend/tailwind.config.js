/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    container: {
      center: true,
      padding: '1rem',
      screens: { sm: '640px', md: '768px', lg: '1024px', xl: '1200px', '2xl': '1320px' },
    },
    extend: {
      colors: {
        brand: {
          50: '#eef6ff', 100: '#d9ebff', 200: '#b9d9ff', 300: '#8cc0ff',
          400: '#5ea3ff', 500: '#3b82f6', 600: '#2563eb', 700: '#1d4ed8',
          800: '#1e40af', 900: '#1e3a8a',
        },
        accent: {
          50: '#fff3e6', 100: '#ffe4c2', 200: '#ffcd8a', 300: '#ffb155',
          400: '#ff9830', 500: '#f97316', 600: '#ea5c0a', 700: '#c2470a',
          800: '#9a3a0f', 900: '#7d310f',
        },
      },
      boxShadow: {
        card: '0 1px 2px rgba(16,24,40,0.06), 0 1px 3px rgba(16,24,40,0.10)',
        soft: '0 10px 25px rgba(0,0,0,0.05)',
      },
      borderRadius: { xl: '14px' },
      animation: { 'fade-up': 'fadeUp .35s ease-out', 'fade-in': 'fadeIn .25s ease-in' },
      keyframes: {
        fadeUp: { '0%': { opacity: 0, transform: 'translateY(8px)' }, '100%': { opacity: 1, transform: 'translateY(0)' } },
        fadeIn: { '0%': { opacity: 0 }, '100%': { opacity: 1 } },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
    require('@tailwindcss/line-clamp'),
  ],
}
