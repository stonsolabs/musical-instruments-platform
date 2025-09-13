import { GetServerSideProps } from 'next';
import Head from 'next/head';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { Product, ProductComparison, AffiliateStoreWithUrl } from '../src/types';
import { fetchProductComparison, fetchProduct, fetchProductAffiliateStores } from '../src/lib/api';
import CompareSearch from '../src/components/CompareSearch';
import ComparisonTable from '../src/components/ComparisonTable';
import { ComparisonButtons } from '../src/components/AffiliateButtons';
import ProductContentSections from '../src/components/ProductContentSections';
import ComparisonGrid from '../src/components/ComparisonGrid';
import ProductVoting from '../src/components/ProductVoting';
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
  const [isMobile, setIsMobile] = useState(false);

  // Track mobile state
  useEffect(() => {
    const checkMobile = () => setIsMobile(window.innerWidth < 640);
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  // Handle URL query parameters for pre-loaded comparison
  useEffect(() => {
    const { products } = router.query;

    if (router.isReady && products && typeof products === 'string') {
      const tokens = products
        .split(',')
        .map((t) => decodeURIComponent(t.trim()))
        .filter(Boolean);

      const allNumeric = tokens.length > 0 && tokens.every((t) => /^\d+$/.test(t));

      if (allNumeric) {
        const numericIds = tokens.map((t) => parseInt(t, 10));
        const currentIds = comparison?.products.map((p) => p.id) || [];
        const sameIds =
          numericIds.length === currentIds.length &&
          numericIds.every((id) => currentIds.includes(id));
        if (!sameIds) {
          loadComparison(numericIds);
        }
        return;
      }

      // Compare slugs with current comparison to avoid refetch loops
      const currentSlugs = (comparison?.products || []).map((p) => p.slug);
      const sameSlugs =
        tokens.length === currentSlugs.length &&
        tokens.every((s) => currentSlugs.includes(s));

      if (sameSlugs) {
        // Already showing the requested comparison, nothing to do
        return;
      }

      // Resolve slugs to IDs then load
      (async () => {
        try {
          console.log('Resolving product slugs:', tokens);
          const ids: number[] = [];
          for (const tok of tokens) {
            try {
              const prod = await fetchProduct(tok);
              if (prod?.id) ids.push(prod.id);
            } catch (e) {
              console.warn('Failed to resolve product slug:', tok, e);
            }
          }
          if (ids.length >= 2) {
            await loadComparison(ids);
          } else if (ids.length === 1) {
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
    } else if (router.isReady && !products && comparison) {
      // Clear comparison if no products in URL
      setComparison(null);
    }
  }, [router.query, router.isReady, comparison]);

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
      
      // Update URL with slugs instead of IDs
      const productSlugs = comparisonData.products.map(p => p.slug).join(',');
      const newQuery = { products: productSlugs };
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

    // Limit to 2 products on mobile, 4 on desktop
    const maxProducts = isMobile ? 2 : 4;
    
    // If we're at the limit, replace the oldest product
    if (currentIds.length >= maxProducts) {
      const newIds = [...currentIds.slice(1), productId]; // Remove oldest, add new
      console.log(`At ${maxProducts} product limit, replacing oldest. New IDs:`, newIds);
      await loadComparison(newIds);
    } else {
      // Add to existing comparison
      const newIds = [...currentIds, productId];
      console.log('Loading comparison with new IDs:', newIds);
      await loadComparison(newIds);
    }
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

      <div className="min-h-screen bg-gray-50 overflow-x-hidden">
        <div className="w-full max-w-none sm:max-w-7xl sm:mx-auto px-0 sm:px-4 lg:px-8 py-4 sm:py-8">
          {/* Enhanced Page Header */}
          <div className="text-center mb-12">
            <div className="relative">
              <h1 className="text-3xl sm:text-5xl font-bold text-gray-900 mb-6">
                Compare Instruments
              </h1>
              <div className="absolute -top-2 left-1/2 transform -translate-x-1/2 text-6xl opacity-10">
                🎵
              </div>
            </div>
            <p className="text-lg sm:text-xl text-gray-600 mb-6 sm:mb-8 px-2 sm:px-4 sm:max-w-4xl sm:mx-auto text-center">
              Make informed decisions with our comprehensive side-by-side instrument comparisons
            </p>
            
            {/* Simplified description */}
            <div className="px-2 sm:px-4 sm:max-w-2xl sm:mx-auto text-center">
              <p className="text-sm sm:text-base text-gray-600 mb-6">Compare specifications, features, prices, and community ratings to make informed decisions on your next musical investment.</p>
            </div>
          </div>

          {/* Compact Search Section */}
          <div className="mb-8">
            <div className="bg-white rounded-lg shadow-sm border p-4">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-lg font-semibold text-gray-900">Add Products to Compare</h3>
                {comparison && comparison.products.length > 0 && (
                  <div className="flex items-center space-x-2">
                    <span className="text-sm text-gray-600">
                      {comparison.products.length}/{isMobile ? 2 : 4}
                    </span>
                    <button
                      onClick={clearComparison}
                      className="text-sm text-gray-500 hover:text-red-600 transition-colors"
                    >
                      Clear all
                    </button>
                  </div>
                )}
              </div>
              <CompareSearch onProductSelect={addProductToComparison} />
            </div>
          </div>

          {/* Comparison Controls */}
          {comparison && (
            <div className="mb-8">
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div className="flex items-center space-x-4">
                  <h2 className="text-xl sm:text-2xl font-bold text-gray-900">
                    Comparing {comparison.products.length} Products
                  </h2>
                  <span className="badge badge-primary">
                    {comparison.common_specs.length} common specs
                  </span>
                </div>
                
                <div className="flex items-center space-x-4">
                  {/* In-page Goto Buttons */}
                  <div className="flex flex-wrap gap-2 bg-white rounded-lg p-1 shadow-sm border border-gray-200">
                    {[
                      { id: 'overview', label: 'Overview' },
                      { id: 'differences', label: 'Differences' },
                      { id: 'specifications', label: 'Specifications' },
                      { id: 'analysis', label: 'Analysis' },
                      { id: 'reviews', label: 'Reviews' },
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
            <div className="space-y-12">
              {/* Show message for single product */}
              {comparison.products.length === 1 && (
                <div className="bg-blue-50 border border-blue-200 rounded-xl p-6 text-center">
                  <div className="text-4xl mb-4">🔍</div>
                  <h3 className="text-xl font-bold text-blue-900 mb-2">Add More Products to Compare</h3>
                  <p className="text-blue-700">You have 1 product selected. Add more products above to start comparing specifications and features!</p>
                </div>
              )}
              
              {/* 1. PRODUCT OVERVIEW - Side by Side */}
              <div id="overview" className="card p-4 sm:p-8">
                <div className="text-center mb-8">
                  <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-4">🏆 Product Overview</h2>
                  <p className="text-sm sm:text-base text-gray-600 px-2 sm:px-4 sm:max-w-3xl sm:mx-auto text-center">
                    Compare basic information and key details for each instrument
                  </p>
                </div>
                
                <div className={`grid gap-2 sm:gap-4 ${comparison.products.length === 2 ? 'grid-cols-2' : comparison.products.length === 3 ? 'grid-cols-2 lg:grid-cols-3' : comparison.products.length === 4 ? 'grid-cols-2 lg:grid-cols-4' : 'grid-cols-1 max-w-md mx-auto'}`}>
                  {comparison.products.map((product, index) => {
                    const englishContent = product.ai_content?.localized_content?.['en-US'] || product.ai_content?.localized_content?.['en-GB'] || product.content?.localized_content?.['en-US'] || product.content?.localized_content?.['en-GB'];
                    
                    return (
                      <div key={product.id} className="bg-white border border-gray-200 rounded-lg p-3 sm:p-6">
                        {/* Product Header with Remove Button */}
                        <div className="relative mb-6">
                          <button
                            onClick={() => removeProductFromComparison(product.id)}
                            className="absolute -top-2 -right-2 w-6 h-6 bg-red-500 hover:bg-red-600 rounded-full flex items-center justify-center text-white transition-colors z-10"
                            title="Remove from comparison"
                          >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                            </svg>
                          </button>
                          <div className="absolute -top-2 -left-2">
                            <span className="inline-flex items-center justify-center w-6 h-6 bg-purple-600 text-white rounded-full text-sm font-bold">
                              {index + 1}
                            </span>
                          </div>
                          
                          {/* Product Image */}
                          <div className="w-32 h-32 bg-gray-100 rounded-xl overflow-hidden mx-auto mb-4">
                            <img
                              src={getProductImageUrl(product)}
                              alt={product.name}
                              className="w-full h-full object-cover"
                              loading="lazy"
                              onError={(e)=>{(e.target as HTMLImageElement).style.display='none'}}
                            />
                          </div>
                          
                          {/* Product Info */}
                          <div className="text-center">
                            <h3 className="font-bold text-gray-900 text-sm sm:text-lg mb-1 leading-tight">
                              <Link href={`/products/${product.slug}`} className="hover:text-brand-primary">
                                {product.name}
                              </Link>
                            </h3>
                            <p className="text-xs sm:text-sm text-gray-600 mb-3">{product.brand.name} • {product.category.name}</p>
                          </div>
                        </div>

                        {/* Basic Overview */}
                        {englishContent?.basic_info && (
                          <div className="mb-4 p-4 bg-blue-50 rounded-lg">
                            <h4 className="font-semibold text-blue-900 mb-2 text-sm">📝 Overview</h4>
                            <p className="text-xs text-blue-800 leading-relaxed">{englishContent.basic_info}</p>
                          </div>
                        )}

                        {/* Professional Score */}
                        <div className="mb-4 p-4 bg-purple-50 rounded-lg">
                          <div className="text-center mb-3">
                            <div className="text-2xl font-bold text-purple-700 mb-1">
                              {product.content?.professional_ratings?.overall_score || '8.5'}
                            </div>
                            <div className="text-xs text-purple-600 font-medium">Professional Score</div>
                          </div>
                          
                          <div className="grid grid-cols-2 gap-2 mb-3">
                            {[
                              { label: 'Sound', value: product.content?.professional_ratings?.sound || 85, icon: '🎵' },
                              { label: 'Build', value: product.content?.professional_ratings?.build || 90, icon: '🔧' },
                              { label: 'Play', value: product.content?.professional_ratings?.playability || 88, icon: '🎯' },
                              { label: 'Value', value: product.content?.professional_ratings?.value || 80, icon: '💰' }
                            ].map((rating) => (
                              <div key={rating.label} className="text-center">
                                <div className="text-sm mb-1">{rating.icon}</div>
                                <div className="text-xs font-bold text-gray-900">{rating.value}</div>
                                <div className="text-xs text-gray-600">{rating.label}</div>
                              </div>
                            ))}
                          </div>
                          
                          {/* Professional Notes - Close to Score */}
                          {product.content?.professional_ratings?.notes && (
                            <div className="text-xs text-purple-800 bg-purple-100 rounded-lg p-2 mt-3 border border-purple-200">
                              <p className="italic">"{product.content.professional_ratings.notes}"</p>
                            </div>
                          )}
                        </div>

                        {/* Community Votes */}
                        <div className="mb-4 p-4 bg-green-50 rounded-lg">
                          <h4 className="font-semibold text-green-900 mb-2 text-sm text-center">👥 Community</h4>
                          {product.vote_stats ? (
                            <div className="space-y-3">
                              <div className="flex items-center justify-center space-x-4">
                                <div className="text-center">
                                  <div className="flex items-center justify-center space-x-1">
                                    <span className="text-sm">🤘</span>
                                    <span className="text-sm font-bold text-green-600">{product.vote_stats.thumbs_up_count}</span>
                                  </div>
                                  <div className="text-xs text-gray-500">Up</div>
                                </div>
                                <div className="text-center">
                                  <div className="flex items-center justify-center space-x-1">
                                    <span className="text-sm">👎</span>
                                    <span className="text-sm font-bold text-red-600">{product.vote_stats.thumbs_down_count}</span>
                                  </div>
                                  <div className="text-xs text-gray-500">Down</div>
                                </div>
                              </div>
                              
                              {/* Compact Interactive Voting */}
                              <div className="scale-75">
                                <ProductVoting 
                                  productId={product.id}
                                  initialUpvotes={product.vote_stats.thumbs_up_count}
                                  initialDownvotes={product.vote_stats.thumbs_down_count}
                                />
                              </div>
                            </div>
                          ) : (
                            <div className="space-y-3">
                              <div className="text-center text-xs text-gray-500">No votes yet</div>
                              
                              {/* Compact Interactive Voting */}
                              <div className="scale-75">
                                <ProductVoting 
                                  productId={product.id}
                                  initialUpvotes={0}
                                  initialDownvotes={0}
                                />
                              </div>
                            </div>
                          )}
                        </div>

                        {/* Recognition Badges */}
                        {product.content?.quick_badges && (
                          <div className="mb-4 p-4 bg-orange-50 rounded-lg">
                            <h4 className="font-semibold text-orange-900 mb-2 text-sm">🏆 Recognition</h4>
                            <div className="grid grid-cols-2 gap-1">
                              {product.content.quick_badges.value_pick && (
                                <span className="inline-flex items-center justify-center px-2 py-1 rounded text-xs font-medium bg-yellow-100 text-yellow-700 border border-yellow-200 text-center">
                                  🏆 Best Value
                                </span>
                              )}
                              {product.content.quick_badges.pro_choice && (
                                <span className="inline-flex items-center justify-center px-2 py-1 rounded text-xs font-medium bg-purple-100 text-purple-700 border border-purple-200 text-center">
                                  🎯 Pro Choice
                                </span>
                              )}
                              {product.content.quick_badges.gig_ready && (
                                <span className="inline-flex items-center justify-center px-2 py-1 rounded text-xs font-medium bg-green-100 text-green-700 border border-green-200 text-center">
                                  🚀 Gig Ready
                                </span>
                              )}
                              {product.content.quick_badges.studio_ready && (
                                <span className="inline-flex items-center justify-center px-2 py-1 rounded text-xs font-medium bg-blue-100 text-blue-700 border border-blue-200 text-center">
                                  ⭐ Studio Ready
                                </span>
                              )}
                              {product.content.quick_badges.beginner_friendly && (
                                <span className="inline-flex items-center justify-center px-2 py-1 rounded text-xs font-medium bg-orange-100 text-orange-700 border border-orange-200 text-center">
                                  👶 Beginner Friendly
                                </span>
                              )}
                            </div>
                          </div>
                        )}

                        {/* Key Features */}
                        {product.content?.comparison_helpers?.standout_strengths && (
                          <div className="mb-4 p-4 bg-yellow-50 rounded-lg">
                            <h4 className="font-semibold text-yellow-900 mb-2 text-sm">⭐ Key Features</h4>
                            <ul className="space-y-1">
                              {product.content.comparison_helpers.standout_strengths.slice(0, 6).map((strength, idx) => (
                                <li key={idx} className="flex items-start space-x-1">
                                  <span className="text-yellow-600 mt-0.5 text-xs">•</span>
                                  <span className="text-xs text-yellow-800">{strength}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {/* Purchase Button */}
                        <div className="pt-4 border-t border-gray-100">
                          <ComparisonButtons product={product} preloadedStores={affiliateStoresByProduct[product.id] || []} />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>


              {/* 3. DETAILED SPECIFICATIONS TABLE */}
              <div id="specifications" className="card p-4 sm:p-8">
                <div className="text-center mb-8">
                  <h2 className="text-3xl font-bold text-gray-900 mb-4">📊 Detailed Specifications</h2>
                  <p className="text-gray-600 max-w-3xl mx-auto">
                    Comprehensive side-by-side comparison of all technical specifications and features
                  </p>
                </div>
                <ComparisonTable comparison={comparison} />
              </div>


              {/* 3. PROFESSIONAL ASSESSMENT - Side by Side */}
              {comparison.products.length > 0 && (
                <div id="analysis" className="card p-4 sm:p-8">
                  <div className="text-center mb-8">
                    <h2 className="text-3xl font-bold text-gray-900 mb-4">🎓 Professional Assessment</h2>
                    <p className="text-sm sm:text-base text-gray-600 px-2 sm:px-4 sm:max-w-3xl sm:mx-auto text-center">
                      Expert analysis and professional insights for each instrument
                    </p>
                  </div>
                  
                  <div className={`grid gap-2 sm:gap-4 ${comparison.products.length === 2 ? 'grid-cols-2' : comparison.products.length === 3 ? 'grid-cols-2 lg:grid-cols-3' : comparison.products.length === 4 ? 'grid-cols-2 lg:grid-cols-4' : 'grid-cols-1 max-w-md mx-auto'}`}>
                    {comparison.products.map((product, index) => {
                      const englishContent = product.ai_content?.localized_content?.['en-US'] || product.ai_content?.localized_content?.['en-GB'] || product.content?.localized_content?.['en-US'] || product.content?.localized_content?.['en-GB'];
                      
                      return (
                        <div key={product.id} className="bg-white border border-gray-200 rounded-lg p-3 sm:p-6">
                          {/* Product Header */}
                          <div className="text-center mb-6 pb-4 border-b border-gray-100">
                            <div className="w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold mx-auto mb-2">
                              {index + 1}
                            </div>
                            <h3 className="font-bold text-sm sm:text-lg text-gray-900">
                              <Link href={`/products/${product.slug}`} className="hover:text-brand-primary">
                                {product.name}
                              </Link>
                            </h3>
                            <p className="text-sm text-gray-600">{product.brand.name}</p>
                          </div>
                          
                          {/* Professional Assessment */}
                          {englishContent?.professional_assessment && (
                            <div className="mb-4 p-4 bg-blue-50 rounded-lg">
                              <h4 className="font-semibold text-blue-900 mb-2 text-sm">🎓 Expert Assessment</h4>
                              <p className="text-xs text-blue-800 leading-relaxed">{englishContent.professional_assessment}</p>
                            </div>
                          )}

                          {/* Technical Analysis */}
                          {englishContent?.technical_analysis && (
                            <div className="mb-4 p-4 bg-gray-50 rounded-lg">
                              <h4 className="font-semibold text-gray-900 mb-2 text-sm">🔬 Technical Analysis</h4>
                              <p className="text-xs text-gray-700 leading-relaxed">{englishContent.technical_analysis}</p>
                            </div>
                          )}

                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* 4. USAGE GUIDANCE - Side by Side */}
              {comparison.products.length > 0 && (
                <div id="usage-guidance" className="card p-4 sm:p-8">
                  <div className="text-center mb-8">
                    <h2 className="text-3xl font-bold text-gray-900 mb-4">🎯 Usage Guidance</h2>
                    <p className="text-sm sm:text-base text-gray-600 px-2 sm:px-4 sm:max-w-3xl sm:mx-auto text-center">
                      How to best use each instrument and what to expect
                    </p>
                  </div>
                  
                  <div className={`grid gap-2 sm:gap-4 ${comparison.products.length === 2 ? 'grid-cols-2' : comparison.products.length === 3 ? 'grid-cols-2 lg:grid-cols-3' : comparison.products.length === 4 ? 'grid-cols-2 lg:grid-cols-4' : 'grid-cols-1 max-w-md mx-auto'}`}>
                    {comparison.products.map((product, index) => {
                      const englishContent = product.ai_content?.localized_content?.['en-US'] || product.ai_content?.localized_content?.['en-GB'] || product.content?.localized_content?.['en-US'] || product.content?.localized_content?.['en-GB'];
                      
                      return (
                        <div key={product.id} className="bg-white border border-gray-200 rounded-lg p-3 sm:p-6">
                          {/* Product Header */}
                          <div className="text-center mb-6 pb-4 border-b border-gray-100">
                            <div className="w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold mx-auto mb-2">
                              {index + 1}
                            </div>
                            <h3 className="font-bold text-sm sm:text-lg text-gray-900">
                              <Link href={`/products/${product.slug}`} className="hover:text-brand-primary">
                                {product.name}
                              </Link>
                            </h3>
                            <p className="text-sm text-gray-600">{product.brand.name}</p>
                          </div>
                          
                          {/* Usage Guidance */}
                          {englishContent?.usage_guidance && (
                            <div className="mb-4 p-4 bg-green-50 rounded-lg">
                              <h4 className="font-semibold text-green-900 mb-2 text-sm">🎯 How to Use</h4>
                              <p className="text-xs text-green-800 leading-relaxed">{englishContent.usage_guidance}</p>
                            </div>
                          )}

                          {/* Setup Tips */}
                          {product.content?.setup_tips && product.content.setup_tips.length > 0 && (
                            <div className="mb-4 p-4 bg-blue-50 rounded-lg">
                              <h4 className="font-semibold text-blue-900 mb-2 text-sm">🔧 Setup Tips</h4>
                              <ul className="space-y-1">
                                {product.content.setup_tips.slice(0, 4).map((tip, idx) => (
                                  <li key={idx} className="flex items-start space-x-2">
                                    <span className="text-blue-600 mt-0.5 text-xs">•</span>
                                    <span className="text-xs text-blue-800">{tip}</span>
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}

                          {/* Full Audience Fit Section */}
                          {product.content?.audience_fit && (
                            <div className="space-y-3">
                              {/* Skill Levels */}
                              <div className="p-4 bg-gray-50 rounded-lg">
                                <h4 className="font-semibold text-gray-900 mb-3 text-sm flex items-center">
                                  <span className="mr-2">👥</span>
                                  Skill Levels
                                </h4>
                                <div className="space-y-2">
                                  <div className={`flex items-center justify-between p-2 rounded text-xs ${product.content.audience_fit?.beginners ? 'bg-green-100 border border-green-200' : 'bg-gray-100'}`}>
                                    <span className="font-medium">Beginners</span>
                                    <span>{product.content.audience_fit?.beginners ? '✅' : '❌'}</span>
                                  </div>
                                  <div className={`flex items-center justify-between p-2 rounded text-xs ${product.content.audience_fit?.intermediate ? 'bg-green-100 border border-green-200' : 'bg-gray-100'}`}>
                                    <span className="font-medium">Intermediate</span>
                                    <span>{product.content.audience_fit?.intermediate ? '✅' : '❌'}</span>
                                  </div>
                                  <div className={`flex items-center justify-between p-2 rounded text-xs ${product.content.audience_fit?.professionals ? 'bg-green-100 border border-green-200' : 'bg-gray-100'}`}>
                                    <span className="font-medium">Professionals</span>
                                    <span>{product.content.audience_fit?.professionals ? '✅' : '❌'}</span>
                                  </div>
                                </div>
                              </div>

                              {/* Learning Curve */}
                              {product.content.audience_fit?.learning_curve && (
                                <div className="p-4 bg-gray-50 rounded-lg">
                                  <h4 className="font-semibold text-gray-900 mb-2 text-sm flex items-center">
                                    <span className="mr-2">📈</span>
                                    Learning Curve
                                  </h4>
                                  <div className="text-center">
                                    <span className={`inline-flex px-3 py-2 rounded text-xs font-semibold ${
                                      product.content.audience_fit.learning_curve === 'easy' || product.content.audience_fit.learning_curve === 'very easy' ? 'bg-green-100 text-green-800 border border-green-200' :
                                      product.content.audience_fit.learning_curve === 'moderate' ? 'bg-yellow-100 text-yellow-800 border border-yellow-200' :
                                      'bg-red-100 text-red-800 border border-red-200'
                                    }`}>
                                      {product.content.audience_fit.learning_curve.charAt(0).toUpperCase() + product.content.audience_fit.learning_curve.slice(1)}
                                    </span>
                                  </div>
                                </div>
                              )}

                              {/* Suitable Genres */}
                              {product.content.audience_fit?.suitable_genres && (
                                <div className="p-4 bg-blue-50 rounded-lg">
                                  <h4 className="font-semibold text-blue-900 mb-2 text-sm flex items-center">
                                    <span className="mr-2">🎵</span>
                                    Suitable Genres
                                  </h4>
                                  <div className="flex flex-wrap gap-1">
                                    {product.content.audience_fit.suitable_genres.slice(0, 6).map((genre, idx) => (
                                      <span key={idx} className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-blue-200 text-blue-800">
                                        {genre}
                                      </span>
                                    ))}
                                  </div>
                                </div>
                              )}

                              {/* Studio/Live Role */}
                              {product.content.audience_fit?.studio_live_role && (
                                <div className="p-4 bg-purple-50 rounded-lg">
                                  <h4 className="font-semibold text-purple-900 mb-2 text-sm flex items-center">
                                    <span className="mr-2">🎯</span>
                                    Best Use Case
                                  </h4>
                                  <div className="text-center">
                                    <span className={`inline-flex items-center px-3 py-2 rounded text-xs font-semibold ${
                                      product.content.audience_fit.studio_live_role === 'versatile' ? 'bg-purple-100 text-purple-800 border border-purple-200' :
                                      product.content.audience_fit.studio_live_role === 'best in studio' ? 'bg-blue-100 text-blue-800 border border-blue-200' :
                                      'bg-green-100 text-green-800 border border-green-200'
                                    }`}>
                                      {product.content.audience_fit.studio_live_role.charAt(0).toUpperCase() + product.content.audience_fit.studio_live_role.slice(1)}
                                    </span>
                                  </div>
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* 5. CATEGORY-SPECIFIC METRICS - Side by Side */}
              {comparison.products.length > 0 && (
                <div id="category-metrics" className="card p-4 sm:p-8">
                  <div className="text-center mb-8">
                    <h2 className="text-3xl font-bold text-gray-900 mb-4">📊 Category-Specific Metrics</h2>
                    <p className="text-sm sm:text-base text-gray-600 px-2 sm:px-4 sm:max-w-3xl sm:mx-auto text-center">
                      Specialized performance measurements and ratings for each instrument type
                    </p>
                  </div>
                  
                  <div className={`grid gap-2 sm:gap-4 ${comparison.products.length === 2 ? 'grid-cols-2' : comparison.products.length === 3 ? 'grid-cols-2 lg:grid-cols-3' : comparison.products.length === 4 ? 'grid-cols-2 lg:grid-cols-4' : 'grid-cols-1 max-w-md mx-auto'}`}>
                    {comparison.products.map((product, index) => (
                      <div key={product.id} className="bg-white border border-gray-200 rounded-lg p-3 sm:p-6">
                        {/* Product Header */}
                        <div className="text-center mb-6 pb-4 border-b border-gray-100">
                          <div className="w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold mx-auto mb-2">
                            {index + 1}
                          </div>
                          <h3 className="font-bold text-sm sm:text-lg text-gray-900">
                            <Link href={`/products/${product.slug}`} className="hover:text-brand-primary">
                              {product.name}
                            </Link>
                          </h3>
                          <p className="text-sm text-gray-600">{product.brand.name}</p>
                        </div>
                        
                        {/* Category-Specific Metrics */}
                        {product.content?.category_specific?.metrics ? (
                          <div className="grid grid-cols-1 gap-3">
                            {Object.entries(product.content.category_specific.metrics).map(([metric, value]) => {
                              // Handle case where value might be an object
                              const displayValue = typeof value === 'object' ? JSON.stringify(value) : String(value);
                              const numericValue = typeof value === 'number' ? value : 
                                                   typeof value === 'string' && !isNaN(Number(value)) ? Number(value) : 0;
                              
                              return (
                                <div key={metric} className="text-center bg-gray-50 rounded-lg p-3">
                                  <div className="text-lg font-bold text-purple-700 mb-1">{displayValue}</div>
                                  <div className="text-xs text-gray-600 capitalize">{metric.replace(/_/g, ' ')}</div>
                                  <div className="w-full bg-gray-200 rounded-full h-1.5 mt-2">
                                    <div 
                                      className="bg-gradient-to-r from-purple-400 to-purple-600 h-1.5 rounded-full" 
                                      style={{ width: `${Math.min(numericValue, 100)}%` }}
                                    />
                                  </div>
                                </div>
                              );
                            })}
                          </div>
                        ) : (
                          <div className="text-center py-8">
                            <div className="text-4xl mb-4 opacity-20">📊</div>
                            <h4 className="text-sm font-medium text-gray-900 mb-2">No Category Metrics</h4>
                            <p className="text-xs text-gray-500">Category-specific metrics for this product are being prepared.</p>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 6. CUSTOMER FEEDBACK - Side by Side */}
              {comparison.products.length > 0 && (
                <div id="reviews" className="card p-4 sm:p-8">
                  <div className="text-center mb-8">
                    <h2 className="text-3xl font-bold text-gray-900 mb-4">⭐ Customer Feedback</h2>
                    <p className="text-sm sm:text-base text-gray-600 px-2 sm:px-4 sm:max-w-3xl sm:mx-auto text-center">
                      What customers and users are saying about each instrument
                    </p>
                  </div>
                  
                  <div className={`grid gap-2 sm:gap-4 ${comparison.products.length === 2 ? 'grid-cols-2' : comparison.products.length === 3 ? 'grid-cols-2 lg:grid-cols-3' : comparison.products.length === 4 ? 'grid-cols-2 lg:grid-cols-4' : 'grid-cols-1 max-w-md mx-auto'}`}>
                    {comparison.products.map((product, index) => {
                      const englishContent = product.ai_content?.localized_content?.['en-US'] || product.ai_content?.localized_content?.['en-GB'] || product.content?.localized_content?.['en-US'] || product.content?.localized_content?.['en-GB'];
                      
                      return (
                        <div key={product.id} className="bg-white border border-gray-200 rounded-lg p-3 sm:p-6">
                          {/* Product Header with Community Votes */}
                          <div className="text-center mb-6 pb-4 border-b border-gray-100">
                            <div className="w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold mx-auto mb-2">
                              {index + 1}
                            </div>
                          <h3 className="font-bold text-sm sm:text-lg text-gray-900 mb-2">
                            <Link href={`/products/${product.slug}`} className="hover:text-brand-primary">
                              {product.name}
                            </Link>
                          </h3>
                            
                            {/* Community Votes & Interactive Voting */}
                            {product.vote_stats ? (
                              <div className="space-y-3 mb-4">
                                <div className="flex items-center justify-center space-x-4">
                                  <div className="text-center">
                                    <div className="flex items-center justify-center space-x-1">
                                      <span className="text-sm">🤘</span>
                                      <span className="text-sm font-bold text-green-600">{product.vote_stats.thumbs_up_count}</span>
                                    </div>
                                    <div className="text-xs text-gray-500">Likes</div>
                                  </div>
                                  <div className="text-center">
                                    <div className="flex items-center justify-center space-x-1">
                                      <span className="text-sm">👎</span>
                                      <span className="text-sm font-bold text-red-600">{product.vote_stats.thumbs_down_count}</span>
                                    </div>
                                    <div className="text-xs text-gray-500">Dislikes</div>
                                  </div>
                                </div>
                                
                                {/* Compact Interactive Voting */}
                                <div className="scale-75">
                                  <ProductVoting 
                                    productId={product.id}
                                    initialUpvotes={product.vote_stats.thumbs_up_count}
                                    initialDownvotes={product.vote_stats.thumbs_down_count}
                                  />
                                </div>
                              </div>
                            ) : (
                              <div className="space-y-3 mb-4">
                                <div className="text-xs text-gray-500">No community votes yet</div>
                                
                                {/* Compact Interactive Voting */}
                                <div className="scale-75">
                                  <ProductVoting 
                                    productId={product.id}
                                    initialUpvotes={0}
                                    initialDownvotes={0}
                                  />
                                </div>
                              </div>
                            )}
                            <p className="text-sm text-gray-600">{product.brand.name}</p>
                          </div>
                          
                          {/* Customer Reviews */}
                          {englishContent?.customer_reviews && (
                            <div className="mb-4 p-4 bg-orange-50 rounded-lg">
                              <h4 className="font-semibold text-orange-900 mb-2 text-sm">⭐ User Reviews</h4>
                              <p className="text-xs text-orange-800 leading-relaxed">{englishContent.customer_reviews}</p>
                            </div>
                          )}

                          {/* Maintenance & Care */}
                          {englishContent?.maintenance_care && (
                            <div className="mb-4 p-4 bg-green-50 rounded-lg">
                              <h4 className="font-semibold text-green-900 mb-2 text-sm">🔧 Care & Maintenance</h4>
                              <p className="text-xs text-green-800 leading-relaxed">{englishContent.maintenance_care}</p>
                            </div>
                          )}

                          {/* Purchase Decision */}
                          {englishContent?.purchase_decision && (
                            <div className="mb-4 p-4 bg-purple-50 rounded-lg">
                              <h4 className="font-semibold text-purple-900 mb-2 text-sm">💡 Purchase Guide</h4>
                              <p className="text-xs text-purple-800 leading-relaxed">{englishContent.purchase_decision}</p>
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* 6. COMPARISON HELPERS - Side by Side */}
              {comparison.products.length > 0 && (
                <div id="differences" className="card p-4 sm:p-8">
                  <div className="text-center mb-8">
                    <h2 className="text-3xl font-bold text-gray-900 mb-4">⚖️ Comparison Guide</h2>
                    <p className="text-sm sm:text-base text-gray-600 px-2 sm:px-4 sm:max-w-3xl sm:mx-auto text-center">
                      Detailed comparison insights to help you make the right choice
                    </p>
                  </div>
                  
                  <div className={`grid gap-2 sm:gap-4 ${comparison.products.length === 2 ? 'grid-cols-2' : comparison.products.length === 3 ? 'grid-cols-2 lg:grid-cols-3' : comparison.products.length === 4 ? 'grid-cols-2 lg:grid-cols-4' : 'grid-cols-1 max-w-md mx-auto'}`}>
                    {comparison.products.map((product, index) => (
                      <div key={product.id} className="bg-white border border-gray-200 rounded-lg p-3 sm:p-6">
                        {/* Product Header */}
                        <div className="text-center mb-6 pb-4 border-b border-gray-100">
                          <div className="w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold mx-auto mb-2">
                            {index + 1}
                          </div>
                          <h3 className="font-bold text-sm sm:text-lg text-gray-900">
                            <Link href={`/products/${product.slug}`} className="hover:text-brand-primary">
                              {product.name}
                            </Link>
                          </h3>
                          <p className="text-sm text-gray-600">{product.brand.name}</p>
                        </div>
                        
                        {/* Best For */}
                        {product.content?.comparison_helpers?.best_for && (
                          <div className="mb-4 p-4 bg-green-50 rounded-lg">
                            <h4 className="font-semibold text-green-900 mb-2 text-sm">✅ Best For</h4>
                            <ul className="space-y-1">
                              {product.content.comparison_helpers.best_for.map((item, idx) => (
                                <li key={idx} className="flex items-start space-x-2">
                                  <span className="text-green-600 mt-0.5 text-xs">✓</span>
                                  <span className="text-xs text-green-800">{item}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {/* Not Ideal For */}
                        {product.content?.comparison_helpers?.not_ideal_for && (
                          <div className="mb-4 p-4 bg-red-50 rounded-lg">
                            <h4 className="font-semibold text-red-900 mb-2 text-sm">❌ Not Ideal For</h4>
                            <ul className="space-y-1">
                              {product.content.comparison_helpers.not_ideal_for.map((item, idx) => (
                                <li key={idx} className="flex items-start space-x-2">
                                  <span className="text-red-600 mt-0.5 text-xs">✗</span>
                                  <span className="text-xs text-red-800">{item}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {/* Key Tradeoffs */}
                        {product.content?.comparison_helpers?.key_tradeoffs && (
                          <div className="mb-4 p-4 bg-yellow-50 rounded-lg">
                            <h4 className="font-semibold text-yellow-900 mb-2 text-sm">⚠️ Key Tradeoffs</h4>
                            <ul className="space-y-1">
                              {product.content.comparison_helpers.key_tradeoffs.map((tradeoff, idx) => (
                                <li key={idx} className="flex items-start space-x-2">
                                  <span className="text-yellow-600 mt-0.5 text-xs">⚠</span>
                                  <span className="text-xs text-yellow-800">{tradeoff}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* 7. ACCESSORY RECOMMENDATIONS - Side by Side */}
          {comparison && comparison.products.length > 0 && (
            <div id="accessories" className="card p-4 sm:p-8">
              <div className="text-center mb-8">
                <h2 className="text-3xl font-bold text-gray-900 mb-4">🎯 Recommended Accessories</h2>
                <p className="text-sm sm:text-base text-gray-600 px-2 sm:px-4 sm:max-w-3xl sm:mx-auto text-center">
                  Essential accessories to get the most out of each instrument
                </p>
              </div>
              
              <div className={`grid gap-2 sm:gap-8 ${comparison.products.length === 2 ? 'grid-cols-2' : comparison.products.length === 3 ? 'grid-cols-2 lg:grid-cols-3' : comparison.products.length === 4 ? 'grid-cols-2 lg:grid-cols-4' : 'grid-cols-1 max-w-md mx-auto'}`}>
                {comparison.products.map((product, index) => (
                  <div key={product.id} className="bg-white border border-gray-200 rounded-lg p-3 sm:p-6">
                    {/* Product Header */}
                    <div className="text-center mb-6 pb-4 border-b border-gray-100">
                      <div className="w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold mx-auto mb-2">
                        {index + 1}
                      </div>
                      <h3 className="font-bold text-sm sm:text-lg text-gray-900">
                        <Link href={`/products/${product.slug}`} className="hover:text-brand-primary">
                          {product.name}
                        </Link>
                      </h3>
                      <p className="text-sm text-gray-600">{product.brand.name}</p>
                    </div>
                    
                    {/* Accessory Recommendations */}
                    {product.content?.accessory_recommendations && product.content.accessory_recommendations.length > 0 ? (
                      <div className="space-y-3">
                        {product.content.accessory_recommendations.slice(0, 4).map((accessory, idx) => (
                          <div key={idx} className="border border-gray-200 rounded-lg p-4">
                            <h4 className="font-semibold text-gray-900 mb-2 text-sm">{accessory.name}</h4>
                            <p className="text-xs text-gray-600">{accessory.why}</p>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="text-center py-8">
                        <div className="text-4xl mb-4 opacity-20">🎯</div>
                        <h4 className="text-sm font-medium text-gray-900 mb-2">No Accessories Listed</h4>
                        <p className="text-xs text-gray-500">Accessory recommendations for this product are being prepared.</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Warranty & Protection section removed by request */}

          {/* QUESTIONS & ANSWERS - Side by Side (at the end) */}
          {comparison && comparison.products.length > 0 && (
            <div id="qa" className="card p-4 sm:p-8">
              <div className="text-center mb-8">
                <h2 className="text-3xl font-bold text-gray-900 mb-4">❓ Questions & Answers</h2>
                <p className="text-gray-600 max-w-3xl mx-auto">
                  Common questions and detailed answers about each instrument
                </p>
              </div>
              
              <div className={`grid gap-2 sm:gap-8 ${comparison.products.length === 2 ? 'grid-cols-2' : comparison.products.length === 3 ? 'grid-cols-2 lg:grid-cols-3' : comparison.products.length === 4 ? 'grid-cols-2 lg:grid-cols-4' : 'grid-cols-1 max-w-md mx-auto'}`}>
                {comparison.products.map((product, index) => {
                  const qaData = (product as any).qa || product.content?.qa || product.content?.content_metadata?.qa || product.ai_content?.qa;
                  
                  return (
                    <div key={product.id} className="bg-white border border-gray-200 rounded-lg p-3 sm:p-6">
                      {/* Product Header */}
                      <div className="text-center mb-6 pb-4 border-b border-gray-100">
                        <div className="w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold mx-auto mb-2">
                          {index + 1}
                        </div>
                        <h3 className="font-bold text-sm sm:text-lg text-gray-900">
                          <Link href={`/products/${product.slug}`} className="hover:text-brand-primary">
                            {product.name}
                          </Link>
                        </h3>
                        <p className="text-sm text-gray-600">{product.brand.name}</p>
                      </div>
                      
                      {/* Q&A Section */}
                      {qaData && Array.isArray(qaData) && qaData.length > 0 ? (
                        <div className="space-y-4">
                          {qaData.slice(0, 4).map((item: any, idx: number) => (
                            <div key={idx} className="border-b border-gray-100 pb-4 last:border-b-0">
                              <div className="font-semibold text-gray-900 mb-2 text-sm">
                                Q: {item.question}
                              </div>
                              <div className="text-gray-700 text-xs leading-relaxed">
                                A: {item.answer}
                              </div>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <div className="text-center py-8">
                          <div className="text-4xl mb-4 opacity-20">❓</div>
                          <h4 className="text-sm font-medium text-gray-900 mb-2">No Q&A Available</h4>
                          <p className="text-xs text-gray-500">Questions and answers for this product are being prepared.</p>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
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
              <p className="text-sm sm:text-lg text-gray-600 mb-8 px-2 sm:px-4 sm:max-w-2xl sm:mx-auto text-center">
                Use the search above to find instruments and build your comparison. 
                Compare specifications, features, prices, and community ratings.
              </p>
              
              {/* Quick Action Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-6 px-2 sm:px-4 sm:max-w-4xl sm:mx-auto mb-8">
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
