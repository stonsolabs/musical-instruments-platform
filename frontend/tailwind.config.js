/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx}',
    './src/components/**/*.{js,ts,jsx,tsx}',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        },
        accent: {
          50: '#fef7f0',
          100: '#fdecd4',
          200: '#fbd5a8',
          300: '#f8b971',
          400: '#f59538',
          500: '#f2751a',
          600: '#e35d0f',
          700: '#bc4510',
          800: '#963714',
          900: '#7a3014',
        },
        brand: {
          primary: '#1a1a1a',    // Dark gray/black (Baum style)
          secondary: '#ffffff',  // White
          accent: '#f3f4f6',     // Light gray
          dark: '#000000',       // Pure black
          blue: '#1a1a1a',       // Dark for blue contexts
          orange: '#D91C01',     // Baum red for accents
          red: '#D91C01',        // Baum red
        },
        store: {
          thomann: {
            DEFAULT: '#0aa4bc',
            dark: '#0a91a7',
          },
          gear4music: {
            DEFAULT: '#f59e0b',
            dark: '#d97706',
          },
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Oswald', 'system-ui', 'sans-serif'], // Baum Guitars style
      },
      boxShadow: {
        'elegant': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'glow': '0 0 20px rgba(59, 130, 246, 0.3)',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ],
}
