import React from 'react';
import { Metadata } from 'next';
import TopRatedClient from './TopRatedClient';

export const metadata: Metadata = {
  title: 'Top Rated Musical Instruments | GetYourMusicGear',
  description: 'Discover the highest-rated musical instruments based on user votes. Find the most loved guitars, keyboards, drums, and more gear chosen by musicians.',
  keywords: 'top rated musical instruments, best rated gear, user reviews, popular instruments, voted instruments',
  openGraph: {
    title: 'Top Rated Musical Instruments | GetYourMusicGear',
    description: 'Discover the highest-rated musical instruments based on user votes.',
    type: 'website',
  },
};

export default function TopRatedPage() {
  return <TopRatedClient />;
}
