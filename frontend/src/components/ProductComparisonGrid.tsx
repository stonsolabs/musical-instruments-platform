'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import type { Product, SearchAutocompleteProduct } from '@/types';
import UnifiedSearchAutocomplete from '@/components/UnifiedSearchAutocomplete';
import { formatPrice, formatRating } from '@/lib/utils';

interface ProductComparisonGridProps {
  products: Product[];
  onRemoveProduct: (productSlug: string) => void;
  onAddProduct: (product: Product) => void;
  maxProducts?: number;
}

export default function ProductComparisonGrid({ 
  products, 
  onRemoveProduct, 
  onAddProduct, 
  maxProducts = 4 
}: ProductComparisonGridProps) {
  const [showAddProduct, setShowAddProduct] = useState(false);
  const [isAddingProduct, setIsAddingProduct] = useState(false);

  const canAddMore = products.length < maxProducts;

  const handleAddProduct = async (product: SearchAutocompleteProduct) => {
    if (!canAddMore) return;
    
    setIsAddingProduct(true);
    try {
      // Convert SearchAutocompleteProduct to Product type
      const convertedProduct: Product = {
        id: product.id,
        sku: product.slug, // Use slug as SKU since SearchAutocompleteProduct doesn't have sku
        name: product.name,
        slug: product.slug,
        brand: product.brand,
        category: product.category,
        description: '', // SearchAutocompleteProduct doesn't have description
        specifications: {}, // SearchAutocompleteProduct doesn't have specifications
        images: product.images,
        msrp_price: undefined,
        best_price: product.best_price ? {
          id: 0, // Generate a temporary ID
          price: product.best_price.price,
          currency: product.best_price.currency,
          affiliate_url: product.best_price.affiliate_url,
          last_checked: new Date().toISOString(),
          is_available: true,
          store: {
            id: product.best_price.store.id,
            name: product.best_price.store.name,
            logo_url: undefined,
            website_url: '' // Add required field
          }
        } : undefined,
        prices: product.prices?.map(price => ({
          id: price.id,
          price: price.price,
          currency: price.currency,
          affiliate_url: price.affiliate_url,
          last_checked: price.last_checked || new Date().toISOString(),
          is_available: price.is_available,
          store: {
            id: price.store.id,
            name: price.store.name,
            logo_url: undefined,
            website_url: '' // Add required field
          }
        })),
        avg_rating: product.avg_rating,
        review_count: product.review_count,
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        ai_content: undefined
      };
      
      onAddProduct(convertedProduct);
      setShowAddProduct(false);
    } catch (error) {
      console.error('Error adding product:', error);
    } finally {
      setIsAddingProduct(false);
    }
  };

  // Determine grid layout based on product count
  const getGridLayout = () => {
    const count = products.length;
    if (count === 1) return 'grid-cols-1 max-w-sm';
    if (count === 2) return 'grid-cols-1 sm:grid-cols-2';
    if (count === 3) return 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3';
    return 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4';
  };

  return (
    <div className="mb-8">
      {/* Desktop Layout */}
      <div className="hidden lg:flex gap-4 items-start">
        {/* Products Grid */}
        <div className={`grid gap-4 flex-1 ${getGridLayout()}`}>
          {products.map((product) => (
            <ProductCard 
              key={product.id} 
              product={product} 
              onRemove={() => onRemoveProduct(product.slug)}
              showRemoveButton={products.length > 1}
            />
          ))}
          
          {/* Add Product Card - Always show if can add more */}
          {canAddMore && (
            <AddProductCard 
              onAddProduct={handleAddProduct}
              showSearch={showAddProduct}
              onToggleSearch={() => setShowAddProduct(!showAddProduct)}
              isAdding={isAddingProduct}
            />
          )}
        </div>
      </div>

      {/* Mobile/Tablet Layout */}
      <div className="lg:hidden space-y-6">
        {/* Products Grid */}
        <div className={`grid gap-4 ${getGridLayout()}`}>
          {products.map((product) => (
            <ProductCard 
              key={product.id} 
              product={product} 
              onRemove={() => onRemoveProduct(product.slug)}
              showRemoveButton={products.length > 1}
              isMobile={true}
            />
          ))}
        </div>

        {/* Add Product Card - Mobile */}
        {canAddMore && (
          <div className="flex justify-center">
            <AddProductCard 
              onAddProduct={handleAddProduct}
              showSearch={showAddProduct}
              onToggleSearch={() => setShowAddProduct(!showAddProduct)}
              isAdding={isAddingProduct}
              isMobile={true}
            />
          </div>
        )}
      </div>
    </div>
  );
}

// Individual Product Card Component
interface ProductCardProps {
  product: Product;
  onRemove: () => void;
  showRemoveButton: boolean;
  isMobile?: boolean;
}

function ProductCard({ product, onRemove, showRemoveButton, isMobile = false }: ProductCardProps) {
  return (
    <div className="bg-white rounded-xl shadow-elegant border border-primary-200 overflow-hidden relative">
      {/* Remove Button */}
      {showRemoveButton && (
        <button
          onClick={onRemove}
          className="absolute top-3 right-3 z-10 w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center hover:bg-red-600 transition-colors text-xs font-bold shadow-md"
          title="Remove from comparison"
        >
          ×
        </button>
      )}
      
      <div className={isMobile ? "p-4" : "p-6"}>
        {/* Product Image */}
        <Link href={`/products/${product.slug}-${product.id}`} className="block mb-4">
          <div className="aspect-square bg-gradient-to-br from-primary-100 to-primary-200 rounded-lg flex items-center justify-center overflow-hidden hover:shadow-md transition-shadow">
            {product.images && product.images.length > 0 ? (
              <img 
                src={product.images[0]} 
                alt={product.name}
                className="w-full h-full object-contain"
              />
            ) : (
              <span className={`text-primary-400 ${isMobile ? 'text-3xl' : 'text-4xl'}`}>🎸</span>
            )}
          </div>
        </Link>
        
        {/* Product Info */}
        <div className="space-y-4">
          {/* Brand and Name */}
          <div>
            <p className="text-sm text-primary-600 mb-1">{product.brand.name}</p>
            <Link href={`/products/${product.slug}-${product.id}`} className="block">
              <h3 className={`font-semibold text-primary-900 line-clamp-2 hover:text-accent-600 transition-colors ${isMobile ? 'text-sm' : ''}`}>
                {product.name}
              </h3>
            </Link>
          </div>

          {/* Expert Ratings */}
          <div className={isMobile ? "h-auto" : "h-24"}>
            {product.ai_content ? (
              <div className={`p-3 bg-primary-50 rounded-lg ${isMobile ? 'h-auto' : 'h-full'}`}>
                <h4 className="text-sm font-semibold text-primary-700 mb-2">Expert Ratings</h4>
                <div className="grid grid-cols-2 gap-2">
                  <div className="text-center">
                    <div className={`font-bold text-success-600 ${isMobile ? 'text-sm' : 'text-lg'}`}>
                      {product.ai_content.professional_assessment.expert_rating.build_quality}/10
                    </div>
                    <div className="text-xs text-primary-600">Build</div>
                  </div>
                  <div className="text-center">
                    <div className={`font-bold text-accent-600 ${isMobile ? 'text-sm' : 'text-lg'}`}>
                      {product.ai_content.professional_assessment.expert_rating.sound_quality}/10
                    </div>
                    <div className="text-xs text-primary-600">Sound</div>
                  </div>
                  <div className="text-center">
                    <div className={`font-bold text-warning-600 ${isMobile ? 'text-sm' : 'text-lg'}`}>
                      {product.ai_content.professional_assessment.expert_rating.value_for_money}/10
                    </div>
                    <div className="text-xs text-primary-600">Value</div>
                  </div>
                  <div className="text-center">
                    <div className={`font-bold text-primary-600 ${isMobile ? 'text-sm' : 'text-lg'}`}>
                      {product.ai_content.professional_assessment.expert_rating.versatility}/10
                    </div>
                    <div className="text-xs text-primary-600">Versatility</div>
                  </div>
                </div>
              </div>
            ) : (
              <div className={`p-3 bg-gray-50 rounded-lg ${isMobile ? 'h-auto' : 'h-full'} flex items-center justify-center`}>
                <p className="text-sm text-gray-500">No ratings available</p>
              </div>
            )}
          </div>

          {/* Store Buttons */}
          <div className="space-y-2 h-24 flex flex-col">
            {product.prices && product.prices.length > 0 ? (
              <>
                {product.prices.slice(0, 2).map((price) => {
                  const isThomann = price.store.name.toLowerCase().includes('thomann');
                  const isGear4Music = price.store.name.toLowerCase().includes('gear4music');
                  
                  if (isThomann) {
                    return (
                      <div key={price.id} className="flex gap-1 flex-shrink-0">
                        <a
                          href={price.affiliate_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="fp-table__column-button inline-flex items-center gap-1 px-3 py-2 bg-cyan-500 hover:bg-cyan-600 text-white text-xs font-medium rounded transition-colors"
                        >
                          <img src="/thoman-favicon.png" alt="T" className="w-3 h-3" />
                          <span>View Price</span>
                        </a>
                      </div>
                    );
                  } else if (isGear4Music) {
                    return (
                      <div key={price.id} className="flex gap-1 flex-shrink-0">
                        <a
                          href={price.affiliate_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="fp-table__column-button inline-flex items-center gap-1 px-3 py-2 bg-orange-500 hover:bg-orange-600 text-white text-xs font-medium rounded transition-colors"
                        >
                          <img src="/gear-100.png" alt="G" className="w-3 h-3" />
                          <span>View Price</span>
                        </a>
                      </div>
                    );
                  } else {
                    return (
                      <div key={price.id} className="flex gap-1 flex-shrink-0">
                        <a 
                          href={price.affiliate_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="fp-table__column-button inline-flex items-center gap-1 px-3 py-2 bg-primary-600 hover:bg-primary-700 text-white text-xs font-medium rounded transition-colors"
                        >
                          <span>View Price</span>
                        </a>
                      </div>
                    );
                  }
                })}
                {product.prices.length > 2 && (
                  <div className="text-center pt-1">
                    <Link 
                      href={`/products/${product.slug}-${product.id}`}
                      className="text-xs text-primary-600 hover:text-primary-800 font-medium"
                    >
                      +{product.prices.length - 2} more stores
                    </Link>
                  </div>
                )}
              </>
            ) : (
              <>
                <div className="flex gap-1 flex-shrink-0">
                  <a
                    href={`https://thomann.com/intl/search_dir.html?sw=${encodeURIComponent(product.name)}&aff=123`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="fp-table__column-button inline-flex items-center gap-1 px-3 py-2 bg-cyan-500 hover:bg-cyan-600 text-white text-xs font-medium rounded transition-colors"
                  >
                    <img src="/thoman-favicon.png" alt="T" className="w-3 h-3" />
                    <span>View Price</span>
                  </a>
                </div>
                <div className="flex gap-1 flex-shrink-0">
                  <a
                    href={`https://gear4music.com/search?search=${encodeURIComponent(product.name)}&aff=123`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="fp-table__column-button inline-flex items-center gap-1 px-3 py-2 bg-orange-500 hover:bg-orange-600 text-white text-xs font-medium rounded transition-colors"
                  >
                    <img src="/gear-100.png" alt="G" className="w-3 h-3" />
                    <span>View Price</span>
                  </a>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// Add Product Card Component
interface AddProductCardProps {
  onAddProduct: (product: SearchAutocompleteProduct) => void;
  showSearch: boolean;
  onToggleSearch: () => void;
  isAdding: boolean;
  isMobile?: boolean;
}

function AddProductCard({ onAddProduct, showSearch, onToggleSearch, isAdding, isMobile = false }: AddProductCardProps) {
  return (
    <div className={`bg-white rounded-xl shadow-elegant border-2 border-dashed border-primary-300 p-4 hover:border-primary-400 transition-colors cursor-pointer ${isMobile ? 'max-w-sm w-full' : 'h-fit sticky top-6'}`}>
      <div className="text-center">
        <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center mb-3 mx-auto">
          <svg className="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
        </div>
        <h4 className="font-semibold text-primary-900 mb-2 text-sm">Add More Instruments</h4>
        <p className="text-xs text-primary-600 mb-3">Compare with additional products</p>
        
        {showSearch ? (
          <div className="w-full">
            <UnifiedSearchAutocomplete
              variant="product-select"
              placeholder="Search for instruments..."
              className="w-full mb-3"
              onProductSelect={onAddProduct}
            />
            <button 
              onClick={onToggleSearch}
              className="text-xs text-primary-600 hover:text-primary-800"
              disabled={isAdding}
            >
              {isAdding ? 'Adding...' : 'Cancel'}
            </button>
          </div>
        ) : (
          <button
            onClick={onToggleSearch}
            className="bg-primary-600 text-white px-3 py-2 rounded-lg hover:bg-primary-700 transition-colors text-xs font-medium w-full"
            disabled={isAdding}
          >
            Add Product
          </button>
        )}
      </div>
    </div>
  );
}
