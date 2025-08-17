import type { AppProps } from 'next/app'
import Head from 'next/head'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import { GoogleTagManager, VercelAnalytics } from '@/components/Analytics'
import { AnalyticsProvider } from '@/components/AnalyticsProvider'
import '@/app/globals.css'

export default function App({ Component, pageProps }: AppProps) {
  return (
    <>
      <Head>
        <title>Compare Musical Instruments</title>
        <meta name="description" content="Find the best deals on musical instruments. Compare specs, read reviews, and discover your next instrument." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
        <GoogleTagManager />
      </Head>
      
      {/* GTM noscript fallback */}
      <noscript>
        <iframe 
          src={`https://www.googletagmanager.com/ns.html?id=${process.env.NEXT_PUBLIC_GTM_ID}`}
          height="0" 
          width="0" 
          style={{ display: 'none', visibility: 'hidden' }}
        />
      </noscript>
      
      <div className="bg-gray-50 min-h-screen">
        <AnalyticsProvider>
          <Header />
          <main>
            <Component {...pageProps} />
          </main>
          <Footer />
        </AnalyticsProvider>
        <VercelAnalytics />
      </div>
    </>
  )
}
