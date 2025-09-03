'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import type { ComparisonResponse, Product } from '@/types';
import { apiClient } from '@/lib/api';

import SpecificationsComparison from '@/components/SpecificationsComparison';
import UnifiedSearchAutocomplete from '@/components/UnifiedSearchAutocomplete';
import ProductComparisonGrid from '@/components/ProductComparisonGrid';

import { formatPrice, formatRating } from '@/lib/utils';

// Helper function to generate common specifications across products
const generateCommonSpecs = (products: Product[]): string[] => {
  if (products.length === 0) return [];
  
  try {
    // Get all specification keys from all products
    const allSpecs = new Set<string>();
    products.forEach(product => {
      if (product.specifications && typeof product.specifications === 'object') {
        Object.keys(product.specifications).forEach(key => allSpecs.add(key));
      }
    });
    
    // Filter to only specs that appear in at least one product
    const commonSpecs = Array.from(allSpecs).filter(spec => {
      return products.some(product => 
        product.specifications && 
        typeof product.specifications === 'object' &&
        product.specifications[spec] !== undefined && 
        product.specifications[spec] !== null &&
        product.specifications[spec] !== ''
      );
    });
    
    return commonSpecs.sort();
  } catch (error) {
    console.error('Error generating common specs:', error);
    return [];
  }
};

// Helper function to generate comparison matrix
const generateComparisonMatrix = (products: Product[]): {[spec: string]: {[productId: string]: any}} => {
  try {
    const matrix: {[spec: string]: {[productId: string]: any}} = {};
    const commonSpecs = generateCommonSpecs(products);
    
    commonSpecs.forEach(spec => {
      matrix[spec] = {};
      products.forEach(product => {
        const value = product.specifications && typeof product.specifications === 'object' ? product.specifications[spec] : undefined;
        matrix[spec][String(product.id)] = value || 'N/A';
      });
    });
    
    return matrix;
  } catch (error) {
    console.error('Error generating comparison matrix:', error);
    return {};
  }
};

interface CompareClientProps {
  products: Product[];
  productSlugs: string[];
}

export default function CompareClient({ products, productSlugs }: CompareClientProps) {
  // Much simpler - no complex state management needed!
  const [showPurchaseGuide, setShowPurchaseGuide] = useState(true);
  const [showUsageGuidance, setShowUsageGuidance] = useState(true);
  const [showMaintenanceCare, setShowMaintenanceCare] = useState(true);
  const [showReviews, setShowReviews] = useState(true);

  // Create comparison data from products
  const data: ComparisonResponse = {
    products,
    common_specs: generateCommonSpecs(products),
    comparison_matrix: generateComparisonMatrix(products),
    generated_at: new Date().toISOString()
  };

  // Track comparison analytics
  useEffect(() => {
    if (products.length > 0 && typeof window !== 'undefined') {
      console.log('Comparison loaded:', products.map(p => p.name));
      
      // Track comparison in backend (fire and forget)
      setTimeout(async () => {
        try {
          await apiClient.trackComparison(products.map(p => p.id));
        } catch (error) {
          console.error('Failed to track comparison:', error);
        }
      }, 100);
    }
  }, [products]);

  const handleAddProduct = (product: Product) => {
    if (product && data) {
      const newSlugs = [...productSlugs, product.slug];
      const newUrl = `/compare?products=${newSlugs.join(',')}`;
      window.location.href = newUrl;
    }
  };

  const handleRemoveProduct = (productSlug: string) => {
    if (data && data.products.length > 1) {
      const newSlugs = productSlugs.filter(slug => slug !== productSlug);
      if (newSlugs.length > 0) {
        const newUrl = `/compare?products=${newSlugs.join(',')}`;
        window.location.href = newUrl;
      } else {
        window.location.href = '/products';
      }
    }
  };

  const handleAddProductFromSearch = (searchProduct: any) => {
    // Convert search product to the format we need
    if (searchProduct && searchProduct.slug) {
      const newSlugs = [...productSlugs, searchProduct.slug];
      const newUrl = `/compare?products=${newSlugs.join(',')}`;
      window.location.href = newUrl;
    }
  };

  // No products found - much simpler handling
  if (products.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-primary-500 mb-4">No products found for comparison.</div>
        <Link 
          href="/products"
          className="bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700 transition-colors"
        >
          Browse Products
        </Link>
      </div>
    );
  }

  // Handle single product display
  const isSingleProduct = data.products.length === 1;

  // Check if comparing across different categories
  const hasDifferentCategories = new Set(data.products.map(p => p.category.name)).size > 1;

  return (
    <div className="max-w-7xl mx-auto">
      {/* Product Comparison Section */}
      <ProductComparisonGrid
        products={data.products}
        onRemoveProduct={handleRemoveProduct}
        onAddProduct={handleAddProduct}
        maxProducts={4}
      />

      {/* Category Warning */}
      {hasDifferentCategories && (
        <div className="mb-6 p-4 bg-warning-50 border border-warning-200 rounded-lg">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-warning-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-warning-800">
                Cross-Category Comparison
              </h3>
              <div className="mt-2 text-sm text-warning-700">
                <p>
                  You're comparing products across different categories. 
                  Some specifications might not be directly comparable.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Specifications Comparison - Collapsed by default */}
      {(data.products.length === 1 || data.products.some(p => Object.keys(p.specifications || {}).length > 0)) && (
        <SpecificationsComparison 
          products={data.products}
          isCollapsible={true}
          defaultCollapsed={true}
          className="mb-8"
        />
      )}

      {/* Purchase Decision Guide - Always show */}
      {data.products.length > 0 && (
        <div className="bg-white rounded-xl shadow-elegant border border-primary-200 overflow-hidden mb-8">
          <button
            onClick={() => setShowPurchaseGuide(!showPurchaseGuide)}
            className="w-full p-6 flex items-center justify-between hover:bg-primary-50 transition-colors"
          >
            <h3 className="text-xl font-semibold text-primary-900 flex items-center gap-2">
              <span className="text-2xl">🎯</span>
              Purchase Decision Guide
            </h3>
            <svg 
              className={`w-6 h-6 text-primary-600 transition-transform ${showPurchaseGuide ? 'rotate-180' : ''}`} 
              fill="none" stroke="currentColor" viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          {showPurchaseGuide && (
            <div className="px-6 pb-6">
              <div className={`grid gap-6 ${
                data.products.length === 1 
                  ? 'grid-cols-1 max-w-2xl mx-auto' 
                  : data.products.length === 2
                  ? 'grid-cols-1 sm:grid-cols-2'
                  : data.products.length === 3
                  ? 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3'
                  : 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'
              }`}>
              {data.products.map((product) => (
                <div key={product.id} className="border border-primary-200 rounded-lg p-4">
                  <h4 className="font-semibold text-primary-900 mb-4">{product.name}</h4>
                  {product.ai_content ? (
                    <div className="space-y-4">
                      {/* Why Buy */}
                      <div>
                        <h5 className="text-sm font-semibold text-success-700 mb-2">Why Buy</h5>
                        <div className="space-y-2">
                          {(product.ai_content?.purchase_decision?.why_buy || []).slice(0, 2).map((reason, index) => (
                            <div key={index} className="p-2 bg-success-50 border border-success-200 rounded text-xs">
                              <div className="font-medium text-success-800">{reason.title}</div>
                              <div className="text-success-700 mt-1">{reason.description}</div>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Why Not Buy */}
                      <div>
                        <h5 className="text-sm font-semibold text-error-700 mb-2">Considerations</h5>
                        <div className="space-y-2">
                          {(product.ai_content?.purchase_decision?.why_not_buy || []).slice(0, 1).map((reason, index) => (
                            <div key={index} className="p-2 bg-error-50 border border-error-200 rounded text-xs">
                              <div className="font-medium text-error-800">{reason.title}</div>
                              <div className="text-error-700 mt-1">{reason.description}</div>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Best For */}
                      <div>
                        <h5 className="text-sm font-semibold text-primary-700 mb-2">Best For</h5>
                        <div className="space-y-2">
                          {(product.ai_content?.purchase_decision?.best_for || []).slice(0, 1).map((userType, index) => (
                            <div key={index} className="p-2 bg-primary-50 border border-primary-200 rounded text-xs">
                              <div className="font-medium text-primary-800">{userType.user_type}</div>
                              <div className="text-primary-700 mt-1">{userType.reason}</div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  ) : (
                    <p className="text-sm text-primary-500">No purchase guidance available</p>
                  )}
                </div>
              ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Usage Guidance Comparison - Always show */}
      {data.products.length > 0 && (
        <div className="bg-white rounded-xl shadow-elegant border border-primary-200 overflow-hidden mb-8">
          <button
            onClick={() => setShowUsageGuidance(!showUsageGuidance)}
            className="w-full p-6 flex items-center justify-between hover:bg-primary-50 transition-colors"
          >
            <h3 className="text-xl font-semibold text-primary-900 flex items-center gap-2">
              <span className="text-2xl">🎵</span>
              Usage Guidance Comparison
            </h3>
            <svg 
              className={`w-6 h-6 text-primary-600 transition-transform ${showUsageGuidance ? 'rotate-180' : ''}`} 
              fill="none" stroke="currentColor" viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          {showUsageGuidance && (
            <div className="px-6 pb-6">
              <div className={`grid gap-6 ${
                data.products.length === 1 
                  ? 'grid-cols-1 max-w-2xl mx-auto' 
                  : data.products.length === 2
                  ? 'grid-cols-1 sm:grid-cols-2'
                  : data.products.length === 3
                  ? 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3'
                  : 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'
              }`}>
              {data.products.map((product) => (
                <div key={product.id} className="border border-primary-200 rounded-lg p-4">
                  <h4 className="font-semibold text-primary-900 mb-4">{product.name}</h4>
                  {product.ai_content ? (
                    <div className="space-y-4">
                      {/* Music Styles */}
                      <div>
                        <span className="text-sm font-medium text-primary-500">Best Genres</span>
                        <div className="space-y-2 mt-2">
                          <div>
                            <span className="text-xs font-medium text-success-600">Excellent:</span>
                            <div className="flex flex-wrap gap-1 mt-1">
                              {(product.ai_content?.usage_guidance?.suitable_music_styles?.excellent || []).slice(0, 2).map((style, index) => (
                                <span key={index} className="px-2 py-1 bg-success-100 text-success-800 text-xs rounded-full">
                                  {style}
                                </span>
                              ))}
                            </div>
                          </div>
                          <div>
                            <span className="text-xs font-medium text-primary-600">Good:</span>
                            <div className="flex flex-wrap gap-1 mt-1">
                              {(product.ai_content?.usage_guidance?.suitable_music_styles?.good || []).slice(0, 2).map((style, index) => (
                                <span key={index} className="px-2 py-1 bg-primary-100 text-primary-800 text-xs rounded-full">
                                  {style}
                                </span>
                              ))}
                            </div>
                          </div>
                        </div>
                      </div>

                      {/* Recommended Amplifiers */}
                      {/* <div>
                        <span className="text-sm font-medium text-primary-500">Recommended Amps</span>
                        <div className="space-y-1 mt-2">
                          {(product.ai_content?.usage_guidance?.recommended_amplifiers || []).slice(0, 3).map((amp, index) => (
                            <div key={index} className="flex items-center justify-between p-2 bg-accent-50 border border-accent-200 rounded text-xs">
                              <span className="text-accent-800 font-medium truncate flex-1 mr-2">{amp}</span>
                              <div className="flex gap-1 flex-shrink-0">
                                <a
                                  href={`https://thomann.com/intl/search_dir.html?sw=${encodeURIComponent(amp)}&aff=123`}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="fp-table__button fp-table__button--thomann text-xs px-2 py-1 min-w-[24px]"
                                >
                                  T
                                </a>
                                <a
                                  href={`https://gear4music.com/search?search=${encodeURIComponent(amp)}&aff=123`}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="fp-table__button fp-table__button--gear4music text-xs px-2 py-1 min-w-[24px]"
                                >
                                  G
                                </a>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div> */}

                      {/* Learning Curve */}
                      <div>
                        <span className="text-sm font-medium text-primary-500">Learning Curve</span>
                        <p className="text-sm text-primary-700 mt-1">{product.ai_content?.usage_guidance?.skill_development?.learning_curve || 'Learning curve information not available.'}</p>
                      </div>
                    </div>
                  ) : (
                    <p className="text-sm text-primary-500">No usage guidance available</p>
                  )}
                </div>
              ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Maintenance & Care - Always show */}
      {data.products.length > 0 && (
        <div className="bg-white rounded-xl shadow-elegant border border-primary-200 overflow-hidden mb-8">
          <button
            onClick={() => setShowMaintenanceCare(!showMaintenanceCare)}
            className="w-full p-6 flex items-center justify-between hover:bg-primary-50 transition-colors"
          >
            <h3 className="text-xl font-semibold text-primary-900 flex items-center gap-2">
              <span className="text-2xl">🔧</span>
              Maintenance & Care
            </h3>
            <svg 
              className={`w-6 h-6 text-primary-600 transition-transform ${showMaintenanceCare ? 'rotate-180' : ''}`} 
              fill="none" stroke="currentColor" viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          {showMaintenanceCare && (
            <div className="px-6 pb-6">
              <div className={`grid gap-6 ${
                data.products.length === 1 
                  ? 'grid-cols-1 max-w-2xl mx-auto' 
                  : data.products.length === 2
                  ? 'grid-cols-1 sm:grid-cols-2'
                  : data.products.length === 3
                  ? 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3'
                  : 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'
              }`}>
              {data.products.map((product) => (
                <div key={product.id} className="border border-primary-200 rounded-lg p-4">
                  <h4 className="font-semibold text-primary-900 mb-4">{product.name}</h4>
                  {product.ai_content ? (
                    <div className="space-y-4">
                      {/* Care Instructions */}
                      <div>
                        <h5 className="text-sm font-semibold text-primary-700 mb-2">Care Instructions</h5>
                        <div className="space-y-2">
                          <div>
                            <span className="text-xs font-medium text-primary-600">Daily:</span>
                            <p className="text-xs text-primary-700 mt-1">{product.ai_content?.maintenance_care?.care_instructions?.daily || 'Daily care instructions not available.'}</p>
                          </div>
                          <div>
                            <span className="text-xs font-medium text-primary-600">Weekly:</span>
                            <p className="text-xs text-primary-700 mt-1">{product.ai_content?.maintenance_care?.care_instructions?.weekly || 'Weekly care instructions not available.'}</p>
                          </div>
                        </div>
                      </div>

                      {/* Upgrade Potential */}
                      <div>
                        <h5 className="text-sm font-semibold text-primary-700 mb-2">Upgrade Potential</h5>
                        <div className="space-y-2">
                          <div>
                            <span className="text-xs font-medium text-primary-600">Easy Upgrades:</span>
                            <ul className="list-disc list-inside text-xs text-primary-700 mt-1">
                              {(product.ai_content?.maintenance_care?.upgrade_potential?.easy_upgrades || []).slice(0, 2).map((upgrade, index) => (
                                <li key={index}>{upgrade}</li>
                              ))}
                            </ul>
                          </div>
                          <div>
                            <span className="text-xs font-medium text-primary-600">Budget:</span>
                            <p className="text-xs text-primary-700 mt-1">{product.ai_content?.maintenance_care?.upgrade_potential?.recommended_budget || 'Budget recommendation not available.'}</p>
                          </div>
                        </div>
                      </div>

                      {/* Common Issues */}
                      <div>
                        <h5 className="text-sm font-semibold text-primary-700 mb-2">Common Issues</h5>
                        <div className="flex flex-wrap gap-1">
                          {(product.ai_content?.maintenance_care?.common_issues || []).slice(0, 2).map((issue, index) => (
                            <span key={index} className="px-2 py-1 bg-warning-100 text-warning-800 text-xs rounded-full">
                              {issue}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  ) : (
                    <p className="text-sm text-primary-500">No maintenance info available</p>
                  )}
                </div>
              ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Reviews Section - Always show */}
      <div className="bg-white rounded-xl shadow-elegant border border-primary-200 overflow-hidden mb-8">
        <button
          onClick={() => setShowReviews(!showReviews)}
          className="w-full p-6 flex items-center justify-between hover:bg-primary-50 transition-colors"
        >
          <h3 className="text-xl font-semibold text-primary-900 flex items-center gap-2">
            <span className="text-2xl">⭐</span>
            Customer Reviews
          </h3>
          <svg 
            className={`w-6 h-6 text-primary-600 transition-transform ${showReviews ? 'rotate-180' : ''}`} 
            fill="none" stroke="currentColor" viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        {showReviews && (
          <div className="px-6 pb-6">
            <div className={`grid gap-6 ${
              data.products.length === 1 
                ? 'grid-cols-1 max-w-2xl mx-auto' 
                : data.products.length === 2
                ? 'grid-cols-1 sm:grid-cols-2'
                : data.products.length === 3
                ? 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3'
                : 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'
            }`}>
            {data.products.map((product) => (
              <div key={product.id} className="border border-primary-200 rounded-lg p-4">
                <h4 className="font-semibold text-primary-900 mb-4">{product.name}</h4>
                <div className="space-y-3">
                  {product.avg_rating > 0 ? (
                    <>
                      <div className="flex items-center gap-2">
                        <span className="text-warning-500">★</span>
                        <span className="font-medium">{formatRating(product.avg_rating)}</span>
                        <span className="text-sm text-primary-500">({product.review_count} reviews)</span>
                      </div>
                      <div className="text-sm text-primary-600">
                        {product.avg_rating >= 4.5 && "Excellent customer satisfaction"}
                        {product.avg_rating >= 4.0 && product.avg_rating < 4.5 && "Very good customer satisfaction"}
                        {product.avg_rating >= 3.5 && product.avg_rating < 4.0 && "Good customer satisfaction"}
                        {product.avg_rating < 3.5 && "Mixed customer reviews"}
                      </div>
                    </>
                  ) : (
                    <div className="text-sm text-primary-600">
                      <p>No customer reviews available yet.</p>
                      <p className="text-xs text-primary-500 mt-1">Be the first to review this product!</p>
                    </div>
                  )}
                  <Link 
                    href={`/products/${product.slug}`}
                    className="text-sm text-primary-600 hover:text-primary-800 font-medium"
                  >
                    {product.avg_rating > 0 ? 'Read all reviews →' : 'View product details →'}
                  </Link>
                </div>
              </div>
            ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
