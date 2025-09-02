import React from 'react';
import Link from 'next/link';
import type { Product } from '@/types';
import ProductDetailClient from '@/components/ProductDetailClient';

async function fetchProduct(slug: string): Promise<Product | null> {
  try {
    const idPart = slug.split('-').pop();
    const productId = Number(idPart);
    
    if (!Number.isFinite(productId)) {
      console.error('Invalid product ID from slug:', slug);
      return null;
    }

    const apiUrl = `https://getyourmusicgear-api.azurewebsites.net/api/v1/products/${productId}`;
    const apiKey = process.env.API_KEY;

    if (!apiKey) {
      console.error('API_KEY environment variable is not set');
      return null;
    }

    const response = await fetch(apiUrl, {
      headers: {
        'X-API-Key': apiKey,
        'Content-Type': 'application/json',
      },
      next: { revalidate: 300 }, // Revalidate every 5 minutes
    });

    if (!response.ok) {
      console.error(`Product API Error: ${response.status} ${response.statusText}`);
      return null;
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching product:', error);
    return null;
  }
}

export default async function ProductDetailPage({ params }: { params: { slug: string } }) {
  const product = await fetchProduct(params.slug);

  return (
    <div className="min-h-screen bg-primary-50">
      {/* Ad Space - Top */}
      <section className="py-4 bg-white border-b">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-r from-primary-600 to-accent-600 rounded-lg p-4 text-white text-center">
            <p className="text-sm">🎵 Compare prices across Europe's top music stores</p>
          </div>
        </div>
      </section>

      <ProductDetailClient product={product} slug={params.slug} />
    </div>
  );
}