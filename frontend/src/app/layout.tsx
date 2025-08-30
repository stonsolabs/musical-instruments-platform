import './globals.css'
import type { Metadata } from 'next'
import dynamic from 'next/dynamic'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import { GoogleTagManager } from '@/components/Analytics'
import { AnalyticsProvider } from '@/components/AnalyticsProvider'

// Lazy load footer to improve initial load time
const DynamicFooter = dynamic(() => import('@/components/Footer'), {
  ssr: false,
})

export const metadata: Metadata = {
  title: 'Compare Musical Instruments - Find Your Perfect Instrument',
  description: 'Compare musical instruments with expert reviews, detailed specifications, and real-time pricing from trusted retailers. Find the perfect guitar, piano, drums, and more.',
  keywords: 'musical instruments, guitar, piano, drums, comparison, reviews, deals',
  authors: [{ name: 'Get Your Music Gear' }],
  creator: 'Get Your Music Gear',
  publisher: 'Get Your Music Gear',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || 'https://getyourmusicgear.com'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: 'Compare Musical Instruments - Find Your Perfect Instrument',
    description: 'Compare musical instruments with expert reviews, detailed specifications, and real-time pricing from trusted retailers.',
    url: '/',
    siteName: 'Get Your Music Gear',
    images: [
      {
        url: '/logo.png',
        width: 1200,
        height: 630,
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Compare Musical Instruments - Find Your Perfect Instrument',
    description: 'Compare musical instruments with expert reviews, detailed specifications, and real-time pricing from trusted retailers.',
    images: ['/logo.png'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <GoogleTagManager />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link rel="dns-prefetch" href="https://thomann.de" />
        <link rel="dns-prefetch" href="https://gear4music.com" />
        <link rel="dns-prefetch" href="https://www.google-analytics.com" />
        <meta name="theme-color" content="#1e40af" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "WebSite",
              "name": "Get Your Music Gear",
              "description": "Compare musical instruments with expert reviews, detailed specifications, and real-time pricing from trusted retailers.",
              "url": process.env.NEXT_PUBLIC_SITE_URL || "https://getyourmusicgear.com",
              "potentialAction": {
                "@type": "SearchAction",
                "target": {
                  "@type": "EntryPoint",
                  "urlTemplate": `${process.env.NEXT_PUBLIC_SITE_URL || "https://getyourmusicgear.com"}/products?search={search_term_string}`
                },
                "query-input": "required name=search_term_string"
              },
              "publisher": {
                "@type": "Organization",
                "name": "Get Your Music Gear",
                "url": process.env.NEXT_PUBLIC_SITE_URL || "https://getyourmusicgear.com"
              }
            })
          }}
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
          <a href="#main-content" className="skip-link">Skip to main content</a>
          <Header />
          <main id="main-content">
            {children}
          </main>
          <DynamicFooter />
        </AnalyticsProvider>
      </body>
    </html>
  )
}


