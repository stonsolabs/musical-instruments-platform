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
  // Server-side data fetching for SSR
  const mostVotedData = await serverApi.getMostVotedProducts(50);
  const products = mostVotedData?.products || [];

  return <TopRatedClient initialProducts={products} />;
}