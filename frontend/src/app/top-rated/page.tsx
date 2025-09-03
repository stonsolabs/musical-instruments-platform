import React from 'react';
import { Metadata } from 'next';
import { serverApi } from '@/lib/server-api';
import TopRatedClient from './TopRatedClient';

export const metadata: Metadata = {
  title: 'Top Rated Musical Instruments - Community Favorites',
  description: 'Discover the highest rated musical instruments as voted by our community. Find guitars, pianos, drums, and more with expert reviews.',
  keywords: 'top rated musical instruments, best guitars, highest rated pianos, community favorites, instrument reviews',
  openGraph: {
    title: 'Top Rated Musical Instruments - Community Favorites',
    description: 'Discover the highest rated musical instruments as voted by our community.',
    type: 'website',
    url: 'https://getyourmusicgear.com/top-rated',
  },
};

export default async function TopRatedPage() {
  // Server-side data fetching for SSR with error handling
  let mostVotedData;
  
  try {
    console.log('🔍 Top rated page: Server-side data fetching started');
    mostVotedData = await serverApi.getMostVotedProducts(50);
    console.log('✅ Top rated page: Server-side data fetching completed', {
      productsCount: mostVotedData?.products?.length || 0
    });
  } catch (error) {
    console.error('🚨 Top rated page: Server-side data fetching failed', error);
    // Provide fallback data to prevent 500 errors
    mostVotedData = { products: [] };
  }

  const products = mostVotedData?.products || [];

  return <TopRatedClient initialProducts={products} />;
}