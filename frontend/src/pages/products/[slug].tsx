import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import Head from 'next/head';
import { GetServerSideProps } from 'next';
import type { Product } from '@/types';
import { trackProductView, trackEvent } from '@/components/Analytics';
import { getApiBaseUrl } from '@/lib/api';

// Inline utility functions
const formatPrice = (price: number, currency: string = 'EUR'): string => {
  try {
    return new Intl.NumberFormat('en-GB', { style: 'currency', currency }).format(price);
  } catch {
    return `${currency} ${price.toFixed(2)}`;
  }
};

const formatRating = (rating: number): string => {
  return Number.isFinite(rating) ? rating.toFixed(1) : '0.0';
};

const API_BASE_URL = getApiBaseUrl();

interface ProductDetailPageProps {
  product: Product | null;
  error?: string;
}

export default function ProductDetailPage({ product, error }: ProductDetailPageProps) {
  const router = useRouter();
  const [selectedImage, setSelectedImage] = useState(0);

  useEffect(() => {
    if (product) {
      // Track product view
      trackProductView(
        product.id.toString(),
        product.name,
        product.category?.name || 'unknown',
        product.best_price?.price
      );
    }
  }, [product]);

  if (error || !product) {
    return (
      <>
        <Head>
          <title>Product Not Found - Musical Instruments</title>
          <meta name="description" content="The requested product could not be found." />
        </Head>
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">Product Not Found</h1>
            <Link href="/products" className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors">Browse All Products</Link>
          </div>
        </div>
      </>
    );
  }

  // Generate structured data for SEO
  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    description: product.description || `Buy ${product.name} from top music stores. Compare prices and find the best deals.`,
    brand: {
      '@type': 'Brand',
      name: product.brand?.name || 'Unknown Brand',
    },
    category: product.category?.name || 'Musical Instrument',
    url: `https://getyourmusicgear.com/products/${product.slug}`,
    image: product.images?.[0] || '/images/default-product.jpg',
    offers: product.prices && product.prices.length > 0 ? product.prices.map(price => ({
      '@type': 'Offer',
      price: price.price,
      priceCurrency: price.currency,
      availability: price.is_available ? 'https://schema.org/InStock' : 'https://schema.org/OutOfStock',
      seller: {
        '@type': 'Organization',
        name: price.store.name,
      },
      url: price.affiliate_url,
    })) : undefined,
    aggregateRating: product.avg_rating && product.avg_rating > 0 ? {
      '@type': 'AggregateRating',
      ratingValue: product.avg_rating,
      reviewCount: product.review_count || 0,
    } : undefined,
  };

  return (
    <>
      <Head>
        <title>{product.name} - Musical Instruments</title>
        <meta name="description" content={product.description || `Buy ${product.name} from top music stores. Compare prices and find the best deals.`} />
        <meta name="keywords" content={`${product.name}, ${product.brand?.name || ''}, ${product.category?.name || ''}, musical instruments, music gear`} />
        
        {/* Open Graph */}
        <meta property="og:title" content={product.name} />
        <meta property="og:description" content={product.description || `Buy ${product.name} from top music stores.`} />
        <meta property="og:type" content="product" />
        <meta property="og:url" content={`https://getyourmusicgear.com/products/${product.slug}`} />
        {product.images?.[0] && <meta property="og:image" content={product.images[0]} />}
        
        {/* Twitter Card */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content={product.name} />
        <meta name="twitter:description" content={product.description || `Buy ${product.name} from top music stores.`} />
        {product.images?.[0] && <meta name="twitter:image" content={product.images[0]} />}
        
        {/* Structured Data */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
        />
      </Head>

      <div className="min-h-screen bg-gray-50">
        {/* Breadcrumb */}
        <nav className="bg-white border-b">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <ol className="flex items-center space-x-2 text-sm text-gray-600">
              <li><Link href="/" className="hover:text-blue-600">Home</Link></li>
              <li>/</li>
              <li><Link href="/products" className="hover:text-blue-600">Products</Link></li>
              {product.category && (
                <>
                  <li>/</li>
                  <li><Link href={`/products?category=${product.category.slug}`} className="hover:text-blue-600">{product.category.name}</Link></li>
                </>
              )}
              <li>/</li>
              <li className="text-gray-900" aria-current="page">{product.name}</li>
            </ol>
          </div>
        </nav>

        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid lg:grid-cols-2 gap-12">
            {/* Product Images */}
            <div className="space-y-4">
              <div className="aspect-w-1 aspect-h-1 bg-gray-200 rounded-lg overflow-hidden">
                <img
                  src={product.images?.[selectedImage] || '/images/default-product.jpg'}
                  alt={product.name}
                  className="w-full h-full object-cover"
                />
              </div>
              {product.images && product.images.length > 1 && (
                <div className="grid grid-cols-4 gap-2">
                  {product.images.map((image, index) => (
                    <button
                      key={index}
                      onClick={() => setSelectedImage(index)}
                      className={`aspect-w-1 aspect-h-1 rounded-lg overflow-hidden border-2 ${
                        selectedImage === index ? 'border-blue-500' : 'border-gray-200'
                      }`}
                    >
                      <img
                        src={image}
                        alt={`${product.name} - Image ${index + 1}`}
                        className="w-full h-full object-cover"
                      />
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Product Info */}
            <div className="space-y-6">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">{product.name}</h1>
                <div className="flex items-center gap-4 text-sm text-gray-600 mb-4">
                  {product.brand && (
                    <span>Brand: <Link href={`/products?brand=${product.brand.slug}`} className="text-blue-600 hover:underline">{product.brand.name}</Link></span>
                  )}
                  {product.category && (
                    <span>Category: <Link href={`/products?category=${product.category.slug}`} className="text-blue-600 hover:underline">{product.category.name}</Link></span>
                  )}
                </div>
                
                {product.avg_rating && product.avg_rating > 0 && (
                  <div className="flex items-center gap-2 mb-4">
                    <div className="flex items-center">
                      {[...Array(5)].map((_, i) => (
                        <span key={i} className={`text-lg ${i < Math.floor(product.avg_rating!) ? 'text-yellow-400' : 'text-gray-300'}`}>
                          ★
                        </span>
                      ))}
                    </div>
                    <span className="text-sm text-gray-600">
                      {formatRating(product.avg_rating)} ({product.review_count || 0} reviews)
                    </span>
                  </div>
                )}
              </div>

              {product.description && (
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Description</h3>
                  <p className="text-gray-600 leading-relaxed">{product.description}</p>
                </div>
              )}

              {/* Product Specifications */}
              {product.specifications && Object.keys(product.specifications).length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Specifications</h3>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <dl className="space-y-2">
                      {Object.entries(product.specifications).map(([key, value]) => (
                        <div key={key} className="flex justify-between">
                          <dt className="text-sm font-medium text-gray-600 capitalize">{key.replace(/_/g, ' ')}</dt>
                          <dd className="text-sm text-gray-900">{value}</dd>
                        </div>
                      ))}
                    </dl>
                  </div>
                </div>
              )}

              {/* Pricing and Store Links */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Available at</h3>
                <div className="space-y-3">
                  {product.prices && product.prices.length > 0 ? (
                    product.prices.map((price) => (
                      <a
                        key={price.id}
                        href={price.affiliate_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        onClick={() => trackEvent('product_click', {
                          product_id: product.id,
                          store_name: price.store.name,
                          price: price.price,
                        })}
                        className={`block w-full text-center py-3 px-4 rounded-lg font-semibold transition-colors ${
                          price.is_available
                            ? 'bg-blue-600 text-white hover:bg-blue-700'
                            : 'bg-gray-300 text-gray-600 cursor-not-allowed'
                        }`}
                      >
                        {formatPrice(price.price, price.currency)} at {price.store.name}
                        {!price.is_available && ' (Out of Stock)'}
                      </a>
                    ))
                  ) : (
                    <div className="space-y-3">
                      <a
                        href={`https://amazon.com/s?k=${encodeURIComponent(product.name)}&aff=123`}
                        target="_blank"
                        rel="noopener noreferrer"
                        onClick={() => trackEvent('product_click', {
                          product_id: product.id,
                          store_name: 'Amazon',
                        })}
                        className="block w-full text-center py-3 px-4 bg-orange-500 text-white rounded-lg font-semibold hover:bg-orange-600 transition-colors"
                      >
                        Check on Amazon
                      </a>
                      <a
                        href={`https://thomann.com/intl/search_dir.html?sw=${encodeURIComponent(product.name)}&aff=123`}
                        target="_blank"
                        rel="noopener noreferrer"
                        onClick={() => trackEvent('product_click', {
                          product_id: product.id,
                          store_name: 'Thomann',
                        })}
                        className="block w-full text-center py-3 px-4 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors"
                      >
                        Check on Thomann
                      </a>
                      <a
                        href={`https://gear4music.com/search?search=${encodeURIComponent(product.name)}&aff=123`}
                        target="_blank"
                        rel="noopener noreferrer"
                        onClick={() => trackEvent('product_click', {
                          product_id: product.id,
                          store_name: 'Gear4Music',
                        })}
                        className="block w-full text-center py-3 px-4 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 transition-colors"
                      >
                        Check on Gear4Music
                      </a>
                    </div>
                  )}
                </div>
              </div>

              {/* Compare Button */}
              <div>
                <Link
                  href={`/compare?products=${product.slug}`}
                  className="block w-full text-center py-3 px-4 bg-gray-800 text-white rounded-lg font-semibold hover:bg-gray-700 transition-colors"
                >
                  Compare with Other Instruments
                </Link>
              </div>
            </div>
          </div>

          {/* Related Products Section */}
          {product.related_products && product.related_products.length > 0 && (
            <section className="mt-16">
              <h2 className="text-2xl font-bold text-gray-900 mb-8">Related Products</h2>
              <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
                {product.related_products.map((relatedProduct) => (
                  <Link
                    key={relatedProduct.id}
                    href={`/products/${relatedProduct.slug}`}
                    className="group block bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow"
                  >
                    <div className="aspect-w-1 aspect-h-1 bg-gray-200">
                      <img
                        src={relatedProduct.images?.[0] || '/images/default-product.jpg'}
                        alt={relatedProduct.name}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform"
                      />
                    </div>
                    <div className="p-4">
                      <h3 className="font-semibold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
                        {relatedProduct.name}
                      </h3>
                      {relatedProduct.best_price && (
                        <p className="text-lg font-bold text-gray-900">
                          {formatPrice(relatedProduct.best_price.price, relatedProduct.best_price.currency)}
                        </p>
                      )}
                    </div>
                  </Link>
                ))}
              </div>
            </section>
          )}
        </div>
      </div>
    </>
  );
}

// SEO and Performance Optimization: This page is prepared to scale to thousands of indexed pages
// by using getServerSideProps for dynamic content and implementing proper caching strategies.
export const getServerSideProps: GetServerSideProps<ProductDetailPageProps> = async (context) => {
  try {
    const { slug } = context.params!;
    const slugString = Array.isArray(slug) ? slug[0] : slug;
    
    // Extract product ID from slug (format: product-name-123)
    const idPart = slugString.split('-').pop();
    const productId = Number(idPart);
    
    if (!Number.isFinite(productId)) {
      return {
        props: {
          product: null,
          error: 'Invalid product ID',
        },
      };
    }

    // Fetch product data
    const response = await fetch(`${API_BASE_URL}/products/${productId}`);
    
    if (!response.ok) {
      return {
        props: {
          product: null,
          error: 'Product not found',
        },
      };
    }

    const product = await response.json();

    return {
      props: {
        product,
      },
      // Revalidate every 10 minutes for fresh content while maintaining good performance
      // This is crucial for scaling to thousands of pages as it reduces server load
      revalidate: 600,
    };
  } catch (error) {
    console.error('Error in getServerSideProps:', error);
    
    return {
      props: {
        product: null,
        error: 'Failed to load product',
      },
      revalidate: 600,
    };
  }
};
