'use client'

import { GoogleAnalyticsTracker, useGoogleAnalytics } from './Analytics'
import { useEffect, Suspense } from 'react'

export function AnalyticsProvider({ children }: { children: React.ReactNode }) {
  // This will automatically track page views (without searchParams)
  useGoogleAnalytics()

  // Track initial page load
  useEffect(() => {
    // Send initial page view
    if (typeof window !== 'undefined' && window.gtag) {
      window.gtag('event', 'page_view', {
        page_title: document.title,
        page_location: window.location.href,
      })
    }
  }, [])

  return (
    <>
      {children}
      {/* Track page views with search params in a Suspense boundary */}
      <Suspense fallback={null}>
        <GoogleAnalyticsTracker />
      </Suspense>
    </>
  )
}
