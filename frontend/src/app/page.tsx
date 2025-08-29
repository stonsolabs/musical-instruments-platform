import React from 'react';
import type { Metadata } from 'next';
import HomePageClient from '@/components/HomePageClient';

export const metadata: Metadata = {
  title: 'Compare Musical Instruments - Find Your Perfect Instrument | Get Your Music Gear',
  description: 'Compare musical instruments with expert reviews, detailed specifications, and real-time pricing from trusted retailers. Find the perfect guitar, piano, drums, and more.',
  keywords: 'musical instruments, guitar, piano, drums, comparison, reviews, deals, music gear',
  alternates: {
    canonical: 'https://getyourmusicgear.com',
  },
  openGraph: {
    title: 'Compare Musical Instruments - Find Your Perfect Instrument',
    description: 'Compare musical instruments with expert reviews, detailed specifications, and real-time pricing from trusted retailers.',
    url: 'https://getyourmusicgear.com',
    siteName: 'Get Your Music Gear',
    images: [
      {
        url: '/logo.png',
        width: 1200,
        height: 630,
        alt: 'Get Your Music Gear - Compare Musical Instruments',
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
};

export default function HomePage() {
  return <HomePageClient />;
}


