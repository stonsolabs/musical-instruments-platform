import { GetServerSideProps } from 'next';
import Head from 'next/head';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { Product, ProductComparison, AffiliateStoreWithUrl } from '../src/types';
import { fetchProductComparison, fetchProduct, fetchProductAffiliateStores } from '../src/lib/api';
import CompareSearch from '../src/components/CompareSearch';
import ComparisonTable from '../src/components/ComparisonTable';
import { ComparisonButtons } from '../src/components/AffiliateButtons';
import ProductContentSections from '../src/components/ProductContentSections';
import ComparisonGrid from '../src/components/ComparisonGrid';
import { StarIcon } from '@heroicons/react/20/solid';
import { getProductImageUrl } from '../src/lib/utils';

interface ComparePageProps {
  initialComparison?: ProductComparison;
  affiliateStoresByProduct?: Record<number, AffiliateStoreWithUrl[]>;
}

export default function ComparePage({ initialComparison, affiliateStoresByProduct = {} }: ComparePageProps) {
  const router = useRouter();
  const [comparison, setComparison] = useState<ProductComparison | null>(initialComparison || null);
  const [loading, setLoading] = useState(false);
  // Render all sections; use in-page anchors for navigation

  // Handle URL query parameters for pre-loaded comparison
  useEffect(() => {
    const { products } = router.query;
    
    // Only process if we have products query and no current comparison or comparison is different
    if (products && typeof products === 'string' && router.isReady) {
      const tokens = products.split(',');
      const numericIds = tokens.map(t => parseInt(t)).filter(id => !isNaN(id));
      
      // Check if this is different from current comparison
      const currentIds = comparison?.products.map(p => p.id) || [];
      const isDifferent = numericIds.length !== currentIds.length || 
                         numericIds.some(id => !currentIds.includes(id));
      
      if (isDifferent) {
        if (numericIds.length > 0 && numericIds.length === tokens.length) {
          loadComparison(numericIds);
        } else {
          // Resolve slugs to ids
          (async () => {
            try {
              console.log('Resolving product slugs:', tokens);
              const ids: number[] = [];
              for (const tok of tokens) {
                try {
                  const prod = await fetchProduct(tok);
                  console.log('Resolved slug', tok, 'to product:', prod);
                  if (prod?.id) ids.push(prod.id);
                } catch (e) {
                  console.warn('Failed to resolve product slug:', tok, e);
                }
              }
              console.log('Resolved IDs:', ids);
              if (ids.length >= 2) {
                loadComparison(ids);
              } else if (ids.length === 1) {
                // Show single product, user can add more
                try {
                  const product = await fetchProduct(ids[0]);
                  setComparison({
                    products: [product],
                    common_specs: [],
                    spec_differences: []
                  } as any);
                } catch (error) {
                  console.error('Failed to load single product:', error);
                }
              } else {
                console.warn('No valid products found from slugs:', tokens);
              }
            } catch (error) {
              console.error('Error resolving slugs:', error);
            }
          })();
        }
      }
    } else if (!products && comparison && router.isReady) {
      // Clear comparison if no products in URL
      setComparison(null);
    }
  }, [router.query, router.isReady]);

  const loadComparison = async (productIds: number[]) => {
    if (productIds.length < 2) {
      console.warn('Need at least 2 products for comparison');
      return;
    }
    
    setLoading(true);
    try {
      console.log('Loading comparison for products:', productIds);
      const comparisonData = await fetchProductComparison(productIds);
      console.log('Comparison data loaded:', comparisonData);
      setComparison(comparisonData);
      
      // Update URL without reloading
      const newQuery = { products: productIds.join(',') };
      router.push({ pathname: router.pathname, query: newQuery }, undefined, { shallow: true });
    } catch (error) {
      console.error('Error loading comparison:', error);
      // Don't clear comparison on error, keep previous state
    } finally {
      setLoading(false);
    }
  };

  const addProductToComparison = async (productId: number) => {
    console.log('Adding product to comparison:', productId);
    
    if (!comparison) {
      // For single product, we need to get a second product or show message
      console.log('No existing comparison, creating new one');
      setComparison({
        products: [],
        common_specs: [],
        spec_differences: []
      } as any);
      
      // Load the single product and add it
      try {
        const product = await fetchProduct(productId);
        setComparison({
          products: [product],
          common_specs: [],
          spec_differences: []
        } as any);
      } catch (error) {
        console.error('Failed to load single product:', error);
      }
      return;
    }

    const currentIds = comparison.products.map(p => p.id);
    if (currentIds.includes(productId)) {
      console.log('Product already in comparison');
      return;
    }

    const newIds = [...currentIds, productId];
    if (newIds.length > 4) {
      newIds.shift(); // Remove oldest product if more than 4
    }

    console.log('Loading comparison with new IDs:', newIds);
    await loadComparison(newIds);
  };

  const removeProductFromComparison = async (productId: number) => {
    if (!comparison) return;

    const newIds = comparison.products.map(p => p.id).filter(id => id !== productId);
    if (newIds.length < 2) {
      setComparison(null);
      router.push('/compare', undefined, { shallow: true });
    } else {
      await loadComparison(newIds);
    }
  };

  const clearComparison = () => {
    setComparison(null);
    router.push('/compare', undefined, { shallow: true });
  };

  return (
    <>
      <Head>
        <title>Compare Musical Instruments - GetYourMusicGear</title>
        <meta name="description" content="Compare musical instruments side by side. View specifications, prices, and reviews to make informed decisions on your next musical investment." />
      </Head>

      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Enhanced Page Header */}
          <div className="text-center mb-12">
            <div className="relative">
              <h1 className="text-5xl font-bold text-gray-900 mb-6">
                Compare Instruments
              </h1>
              <div className="absolute -top-2 left-1/2 transform -translate-x-1/2 text-6xl opacity-10">
                🎵
              </div>
            </div>
            <p className="text-xl text-gray-600 max-w-4xl mx-auto mb-8">
              Make informed decisions with our comprehensive side-by-side instrument comparisons
            </p>
            
            {/* Enhanced Features Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto mb-8">
              <div className="bg-white rounded-lg p-6 shadow-sm border">
                <div className="text-3xl mb-3">📊</div>
                <h3 className="font-semibold text-gray-900 mb-2">Detailed Specs</h3>
                <p className="text-sm text-gray-600">Compare technical specifications, features, and build quality</p>
              </div>
              <div className="bg-white rounded-lg p-6 shadow-sm border">
                <div className="text-3xl mb-3">🔍</div>
                <h3 className="font-semibold text-gray-900 mb-2">Expert Analysis</h3>
                <p className="text-sm text-gray-600">Professional insights and detailed comparisons</p>
              </div>
              <div className="bg-white rounded-lg p-6 shadow-sm border">
                <div className="text-3xl mb-3">🛒</div>
                <h3 className="font-semibold text-gray-900 mb-2">Shop Smart</h3>
                <p className="text-sm text-gray-600">Find the best deals from trusted music retailers</p>
              </div>
            </div>
            
            {/* Status badges */}
            <div className="flex items-center justify-center gap-3 flex-wrap">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200">
                ⭐ Professional Rating: coming soon
              </span>
              <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-50 text-green-700 border border-green-200">
                📋 Detailed Specs & Analysis
              </span>
              <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-purple-50 text-purple-700 border border-purple-200">
                🔄 Up to 4 Products
              </span>
            </div>
          </div>

          {/* Enhanced Search Section */}
          <div className="mb-12">
            <div className="bg-white rounded-xl shadow-sm border p-8">
              <div className="text-center mb-6">
                <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                  Add Products to Compare
                </h2>
                <p className="text-gray-600">
                  Search for instruments and add up to 4 products for comparison
                </p>
              </div>
              <CompareSearch onProductSelect={addProductToComparison} />
              
              {comparison && comparison.products.length > 0 && (
                <div className="mt-6 pt-6 border-t">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <span className="text-sm font-medium text-gray-700">
                        Currently comparing {comparison.products.length} product{comparison.products.length !== 1 ? 's' : ''}
                      </span>
                      <div className="flex space-x-1">
                        {[...Array(4)].map((_, i) => (
                          <div
                            key={i}
                            className={`w-2 h-2 rounded-full ${
                              i < comparison.products.length ? 'bg-brand-primary' : 'bg-gray-300'
                            }`}
                          />
                        ))}
                      </div>
                    </div>
                    <button
                      onClick={clearComparison}
                      className="text-sm text-gray-500 hover:text-red-600 transition-colors"
                    >
                      Clear all
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Comparison Controls */}
          {comparison && (
            <div className="mb-8">
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div className="flex items-center space-x-4">
                  <h2 className="text-2xl font-bold text-gray-900">
                    Comparing {comparison.products.length} Products
                  </h2>
                  <span className="badge badge-primary">
                    {comparison.common_specs.length} common specs
                  </span>
                </div>
                
                <div className="flex items-center space-x-4">
                  {/* In-page Goto Buttons */}
                  <div className="flex bg-white rounded-lg p-1 shadow-sm border border-gray-200">
                    {[
                      { id: 'summary', label: 'Summary' },
                      { id: 'grid', label: 'Highlights' },
                      { id: 'specs', label: 'Specs Table' },
                      { id: 'analysis', label: 'Content & Analysis' },
                      { id: 'qa', label: 'Q&A' },
                    ].map(({ id, label }) => (
                      <button
                        key={id}
                        onClick={() => {
                          const el = document.getElementById(id);
                          if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        }}
                        className="btn-secondary px-3 py-2 text-sm"
                      >
                        {label}
                      </button>
                    ))}
                  </div>
                  
                  <button
                    onClick={clearComparison}
                    className="btn-secondary"
                  >
                    Clear All
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-blue mx-auto mb-4"></div>
              <p className="text-gray-600">Loading comparison...</p>
            </div>
          )}

          {/* Comparison Content */}
          {comparison && !loading && comparison.products.length > 0 && (
            <div className="space-y-8">
              {/* Show message for single product */}
              {comparison.products.length === 1 && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
                  <p className="text-blue-800 font-medium">You have 1 product selected. Add more products to start comparing!</p>
                </div>
              )}
              
              {/* Product Summary Cards with dynamic columns and right-side buttons */}
              <div id="summary"></div>
              {(() => {
                const count = comparison.products.length;
                const gridCols = count === 1 ? 'grid-cols-1' : count === 2 ? 'grid-cols-2' : count === 3 ? 'grid-cols-3' : 'grid-cols-4';
                return (
                  <div className={`grid ${gridCols} gap-4`}>
                    {comparison.products.map((product) => (
                      <div key={product.id} className="card p-4">
                        <div className="flex items-start justify-between mb-3">
                          <div className="flex-1">
                            <h3 className="font-semibold text-gray-900 text-sm line-clamp-2 mb-1">
                              {product.name}
                            </h3>
                            <p className="text-xs text-gray-500">{product.brand.name}</p>
                          </div>
                          <button
                            onClick={() => removeProductFromComparison(product.id)}
                            className="text-gray-400 hover:text-red-500 transition-colors ml-2"
                          >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                            </svg>
                          </button>
                        </div>

                        <div className="flex items-start gap-3 mb-3">
                          <div className="w-20 h-20 bg-gray-100 rounded overflow-hidden flex-shrink-0">
                            <img
                              src={getProductImageUrl(product)}
                              alt={product.name}
                              className="w-full h-full object-cover"
                              loading="lazy"
                              onError={(e)=>{(e.target as HTMLImageElement).style.display='none'}}
                            />
                          </div>
                          <div className="flex-1">
                            {/* Badges under title */}
                            <div className="flex items-center gap-2 mb-2 flex-wrap">
                              <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-medium bg-purple-50 text-purple-700 border border-purple-200">
                                Professional Rating
                              </span>
                              {product.content && (
                                <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
                                  Summary Available
                                </span>
                              )}
                            </div>
                            <div className="flex items-center space-x-2 mb-2">
                              <div className="flex items-center">
                                {[...Array(5)].map((_, i) => (
                                  <StarIcon
                                    key={i}
                                    className={`w-3 h-3 ${
                                      i < Math.floor(product.avg_rating || 0)
                                        ? 'text-yellow-400'
                                        : 'text-gray-300'
                                    }`}
                                  />
                                ))}
                              </div>
                              <span className="text-xs text-gray-500">({product.review_count})</span>
                            </div>
                            {/* Quick Facts */}
                            <ul className="text-xs text-gray-600 space-y-1">
                              <li><strong>Brand:</strong> {product.brand.name}</li>
                              <li><strong>Category:</strong> {product.category.name}</li>
                              {product.specifications && Object.entries(product.specifications).slice(0, 3).map(([key, value]) => (
                                <li key={`${product.id}-spec-${key}`}>
                                  <strong>{key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:</strong> {value || 'N/A'}
                                </li>
                              ))}
                              {(!product.specifications || Object.keys(product.specifications).length === 0) && (
                                <li><em>Detailed specifications loading...</em></li>
                              )}
                            </ul>
                          </div>
                          <div className="w-40 flex-shrink-0">
                            <ComparisonButtons product={product} preloadedStores={affiliateStoresByProduct[product.id] || []} />
                          </div>
                        </div>

                        {/* Collapsible details per product (narratives, QA) */}
                        {product.content && (
                          <ProductContentSections content={product.content as any} />
                        )}
                      </div>
                    ))}
                  </div>
                );
              })()}

              {/* Key Differences Summary */}
              {(() => {
                const products = comparison.products || [];
                const cm = (comparison as any).comparison_matrix || {};
                const specSet = new Set<string>(Object.keys(cm));
                for (const p of products) {
                  const sp = (p as any).content?.specifications || (p as any).specifications || {};
                  Object.keys(sp).forEach(k => specSet.add(k));
                }
                const allSpecs = Array.from(specSet);
                const diffs = allSpecs.filter(spec => {
                  const values = products.map((p:any) => (p.specifications?.[spec] ?? cm[spec]?.[String(p.id)] ?? p.content?.specifications?.[spec] ?? ''));
                  const norm = (v:any) => String(v ?? '').toLowerCase();
                  const first = norm(values[0]);
                  return values.some(v => norm(v) !== first);
                }).slice(0, 6);
                if (products.length < 2 || diffs.length === 0) return null;
                return (
                  <div id="diffs" className="bg-white rounded-xl shadow-sm border p-6">
                    <h3 className="text-xl font-semibold text-gray-900 mb-4">Key Differences</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {diffs.map((spec) => (
                        <div key={spec} className="bg-gray-50 border border-gray-200 rounded-lg p-3">
                          <div className="text-sm font-medium text-gray-900 capitalize mb-1">{spec.replace(/_/g,' ')}</div>
                          <div className="grid grid-cols-2 gap-2 text-xs text-gray-700">
                            {products.map((p:any) => {
                              const val = p.specifications?.[spec] ?? cm[spec]?.[String(p.id)] ?? p.content?.specifications?.[spec] ?? '—';
                              return (
                                <div key={`${p.id}-${spec}`} className="truncate"><span className="text-gray-500">{p.brand?.name}:</span> {String(val)}</div>
                              );
                            })}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                );
              })()}

              {/* Specs Table (always rendered) */}
              <div id="specs" className="bg-white rounded-xl shadow-sm border p-4">
                <ComparisonTable comparison={comparison} />
              </div>
              
              {/* Content & Analysis (always rendered) */}
              <div id="analysis" className="bg-white rounded-xl shadow-sm border p-8">
                <h3 className="text-2xl font-bold text-gray-900 mb-6">Content & Analysis</h3>
                <div className={`grid ${comparison.products.length === 2 ? 'grid-cols-2' : comparison.products.length === 3 ? 'grid-cols-3' : 'grid-cols-4'} gap-6`}>
                  {comparison.products.map((product) => (
                    <div key={product.id} className="space-y-4">
                      <h4 className="font-semibold text-lg text-gray-900 border-b pb-2">{product.name}</h4>
                      {product.content ? (
                        <ProductContentSections content={product.content as any} />
                      ) : (
                        <div className="text-sm text-gray-500">No content available</div>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* Professional Assessment & Reviews Section */}
              {comparison.products.length > 0 && (
                <div id="grid" className="bg-white rounded-xl shadow-sm border p-8">
                  <h3 className="text-2xl font-bold text-gray-900 mb-6">Professional Assessment</h3>
                  <div className={`grid ${comparison.products.length === 2 ? 'grid-cols-2' : comparison.products.length === 3 ? 'grid-cols-3' : 'grid-cols-4'} gap-6`}>
                    {comparison.products.map((product) => {
                      const englishContent = product.ai_content?.localized_content?.['en-US'] || product.ai_content?.localized_content?.['en-GB'];
                      
                      return (
                        <div key={product.id} className="space-y-4">
                          <h4 className="font-semibold text-lg text-gray-900 border-b pb-2">{product.name}</h4>
                          
                          {englishContent && (
                            <div className="space-y-4">
                              {englishContent.basic_info && (
                                <div>
                                  <h5 className="font-medium text-sm text-gray-800 mb-2">Overview</h5>
                                  <p className="text-sm text-gray-600">{englishContent.basic_info}</p>
                                </div>
                              )}
                              
                              {englishContent.professional_assessment && (
                                <div>
                                  <h5 className="font-medium text-sm text-gray-800 mb-2">Professional Assessment</h5>
                                  <p className="text-sm text-gray-600">{englishContent.professional_assessment}</p>
                                </div>
                              )}
                              
                              {englishContent.customer_reviews && (
                                <div>
                                  <h5 className="font-medium text-sm text-gray-800 mb-2">Customer Reviews</h5>
                                  <p className="text-sm text-gray-600">{englishContent.customer_reviews}</p>
                                </div>
                              )}

                              {englishContent.usage_guidance && (
                                <div>
                                  <h5 className="font-medium text-sm text-gray-800 mb-2">Usage Guidance</h5>
                                  <p className="text-sm text-gray-600">{englishContent.usage_guidance}</p>
                                </div>
                              )}
                            </div>
                          )}
                          
                          {!englishContent && (
                            <div className="text-center py-8 text-gray-500">
                              <p className="text-sm">Detailed analysis coming soon...</p>
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Enhanced Empty State */}
          {!comparison && !loading && (
            <div className="text-center py-16">
              <div className="relative">
                <div className="text-8xl mb-6 opacity-20">🎸</div>
                <div className="absolute top-0 left-1/2 transform -translate-x-1/2 translate-y-4 text-4xl">
                  🥁
                </div>
                <div className="absolute top-8 right-1/2 transform translate-x-16 text-3xl">
                  🎹
                </div>
              </div>
              
              <h3 className="text-3xl font-bold text-gray-900 mb-4">
                Start Your Comparison Journey
              </h3>
              <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
                Use the search above to find instruments and build your comparison. 
                Compare specifications, features, prices, and community ratings.
              </p>
              
              {/* Quick Action Cards */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto mb-8">
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer"
                     onClick={() => router.push('/products?category=guitars')}>
                  <div className="text-3xl mb-3">🎸</div>
                  <h4 className="font-semibold text-gray-900 mb-2">Compare Guitars</h4>
                  <p className="text-sm text-gray-600">Electric, acoustic, bass guitars and more</p>
                </div>
                
                <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer"
                     onClick={() => router.push('/products?category=pianos')}>
                  <div className="text-3xl mb-3">🎹</div>
                  <h4 className="font-semibold text-gray-900 mb-2">Compare Keyboards</h4>
                  <p className="text-sm text-gray-600">Digital pianos, synthesizers, MIDI controllers</p>
                </div>
                
                <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer"
                     onClick={() => router.push('/products?category=drums')}>
                  <div className="text-3xl mb-3">🥁</div>
                  <h4 className="font-semibold text-gray-900 mb-2">Compare Drums</h4>
                  <p className="text-sm text-gray-600">Acoustic kits, electronic drums, percussion</p>
                </div>
              </div>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button
                  onClick={() => router.push('/products')}
                  className="btn-primary px-8 py-3"
                >
                  🔍 Browse All Products
                </button>
                <button
                  onClick={() => router.push('/products?sort_by=rating&sort_order=desc')}
                  className="btn-secondary px-8 py-3"
                >
                  ⭐ View Top Rated
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
}

export const getServerSideProps: GetServerSideProps = async ({ query }) => {
  try {
    const { products } = query;
    
    if (products && typeof products === 'string') {
      const tokens = products.split(',');
      
      // First try to parse as numeric IDs
      const numericIds = tokens.map(id => parseInt(id)).filter(id => !isNaN(id));
      
      if (numericIds.length >= 2 && numericIds.length === tokens.length) {
        // All tokens are numeric IDs, use them directly
        const comparison = await fetchProductComparison(numericIds);
        const affiliateStoresByProduct: Record<number, AffiliateStoreWithUrl[]> = {};
        try {
          await Promise.all(
            (comparison.products || []).map(async (p) => {
              try {
                const resp = await fetchProductAffiliateStores(p.id);
                affiliateStoresByProduct[p.id] = resp.affiliate_stores || [];
              } catch {}
            })
          );
        } catch {}
        return {
          props: {
            initialComparison: comparison,
            affiliateStoresByProduct,
          },
        };
      } else if (tokens.length >= 2) {
        // Some/all tokens are slugs, resolve them server-side
        try {
          const resolvedIds: number[] = [];
          for (const token of tokens) {
            try {
              const product = await fetchProduct(token);
              if (product?.id) {
                resolvedIds.push(product.id);
              }
            } catch (e) {
              console.warn('Failed to resolve product slug server-side:', token, e);
            }
          }
          
          if (resolvedIds.length >= 2) {
            const comparison = await fetchProductComparison(resolvedIds);
            const affiliateStoresByProduct: Record<number, AffiliateStoreWithUrl[]> = {};
            try {
              await Promise.all(
                (comparison.products || []).map(async (p) => {
                  try {
                    const resp = await fetchProductAffiliateStores(p.id);
                    affiliateStoresByProduct[p.id] = resp.affiliate_stores || [];
                  } catch {}
                })
              );
            } catch {}
            return {
              props: {
                initialComparison: comparison,
                affiliateStoresByProduct,
              },
            };
          }
        } catch (error) {
          console.error('Error resolving product slugs:', error);
        }
      }
    }

    return {
      props: {
        initialComparison: null,
      },
    };
  } catch (error) {
    console.error('Error fetching comparison data:', error);
    
    return {
      props: {
        initialComparison: null,
      },
    };
  }
};
