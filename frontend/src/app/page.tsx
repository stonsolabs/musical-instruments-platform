import React from 'react';
import { Metadata } from 'next';
import HomePageClient from '@/components/HomePageClient';

export const metadata: Metadata = {
  title: 'Musical Instruments Platform - Find Your Perfect Instrument',
  description: 'Compare musical instruments, read expert reviews, and find the best prices from trusted retailers worldwide.',
};

export const dynamic = 'force-dynamic';

export default function HomePage() {
  return <HomePageClient />;
}


