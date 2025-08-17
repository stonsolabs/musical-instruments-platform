import './globals.css'
import type { Metadata } from 'next'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import { GoogleTagManager, VercelAnalytics } from '@/components/Analytics'
import { AnalyticsProvider } from '@/components/AnalyticsProvider'

export const metadata: Metadata = {
  title: 'Compare Musical Instruments',
  description: 'Find the best deals on musical instruments. Compare specs, read reviews, and discover your next instrument.',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <GoogleTagManager />
      </head>
      <body className="bg-gray-50">
        {/* GTM noscript fallback */}
        <noscript>
          <iframe 
            src={`https://www.googletagmanager.com/ns.html?id=${process.env.NEXT_PUBLIC_GTM_ID}`}
            height="0" 
            width="0" 
            style={{ display: 'none', visibility: 'hidden' }}
          />
        </noscript>
        
        <AnalyticsProvider>
          <Header />
          <main>
            {children}
          </main>
          <Footer />
        </AnalyticsProvider>
        <VercelAnalytics />
      </body>
    </html>
  )
}


