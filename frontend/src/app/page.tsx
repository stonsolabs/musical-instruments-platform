import React from 'react';
import { Metadata } from 'next';
import { serverApi } from '@/lib/server-api';
import HomePageClient from '@/components/HomePageClient';

export const metadata: Metadata = {
  title: 'Musical Instruments Platform - Find Your Perfect Instrument',
  description: 'Compare musical instruments, read expert reviews, and find the best prices from trusted retailers worldwide.',
};

export default async function HomePage() {
  console.log('🚀 Server-side: HomePage component executing...');
  
  // Server-side data fetching for SSR
  const [trendingData, mostVotedData] = await Promise.allSettled([
    serverApi.getTrendingProducts(12),
    serverApi.getMostVotedProducts(12)
  ]);

  const popularProducts = trendingData.status === 'fulfilled' 
    ? trendingData.value.products || [] 
    : [];

  const topRatedProducts = mostVotedData.status === 'fulfilled' 
    ? mostVotedData.value.products || [] 
    : [];

  console.log('✅ Server-side: Data fetched successfully', {
    popularCount: popularProducts.length,
    topRatedCount: topRatedProducts.length,
    trendingStatus: trendingData.status,
    mostVotedStatus: mostVotedData.status
  });

  return (
    <HomePageClient 
      initialPopularProducts={popularProducts}
      initialTopRatedProducts={topRatedProducts}
    />
  );
}


