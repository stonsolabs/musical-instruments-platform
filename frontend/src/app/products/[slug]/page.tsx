import React from 'react';
import Link from 'next/link';
import type { Product } from '@/types';
import type { Metadata } from 'next';
import { getApiBaseUrl } from '@/lib/api';
import ProductDetailClient from '@/components/ProductDetailClient';

const API_BASE_URL = getApiBaseUrl();

interface ProductPageProps {
  params: { slug: string };
}

// Generate metadata for SEO with proper canonical tags
export async function generateMetadata({ params }: ProductPageProps): Promise<Metadata> {
  const slug = params.slug;
  const idPart = slug.split('-').pop();
  const productId = Number(idPart);
  
  if (!Number.isFinite(productId)) {
    return {
      title: 'Product Not Found',
      description: 'The requested product could not be found.',
      robots: {
        index: false,
        follow: false,
      },
    };
  }

  try {
    const response = await fetch(`${API_BASE_URL}/products/${productId}`, {
      next: { revalidate: 3600 }, // Cache for 1 hour
    });
    
    if (!response.ok) {
      return {
        title: 'Product Not Found',
        description: 'The requested product could not be found.',
        robots: {
          index: false,
          follow: false,
        },
      };
    }

    const product: Product = await response.json();
    const canonicalUrl = `https://getyourmusicgear.com/products/${product.slug}-${product.id}`;

    return {
      title: `${product.name} - ${product.brand?.name || 'Musical Instrument'} | Get Your Music Gear`,
      description: product.description || `Compare prices and read reviews for ${product.name}. Find the best deals on ${product.brand?.name || 'musical instruments'}.`,
      keywords: `${product.name}, ${product.brand?.name || ''}, ${product.category?.name || ''}, musical instruments, music gear, compare prices`,
      alternates: {
        canonical: canonicalUrl,
      },
      openGraph: {
        title: `${product.name} - ${product.brand?.name || 'Musical Instrument'}`,
        description: product.description || `Compare prices and read reviews for ${product.name}.`,
        type: 'product',
        url: canonicalUrl,
        images: product.images && product.images.length > 0 ? [
          {
            url: product.images[0],
            width: 1200,
            height: 630,
            alt: product.name,
          },
        ] : undefined,
      },
      twitter: {
        card: 'summary_large_image',
        title: `${product.name} - ${product.brand?.name || 'Musical Instrument'}`,
        description: product.description || `Compare prices and read reviews for ${product.name}.`,
        images: product.images && product.images.length > 0 ? [product.images[0]] : undefined,
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
  } catch (error) {
    return {
      title: 'Product Not Found',
      description: 'The requested product could not be found.',
      robots: {
        index: false,
        follow: false,
      },
    };
  }
}

export default async function ProductDetailPage({ params }: ProductPageProps) {
  const slug = params.slug;
  const idPart = slug.split('-').pop();
  const productId = Number(idPart);
  
  if (!Number.isFinite(productId)) {
    return (
      <div className="min-h-screen bg-primary-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-primary-900 mb-4">Invalid Product</h1>
          <Link href="/products" className="bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700 transition-colors">Browse All Products</Link>
        </div>
      </div>
    );
  }

  let product: Product | null = null;
  let error = false;

  try {
    const response = await fetch(`${API_BASE_URL}/products/${productId}`, {
      next: { revalidate: 3600 }, // Cache for 1 hour
    });
    
    if (!response.ok) {
      error = true;
    } else {
      product = await response.json();
    }
  } catch (e) {
    error = true;
  }

  if (error || !product) {
    return (
      <div className="min-h-screen bg-primary-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-primary-900 mb-4">Product Not Found</h1>
          <Link href="/products" className="bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700 transition-colors">Browse All Products</Link>
        </div>
      </div>
    );
  }

  return <ProductDetailClient product={product} />;
}



