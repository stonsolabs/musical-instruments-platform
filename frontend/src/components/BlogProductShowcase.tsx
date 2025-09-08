import React, { useState, useEffect } from 'react';
import { BlogPostProduct } from '../types/blog';
import { Product } from '../types';
import { fetchProduct } from '../lib/api';
import { openTopAffiliate } from '../lib/affiliate';
import { ProductCardButtons } from './AffiliateButtons';
import { StarIcon } from '@heroicons/react/20/solid';
import { StarIcon as StarOutlineIcon } from '@heroicons/react/24/outline';
import { getRatingStars, getProductImageUrl } from '../lib/utils';

interface BlogProductShowcaseProps {
  products: BlogPostProduct[];
  title?: string;
  layout?: 'grid' | 'list' | 'carousel';
  showAffiliateButtons?: boolean;
}

export default function BlogProductShowcase({ 
  products, 
  title = "Featured Products",
  layout = 'grid',
  showAffiliateButtons = true
}: BlogProductShowcaseProps) {
  const [productDetails, setProductDetails] = useState<Record<number, Product>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProductDetails = async () => {
      try {
        const details: Record<number, Product> = {};
        
        // Fetch details for each product
        await Promise.all(
          products.map(async (productRef) => {
            try {
              const product = await fetchProduct(productRef.product_slug || productRef.product_id.toString());
              details[productRef.product_id] = product;
            } catch (error) {
              console.error(`Failed to fetch product ${productRef.product_id}:`, error);
            }
          })
        );
        
        setProductDetails(details);
      } catch (error) {
        console.error('Error fetching product details:', error);
      } finally {
        setLoading(false);
      }
    };

    if (products.length > 0) {
      fetchProductDetails();
    } else {
      setLoading(false);
    }
  }, [products]);

  if (loading) {
    return (
      <div className="space-y-6">
        <h3 className="text-2xl font-bold text-gray-900">{title}</h3>
        <div className={`grid gap-6 ${layout === 'grid' ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3' : 'grid-cols-1'}`}>
          {products.map((_, index) => (
            <div key={index} className="animate-pulse">
              <div className="bg-gray-200 h-48 rounded-lg mb-4"></div>
              <div className="bg-gray-200 h-6 rounded mb-2"></div>
              <div className="bg-gray-200 h-4 rounded mb-4"></div>
              <div className="bg-gray-200 h-10 rounded"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (products.length === 0) {
    return null;
  }

  const layoutClasses = {
    grid: 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6',
    list: 'space-y-6',
    carousel: 'flex overflow-x-auto space-x-6 pb-4'
  };

  return (
    <div className="space-y-6">
      <h3 className="text-2xl font-bold text-gray-900">{title}</h3>
      
      <div className={layoutClasses[layout]}>
        {products.map((productRef) => {
          const product = productDetails[productRef.product_id];
          
          if (!product) {
            return (
              <div key={productRef.id} className="bg-gray-50 p-6 rounded-lg">
                <p className="text-gray-500">Product not found</p>
              </div>
            );
          }

          const { full, half, empty } = getRatingStars(product.avg_rating || 0);
          const imageUrl = getProductImageUrl(product);
          
          const openPriorityStore = (e: React.MouseEvent) => openTopAffiliate(product as any, e);

          return (
            <div 
              key={productRef.id} 
              className={`bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow ${
                layout === 'carousel' ? 'flex-shrink-0 w-80' : ''
              }`}
            >
              {/* Product Image */}
              <div className="aspect-square bg-gray-100 overflow-hidden cursor-pointer" onClick={openPriorityStore} title="View at top store">
                <img
                  src={imageUrl}
                  alt={product.name}
                  className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                  onError={(e) => {
                    const target = e.target as HTMLImageElement;
                    target.style.display = 'none';
                  }}
                />
              </div>

              {/* Product Info */}
              <div className="p-6">
                {/* Context Badge */}
                {productRef.context && (
                  <div className="mb-3">
                    <span className="inline-block px-2 py-1 text-xs font-medium bg-brand-accent text-brand-primary rounded-full">
                      {productRef.context}
                    </span>
                  </div>
                )}

                {/* Brand and Category */}
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-500">{product.category.name}</span>
                  <span className="text-sm font-medium text-brand-primary">
                    {product.brand.name}
                  </span>
                </div>

                {/* Product Name */}
                <h4 className="font-semibold text-gray-900 mb-3 line-clamp-2">
                  {product.name}
                </h4>

                {/* Rating */}
                <div className="flex items-center mb-4">
                  <div className="flex items-center">
                    {[...Array(full)].map((_, i) => (
                      <StarIcon key={`full-${i}`} className="h-4 w-4 text-yellow-400" />
                    ))}
                    {[...Array(half)].map((_, i) => (
                      <StarIcon key={`half-${i}`} className="h-4 w-4 text-yellow-400" />
                    ))}
                    {[...Array(empty)].map((_, i) => (
                      <StarOutlineIcon key={`empty-${i}`} className="h-4 w-4 text-gray-300" />
                    ))}
                  </div>
                  <span className="ml-2 text-sm text-gray-500">
                    ({product.review_count || 0})
                  </span>
                </div>

                {/* Affiliate Buttons */}
                {showAffiliateButtons && (
                  <div className="space-y-2">
                    <ProductCardButtons product={product} />
                  </div>
                )}

                {/* View Product Link */}
                <div className="mt-4 pt-4 border-t border-gray-100">
                  <a
                    href={`/products/${product.slug}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center text-brand-primary hover:text-brand-dark font-medium transition-colors"
                  >
                    View Details
                    <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                  </a>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
