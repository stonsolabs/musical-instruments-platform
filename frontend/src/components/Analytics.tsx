'use client'

import Script from 'next/script'

// Google Tag Manager Component
export function GoogleTagManager() {
  const gtmId = process.env.NEXT_PUBLIC_GTM_ID

  // If no GTM ID is set, don't render anything to prevent errors
  if (!gtmId || gtmId === 'GTM-XXXXXXX') {
    console.warn('Google Tag Manager ID not configured. Set NEXT_PUBLIC_GTM_ID in your environment variables.');
    return null
  }

  return (
    <Script
      id="google-tag-manager"
      strategy="afterInteractive"
      dangerouslySetInnerHTML={{
        __html: `
          (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
          new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
          j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
          'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
          })(window,document,'script','dataLayer','${gtmId}');
        `,
      }}
    />
  )
}

// Vercel Analytics Component - Removed, using GTM and Google Analytics instead

// Helper functions for custom event tracking via GTM
export const trackEvent = (eventName: string, parameters?: Record<string, any>) => {
  pushToDataLayer({
    event: eventName,
    ...parameters
  })
}

export const trackPurchase = (transactionId: string, value: number, currency: string = 'EUR', items?: any[]) => {
  pushToDataLayer({
    event: 'purchase',
    transaction_id: transactionId,
    value: value,
    currency: currency,
    items: items || []
  })
}

export const trackProductView = (itemId: string, itemName: string, category: string, value?: number) => {
  pushToDataLayer({
    event: 'view_item',
    currency: 'EUR',
    value: value || 0,
    items: [{
      item_id: itemId,
      item_name: itemName,
      item_category: category,
      quantity: 1
    }]
  })
}

export const trackSearch = (searchTerm: string, numberOfResults?: number) => {
  pushToDataLayer({
    event: 'search',
    search_term: searchTerm,
    number_of_results: numberOfResults
  })
}

export const trackCompare = (items: string[]) => {
  pushToDataLayer({
    event: 'compare_products',
    items: items,
    item_count: items.length
  })
}

// GTM DataLayer helper
export const pushToDataLayer = (data: Record<string, any>) => {
  if (typeof window !== 'undefined' && window.dataLayer) {
    window.dataLayer.push(data)
  }
}

// TypeScript declarations
declare global {
  interface Window {
    dataLayer: any[]
  }
}
