/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx}',
    './src/components/**/*.{js,ts,jsx,tsx}',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      typography: {
        DEFAULT: {
          css: {
            '--tw-prose-body': '#111827',
            '--tw-prose-headings': '#111827',
            '--tw-prose-links': '#111827',
            '--tw-prose-bold': '#111827',
            '--tw-prose-counters': '#6b7280',
            '--tw-prose-bullets': '#9ca3af',
            '--tw-prose-hr': '#e5e7eb',
            '--tw-prose-quotes': '#111827',
            '--tw-prose-quote-borders': '#e5e7eb',
            '--tw-prose-captions': '#6b7280',
            '--tw-prose-code': '#111827',
            '--tw-prose-th-borders': '#e5e7eb',
            '--tw-prose-td-borders': '#e5e7eb',
            h1: { fontFamily: 'Montserrat, sans-serif', fontWeight: '800', letterSpacing: '-0.01em' },
            h2: { fontFamily: 'Montserrat, sans-serif', fontWeight: '800', fontSize: '1.75rem', marginTop: '1.5rem', marginBottom: '0.75rem' },
            h3: { fontFamily: 'Montserrat, sans-serif', fontWeight: '700', fontSize: '1.375rem', marginTop: '1.25rem', marginBottom: '0.5rem' },
            h4: { fontFamily: 'Montserrat, sans-serif', fontWeight: '700' },
            p: { marginTop: '0.9rem', marginBottom: '0.9rem' },
            a: { color: '#111827', textDecoration: 'underline' },
            strong: { color: '#111827' },
            blockquote: { fontStyle: 'normal', borderLeftColor: '#e5e7eb' },
            ul: { marginTop: '0.8rem', marginBottom: '0.8rem' },
            ol: { marginTop: '0.8rem', marginBottom: '0.8rem' },
            code: { backgroundColor: '#f3f4f6', padding: '0.15rem 0.35rem', borderRadius: '0.25rem' },
            pre: { backgroundColor: '#111827', color: '#f9fafb' },
            hr: { borderColor: '#e5e7eb' },
            img: { borderRadius: '0.5rem' }
          }
        }
      },
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
