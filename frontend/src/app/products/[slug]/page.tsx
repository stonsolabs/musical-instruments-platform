import React from 'react';
import Link from 'next/link';
import type { Product } from '@/types';
import type { Metadata } from 'next';
import { serverApi } from '@/lib/server-api';
import ProductDetailClient from '@/components/ProductDetailClient';

export const dynamic = 'force-dynamic';

// Generate metadata for SEO
export async function generateMetadata({ params }: { params: { slug: string } }): Promise<Metadata> {
  try {
    const product = await serverApi.getProduct(params.slug);
    
    if (!product) {
      return {
        title: 'Product Not Found',
        description: 'The requested product could not be found.',
      };
    }

  return {
    title: `${product.name} - ${product.brand?.name || 'Unknown Brand'}`,
    description: product.description || `Compare prices for ${product.name} from top music stores. Expert reviews and detailed specifications.`,
    keywords: `${product.name}, ${product.brand?.name || ''}, ${product.category?.name || ''}, musical instruments, buy online`,
    openGraph: {
      title: `${product.name} - ${product.brand?.name || 'Unknown Brand'}`,
      description: product.description || `Compare prices for ${product.name} from top music stores.`,
      type: 'website',
      url: `https://getyourmusicgear.com/products/${params.slug}`,
      images: product.images?.map(img => ({
        url: img,
        width: 800,
        height: 600,
        alt: product.name,
      })) || [],
    },
    twitter: {
      card: 'summary_large_image',
      title: `${product.name} - ${product.brand?.name || 'Unknown Brand'}`,
      description: product.description || `Compare prices for ${product.name} from top music stores.`,
      images: product.images?.[0] ? [product.images[0]] : [],
    },
  };
  } catch (error) {
    console.error('🚨 Error in generateMetadata:', error);
    // Return fallback metadata when backend is down
    return {
      title: `Product: ${params.slug}`,
      description: 'Product details and pricing information from top music stores.',
    };
  }
}

export default async function ProductDetailPage({ params }: { params: { slug: string } }) {
  let product = null;
  
  try {
    console.log('🔍 Product page: fetching product with slug:', params.slug);
    product = await serverApi.getProduct(params.slug);
  } catch (error) {
    console.error('🚨 Server-side error fetching product:', error);
    // Don't throw the error, continue with null product to show error state
  }

  return (
    <div className="min-h-screen bg-white">
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