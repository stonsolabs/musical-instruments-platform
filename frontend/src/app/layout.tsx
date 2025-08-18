import './globals.css'
import type { Metadata } from 'next'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import { GoogleTagManager } from '@/components/Analytics'
import { AnalyticsProvider } from '@/components/AnalyticsProvider'
import Script from 'next/script'

export const metadata: Metadata = {
  title: 'Compare Musical Instruments',
  description: 'Find the best deals on musical instruments. Compare specs, read reviews, and discover your next instrument.',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <GoogleTagManager />
        <Script
          async
          src={`https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${process.env.NEXT_PUBLIC_GOOGLE_ADSENSE_CLIENT_ID}`}
          crossOrigin="anonymous"
          strategy="afterInteractive"
        />
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
      </body>
    </html>
  )
}


