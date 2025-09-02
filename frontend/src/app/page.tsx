import React, { Suspense } from 'react';
import { Metadata } from 'next';
import HomePageClient from './HomePageClient';

// Force dynamic rendering since this shows database products
export const dynamic = 'force-dynamic';

export const metadata: Metadata = {
  title: 'Musical Instruments Comparison - Find Your Perfect Instrument',
  description: 'Compare musical instruments from top retailers. Find guitars, pianos, drums, and more with expert reviews and real-time pricing.',
  keywords: 'musical instruments, guitar, piano, drums, comparison, reviews, deals',
  openGraph: {
    title: 'Musical Instruments Comparison - Find Your Perfect Instrument',
    description: 'Compare musical instruments from top retailers with expert reviews and real-time pricing.',
    type: 'website',
    url: 'https://getyourmusicgear.com',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Musical Instruments Comparison - Find Your Perfect Instrument',
    description: 'Compare musical instruments from top retailers with expert reviews and real-time pricing.',
  },
};

export default function HomePage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
        <div className="animate-pulse">
          <div className="h-96 bg-gray-200"></div>
          <div className="max-w-6xl mx-auto px-4 py-16">
            <div className="grid md:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="bg-white rounded-lg p-6 h-80"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    }>
      <HomePageClient />
    </Suspense>
  );
}