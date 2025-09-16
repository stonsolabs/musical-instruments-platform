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
        <div className="flex items-center justify-between">
          <h3 className="text-2xl font-bold text-gray-900 flex items-center">
             {title}
          </h3>
          <div className="animate-pulse bg-gray-200 h-4 w-16 rounded"></div>
        </div>
        <div className={`grid gap-6 ${layout === 'grid' ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3' : 'grid-cols-1'}`}>
          {products.map((_, index) => (
            <div key={index} className="animate-pulse bg-white rounded-xl shadow-lg overflow-hidden">
              <div className="bg-gray-200 aspect-square"></div>
              <div className="p-6 space-y-3">
                <div className="bg-gray-200 h-4 rounded w-3/4"></div>
                <div className="bg-gray-200 h-6 rounded"></div>
                <div className="bg-gray-200 h-4 rounded w-1/2"></div>
                <div className="bg-gray-200 h-10 rounded"></div>
              </div>
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
    grid: 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8',
    list: 'space-y-8',
    carousel: 'flex overflow-x-auto space-x-6 pb-4 scrollbar-hide'
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-2xl font-bold text-gray-900 flex items-center">
           {title}
        </h3>
        <div className="text-sm text-gray-500">
          {products.length} product{products.length !== 1 ? 's' : ''} featured
        </div>
      </div>
      
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
              className={`bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-all duration-300 hover:-translate-y-1 group ${
                layout === 'carousel' ? 'flex-shrink-0 w-80' : ''
              }`}
            >
              {/* Product Image */}
              <div className="aspect-square bg-gray-100 overflow-hidden cursor-pointer relative" onClick={openPriorityStore} title="View at top store">
                <img
                  src={imageUrl}
                  alt={product.name}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                  onError={(e) => {
                    const target = e.target as HTMLImageElement;
                    target.style.display = 'none';
                  }}
                />
                
                {/* Gradient Overlay */}
                <div className="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                
                {/* Quick Action Button */}
                <div className="absolute bottom-4 right-4 opacity-0 group-hover:opacity-100 transition-all duration-300 transform translate-y-2 group-hover:translate-y-0">
                  <button className="px-3 py-2 bg-white/90 backdrop-blur-sm rounded-lg text-gray-900 font-medium shadow-lg hover:bg-white transition-colors text-sm">
                    Quick View
                  </button>
                </div>
                
              </div>

              {/* Product Info */}
              <div className="p-6">
                

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
                  <div className="space-y-3">
                    <ProductCardButtons product={product} />
                    
                    {/* Quick Buy Button */}
                    <button
                      onClick={openPriorityStore}
                      className="w-full py-3 bg-gradient-to-r from-green-500 to-green-600 text-white font-bold rounded-lg hover:from-green-600 hover:to-green-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                    >
                      🛒 Check Latest Price
                    </button>
                  </div>
                )}

                {/* Product Actions */}
                <div className="mt-4 pt-4 border-t border-gray-100 flex items-center justify-between">
                  <a
                    href={`/products/${product.slug}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center text-brand-primary hover:text-brand-dark font-medium transition-colors"
                  >
                     Full Review
                    <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                  </a>
                  
                  {/* Social Share */}
                  <button
                    onClick={() => {
                      if (navigator.share) {
                        navigator.share({
                          title: product.name,
                          text: `Check out this ${product.category.name}`,
                          url: window.location.href,
                        });
                      }
                    }}
                    className="text-gray-500 hover:text-gray-700 transition-colors"
                    title="Share this product"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
      
      {/* CTA Section */}
      <div className="text-center p-6 bg-gradient-to-r from-gray-50 to-gray-100 rounded-xl border border-gray-200">
        <h4 className="text-lg font-semibold text-gray-900 mb-2"> Need Help Choosing?</h4>
        <p className="text-gray-600 mb-4">
          Our experts have tested and compared these products to help you make the best choice for your needs and budget.
        </p>
        <div className="flex flex-wrap justify-center gap-3">
          <a href="/compare" className="px-4 py-2 bg-white border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors">
             Compare All
          </a>
          <a href="/contact" className="px-4 py-2 bg-brand-primary text-white rounded-lg hover:bg-brand-dark transition-colors">
             Ask an Expert
          </a>
        </div>
      </div>
    </div>
  );
}
