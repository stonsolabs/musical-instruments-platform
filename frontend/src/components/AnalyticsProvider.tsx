'use client'

import { GoogleTagManager } from './Analytics'
import { useEffect } from 'react'

export function AnalyticsProvider({ children }: { children: React.ReactNode }) {
  // Track initial page load
  useEffect(() => {
    // Send initial page view via GTM
    if (typeof window !== 'undefined' && window.dataLayer) {
      window.dataLayer.push({
        event: 'page_view',
        page_title: document.title,
        page_location: window.location.href,
      })
    }
  }, [])

  return (
    <>
      {children}
      <GoogleTagManager />
    </>
  )
}
