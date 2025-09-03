import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Product } from '@/types';
import { CompactProductVoting } from '@/components/ProductVoting';
import { ThomannButton, Gear4musicButton, GenericStoreButton } from '@/components/AffiliateButton';
import { formatPrice } from '@/lib/utils';

interface ProductCardProps {
  product: Product;
  showVoting?: boolean;
  showPricing?: boolean;
  variant?: 'default' | 'compact' | 'detailed';
  className?: string;
}

export default function ProductCard({ 
  product, 
  showVoting = false, 
  showPricing = true, 
  variant = 'default',
  className = '' 
}: ProductCardProps) {
  const productSlug = product.slug;
  const productUrl = `/products/${productSlug}`;

  // Get fallback store links from content
  const thomannUrl = product.content?.store_links?.['Thomann'] || 
                    product.content?.store_links?.['thomann'] || 
                    `https://thomann.com/intl/search_dir.html?sw=${encodeURIComponent(product.name)}&aff=123`;
  
  const gear4musicUrl = product.content?.store_links?.['gear4music'] || 
                       product.content?.store_links?.['Gear4music'] || 
                       `https://gear4music.com/search?search=${encodeURIComponent(product.name)}&aff=123`;

  return (
    <div className={`bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-all duration-200 ${className}`}>
      {/* Product Image */}
      <div className="relative">
        <Link href={productUrl} className="block">
          <div className="h-48 bg-white flex items-center justify-center overflow-hidden border border-gray-200 product-image-container">
            {product.images && product.images.length > 0 ? (
              <img 
                src={product.images[0]} 
                alt={product.name}
                className="w-full h-full object-contain scale-105"
                style={{ backgroundColor: 'white' }}
                loading="lazy"
              />
            ) : (
              <span className="text-gray-400 text-2xl">🎸</span>
            )}
          </div>
        </Link>
        
        {/* Best Price Badge */}
        {product.prices && product.prices.length > 0 && (
          <div className="absolute top-2 right-2 bg-green-500 text-white px-2 py-1 rounded text-xs font-medium">
            {formatPrice(product.prices[0].price, product.prices[0].currency)}
          </div>
        )}
      </div>
      
      <div className="p-4">
        {/* Brand */}
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-gray-600">{product.brand?.name || 'Brand'}</span>
          {product.avg_rating > 0 && (
            <div className="flex items-center text-sm text-yellow-500">
              <span>⭐</span>
              <span className="ml-1 text-gray-600">{product.avg_rating.toFixed(1)}</span>
            </div>
          )}
        </div>
        
        {/* Voting Component */}
        {showVoting && (
          <div className="flex items-center justify-center mb-3">
            <CompactProductVoting 
              productId={product.id}
              initialStats={product.vote_stats}
              className=""
            />
          </div>
        )}

        {/* Product Name */}
        <Link href={productUrl} className="block">
          <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2 hover:text-accent-600 transition-colors cursor-pointer">
            {product.name}
          </h3>
        </Link>
        
        {/* Description */}
        {variant !== 'compact' && (
          <p className="text-gray-600 text-sm mb-4 line-clamp-2">
            {product.description || "High-quality musical instrument with excellent craftsmanship and sound."}
          </p>
        )}
        
        {/* Pricing and Store Links */}
        {showPricing && (
          <div className="space-y-2">
            {product.prices && product.prices.length > 0 ? (
              <>
                {product.prices
                  .slice(0, variant === 'compact' ? 2 : 3)
                  .map((price) => {
                    const isThomann = price.store.name.toLowerCase().includes('thomann');
                    const isGear4Music = price.store.name.toLowerCase().includes('gear4music');
                    
                    if (isThomann) {
                      return (
                        <ThomannButton
                          key={price.id}
                          href={price.affiliate_url}
                          isAvailable={price.is_available}
                        />
                      );
                    } else if (isGear4Music) {
                      return (
                        <Gear4musicButton
                          key={price.id}
                          href={price.affiliate_url}
                          isAvailable={price.is_available}
                        />
                      );
                    } else {
                      return (
                        <GenericStoreButton
                          key={price.id}
                          href={price.affiliate_url}
                          storeName={price.store.name}
                          isAvailable={price.is_available}
                        />
                      );
                    }
                  })
                }
              </>
            ) : (
              <>
                <ThomannButton href={thomannUrl} />
                <Gear4musicButton href={gear4musicUrl} />
              </>
            )}
          </div>
        )}

        {/* Category and additional info for detailed variant */}
        {variant === 'detailed' && (
          <div className="mt-4 pt-3 border-t border-gray-100">
            <div className="flex items-center justify-between text-xs text-gray-500">
              <span>{product.category?.name || 'Category'}</span>
              {product.review_count > 0 && (
                <span>{product.review_count} reviews</span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// Specialized variants for common use cases
export function CompactProductCard({ product, className = '' }: { product: Product; className?: string }) {
  return (
    <ProductCard 
      product={product} 
      variant="compact" 
      showPricing={true}
      showVoting={false}
      className={className}
    />
  );
}

export function VotingProductCard({ product, className = '' }: { product: Product; className?: string }) {
  return (
    <ProductCard 
      product={product} 
      variant="default" 
      showPricing={true}
      showVoting={true}
      className={className}
    />
  );
}

export function DetailedProductCard({ product, className = '' }: { product: Product; className?: string }) {
  return (
    <ProductCard 
      product={product} 
      variant="detailed" 
      showPricing={true}
      showVoting={false}
      className={className}
    />
  );
}