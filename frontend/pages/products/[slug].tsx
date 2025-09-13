import { GetServerSideProps } from 'next';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { Product } from '../../src/types';
import { fetchProduct } from '../../src/lib/api';
import ProductGallery from '../../src/components/ProductGallery';
import ProductInfo from '../../src/components/ProductInfo';
import ProductSpecifications from '../../src/components/ProductSpecifications';
import ProductContentSections from '../../src/components/ProductContentSections';
import ComprehensiveProductContent from '../../src/components/ComprehensiveProductContent';
import { ProductDetailButtons } from '../../src/components/AffiliateButtons';
import { fetchProductAffiliateStores } from '../../src/lib/api';
import RelatedProducts from '../../src/components/RelatedProducts';
import ProductReviews from '../../src/components/ProductReviews';
import ProductVoting from '../../src/components/ProductVoting';
import { StarIcon } from '@heroicons/react/20/solid';

interface ProductDetailPageProps {
  product: Product;
  affiliateStores?: any[];
}

export default function ProductDetailPage({ product, affiliateStores = [] }: ProductDetailPageProps) {
  const router = useRouter();
  const origin = typeof window !== 'undefined' ? window.location.origin : (process.env.NEXT_PUBLIC_APP_ORIGIN || 'https://www.getyourmusicgear.com');
  const canonicalUrl = `${origin}/products/${product.slug}`;

  if (router.isFallback) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-primary mx-auto mb-4"></div>
          <p className="text-gray-600">Loading product...</p>
        </div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Product Not Found</h1>
          <p className="text-gray-600 mb-6">The product you're looking for doesn't exist.</p>
          <button
            onClick={() => router.back()}
            className="btn-primary"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }

  return (
    <>
      <Head>
        <title>{product.name} - {product.brand.name} | GetYourMusicGear</title>
        <meta name="description" content={product.description || `Compare prices and read reviews for ${product.name} by ${product.brand.name}. Find the best deals on ${product.category.name}.`} />
        <link rel="canonical" href={canonicalUrl} />
        <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
        <meta property="og:title" content={`${product.name} - ${product.brand.name}`} />
        <meta property="og:description" content={product.description || `Compare prices and read reviews for ${product.name}`} />
        <meta property="og:url" content={canonicalUrl} />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content={`${product.name} - ${product.brand.name}`} />
        <meta name="twitter:description" content={product.description || `Compare prices and read reviews for ${product.name}`} />
        <meta property="og:type" content="product" />
        <meta property="og:url" content={`https://getyourmusicgear.com/products/${product.slug}`} />
        {product.images && product.images.length > 0 && (
          <meta property="og:image" content={product.images[0] || ''} />
        )}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              '@context': 'https://schema.org',
              '@type': 'Product',
              name: product.name,
              brand: { '@type': 'Brand', name: product.brand.name },
              category: product.category?.name,
              image: product.images && product.images.length > 0 ? product.images[0] : undefined,
              description: product.description || undefined,
              sku: product.sku || undefined,
              aggregateRating: product.review_count ? {
                '@type': 'AggregateRating',
                ratingValue: product.avg_rating || 0,
                reviewCount: product.review_count,
              } : undefined,
              offers: (affiliateStores && affiliateStores.length > 0) ? {
                '@type': 'AggregateOffer',
                priceCurrency: (affiliateStores[0].currency || 'USD'),
                lowPrice: Math.min(...affiliateStores.map((s: any) => s.price || 0).filter((p: number) => p > 0)) || undefined,
                highPrice: Math.max(...affiliateStores.map((s: any) => s.price || 0).filter((p: number) => p > 0)) || undefined,
                offerCount: affiliateStores.length,
                url: canonicalUrl,
                availability: 'http://schema.org/InStock',
              } : undefined,
            }),
          }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              '@context': 'https://schema.org',
              '@type': 'BreadcrumbList',
              itemListElement: [
                { '@type': 'ListItem', position: 1, name: 'Home', item: `${origin}` },
                { '@type': 'ListItem', position: 2, name: product.category.name, item: `${origin}/products?category=${product.category.slug}` },
                { '@type': 'ListItem', position: 3, name: product.brand.name, item: `${origin}/products?brand=${product.brand.slug}` },
                { '@type': 'ListItem', position: 4, name: product.name, item: canonicalUrl },
              ],
            }),
          }}
        />
      </Head>

      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Breadcrumbs */}
          <nav className="flex mb-8" aria-label="Breadcrumb">
            <ol className="flex items-center space-x-2 text-sm text-gray-500">
              <li>
                <a href="/" className="hover:text-brand-primary transition-colors">
                  Home
                </a>
              </li>
              <li>
                <span className="mx-2">/</span>
              </li>
              <li>
                <a href={`/products?category=${product.category.slug}`} className="hover:text-brand-primary transition-colors">
                  {product.category.name}
                </a>
              </li>
              <li>
                <span className="mx-2">/</span>
              </li>
              <li>
                <a href={`/products?brand=${product.brand.slug}`} className="hover:text-brand-primary transition-colors">
                  {product.brand.name}
                </a>
              </li>
              <li>
                <span className="mx-2">/</span>
              </li>
              <li className="text-gray-900 font-medium">
                {product.name}
              </li>
            </ol>
          </nav>

          {/* 1. OVERVIEW SECTION */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mb-12">
            {/* Left: Gallery + Basic Info */}
            <div className="lg:col-span-8">
              <div className="card p-6 mb-6">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">{product.name}</h1>
                <div className="flex items-center space-x-4 mb-4">
                  <span className="text-lg font-medium text-brand-blue">{product.brand.name}</span>
                  <span className="text-sm text-gray-500">•</span>
                  <span className="text-sm text-gray-600">{product.category.name}</span>
                </div>

                {/* Key Features */}
                {product.content?.comparison_helpers?.standout_strengths && (
                  <div className="mb-6 p-4 bg-blue-50 rounded-lg">
                    <h3 className="text-sm font-semibold text-blue-900 mb-3">✨ Key Features</h3>
                    <div className="space-y-2">
                      {product.content.comparison_helpers.standout_strengths.slice(0, 6).map((strength, idx) => (
                        <div key={idx} className="flex items-start space-x-2">
                          <span className="text-blue-500 mt-0.5">•</span>
                          <span className="text-sm text-blue-800">{strength}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Smaller Image Gallery */}
                <div className="w-full max-w-md mx-auto">
                  <ProductGallery product={product} />
                </div>

                {/* Purchase Section - moved below image */}
                <div className="card p-6 mt-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">🛒 Get This Instrument</h3>
                  <ProductDetailButtons product={product} preloadedStores={affiliateStores as any} />
                </div>
              </div>
            </div>

            {/* Right: Performance Metrics & Community */}
            <div className="lg:col-span-4">
              <div className="sticky top-8 space-y-6">
                {/* Professional Rating */}
                <div className="card p-6">
                  <div className="text-center mb-6">
                    <h3 className="text-xl font-bold text-gray-900 mb-2">🏆 Professional Score</h3>
                    <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-purple-500 to-purple-600 text-white rounded-full text-2xl font-bold mb-4">
                      {product.content?.professional_ratings?.overall_score || '8.5'}
                    </div>
                    <p className="text-sm text-gray-600">Expert Analysis & Testing</p>
                  </div>
                  
                  {/* Professional Ratings Grid */}
                  <div className="grid grid-cols-2 gap-4 mb-6">
                    {[
                      { label: 'Sound', value: product.content?.professional_ratings?.sound || 85, icon: '🎵' },
                      { label: 'Build', value: product.content?.professional_ratings?.build || 90, icon: '🔧' },
                      { label: 'Play', value: product.content?.professional_ratings?.playability || 88, icon: '🎯' },
                      { label: 'Value', value: product.content?.professional_ratings?.value || 80, icon: '💰' }
                    ].map((rating) => (
                      <div key={rating.label} className="text-center">
                        <div className="text-2xl mb-1">{rating.icon}</div>
                        <div className="text-lg font-bold text-gray-900">{rating.value}</div>
                        <div className="text-xs text-gray-600">{rating.label}</div>
                        <div className="w-full bg-gray-200 rounded-full h-1.5 mt-1">
                          <div className="bg-gradient-to-r from-purple-400 to-purple-600 h-1.5 rounded-full" style={{ width: `${rating.value}%` }}></div>
                        </div>
                      </div>
                    ))}
                  </div>
                  
                  {product.content?.professional_ratings?.notes && (
                    <div className="text-sm text-gray-700 bg-gray-50 rounded-lg p-3">
                      <p className="italic">"{product.content.professional_ratings.notes}"</p>
                    </div>
                  )}
                </div>

                {/* Community Votes & Voting */}
                <div className="card p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">👥 Community Votes</h3>
                  {product.vote_stats ? (
                    <div className="space-y-4">
                      <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                        <span className="text-sm text-gray-600">Community Opinion</span>
                        <div className="flex items-center space-x-3">
                          <div className="flex items-center space-x-1">
                            <span className="text-lg">🤘</span>
                            <span className="text-lg font-bold text-green-600">{product.vote_stats.thumbs_up_count}</span>
                          </div>
                          <div className="flex items-center space-x-1">
                            <span className="text-lg">👎</span>
                            <span className="text-lg font-bold text-red-600">{product.vote_stats.thumbs_down_count}</span>
                          </div>
                        </div>
                      </div>
                      
                      {/* Interactive Voting */}
                      <ProductVoting 
                        productId={product.id}
                        initialUpvotes={product.vote_stats.thumbs_up_count}
                        initialDownvotes={product.vote_stats.thumbs_down_count}
                      />
                    </div>
                  ) : (
                    <div className="space-y-4">
                      <div className="text-center py-6 text-gray-500">
                        <p className="text-sm">No community votes yet</p>
                      </div>
                      
                      {/* Interactive Voting */}
                      <ProductVoting 
                        productId={product.id}
                        initialUpvotes={0}
                        initialDownvotes={0}
                      />
                    </div>
                  )}
                </div>

                {/* Recognition Badges - Only show if from content */}
                {product.content?.quick_badges && (
                  <div className="card p-6">
                    <h3 className="text-lg font-bold text-gray-900 mb-4">🏆 Recognition</h3>
                    <div className="grid grid-cols-2 gap-2">
                      {product.content.quick_badges.value_pick && (
                        <span className="inline-flex items-center justify-center px-3 py-2 rounded-lg text-xs font-medium bg-yellow-50 text-yellow-700 border border-yellow-200 text-center">
                          🏆<br />Best Value
                        </span>
                      )}
                      {product.content.quick_badges.pro_choice && (
                        <span className="inline-flex items-center justify-center px-3 py-2 rounded-lg text-xs font-medium bg-purple-50 text-purple-700 border border-purple-200 text-center">
                          🎯<br />Pro Choice
                        </span>
                      )}
                      {product.content.quick_badges.gig_ready && (
                        <span className="inline-flex items-center justify-center px-3 py-2 rounded-lg text-xs font-medium bg-green-50 text-green-700 border border-green-200 text-center">
                          🚀<br />Gig Ready
                        </span>
                      )}
                      {product.content.quick_badges.studio_ready && (
                        <span className="inline-flex items-center justify-center px-3 py-2 rounded-lg text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200 text-center">
                          ⭐<br />Studio Ready
                        </span>
                      )}
                      {product.content.quick_badges.beginner_friendly && (
                        <span className="inline-flex items-center justify-center px-3 py-2 rounded-lg text-xs font-medium bg-orange-50 text-orange-700 border border-orange-200 text-center">
                          👶<br />Beginner Friendly
                        </span>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>


          {/* 2. SPECIFICATIONS SECTION */}
          <div className="mb-12">
            <div className="card p-8">
              <div className="text-center mb-8">
                <h2 className="text-3xl font-bold text-gray-900 mb-4">📊 Technical Specifications</h2>
                <p className="text-gray-600 max-w-2xl mx-auto">
                  Detailed technical specifications, professional analysis, and expert insights
                </p>
              </div>
              
              {/* Specifications Grid */}
              {product.content?.specifications && Object.keys(product.content.specifications).length > 0 ? (
                <ProductSpecifications specifications={product.content.specifications} />
              ) : (
                <div className="text-center py-8">
                  <p className="text-gray-500">Detailed specifications are being updated. Check back soon!</p>
                </div>
              )}
            </div>
          </div>

          {/* Professional Analysis & Content */}
          {product.content && (
            <div className="mb-12">
              <div className="card p-8">
                <div className="text-center mb-8">
                  <h2 className="text-3xl font-bold text-gray-900 mb-4">🎓 Professional Analysis</h2>
                  <p className="text-gray-600 max-w-2xl mx-auto">
                    Expert insights, usage guidance, and comprehensive product analysis
                  </p>
                </div>
                <ComprehensiveProductContent product={product} />
              </div>
            </div>
          )}


          {/* Audience Fit & Usage */}
          {product.content?.audience_fit && (
            <div className="mb-12">
              <div className="card p-8">
                <div className="text-center mb-8">
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">🎯 Who Is This For?</h2>
                  <p className="text-gray-600">Find out if this instrument matches your skill level and musical goals</p>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  {/* Left Column */}
                  <div className="space-y-6">
                    {/* Skill Levels */}
                    <div className="bg-gray-50 rounded-lg p-6">
                      <h4 className="font-semibold text-gray-900 mb-4 flex items-center">
                        <span className="mr-2">👥</span>
                        Skill Levels
                      </h4>
                      <div className="space-y-3">
                        <div className={`flex items-center justify-between p-3 rounded-lg ${product.content.audience_fit?.beginners ? 'bg-green-100 border border-green-200' : 'bg-gray-100'}`}>
                          <span className="text-sm font-medium">Beginners</span>
                          <span className="text-lg">{product.content.audience_fit?.beginners ? '✅' : '❌'}</span>
                        </div>
                        <div className={`flex items-center justify-between p-3 rounded-lg ${product.content.audience_fit?.intermediate ? 'bg-green-100 border border-green-200' : 'bg-gray-100'}`}>
                          <span className="text-sm font-medium">Intermediate</span>
                          <span className="text-lg">{product.content.audience_fit?.intermediate ? '✅' : '❌'}</span>
                        </div>
                        <div className={`flex items-center justify-between p-3 rounded-lg ${product.content.audience_fit?.professionals ? 'bg-green-100 border border-green-200' : 'bg-gray-100'}`}>
                          <span className="text-sm font-medium">Professionals</span>
                          <span className="text-lg">{product.content.audience_fit?.professionals ? '✅' : '❌'}</span>
                        </div>
                      </div>
                    </div>

                    {/* Learning Curve */}
                    <div className="bg-gray-50 rounded-lg p-6">
                      <h4 className="font-semibold text-gray-900 mb-4 flex items-center">
                        <span className="mr-2">📈</span>
                        Learning Curve
                      </h4>
                      <div className="text-center">
                        <div className={`inline-flex px-6 py-3 rounded-lg font-semibold ${
                          product.content.audience_fit?.learning_curve === 'easy' || product.content.audience_fit?.learning_curve === 'very easy' ? 'bg-green-100 text-green-800 border border-green-200' :
                          product.content.audience_fit?.learning_curve === 'moderate' ? 'bg-yellow-100 text-yellow-800 border border-yellow-200' :
                          'bg-red-100 text-red-800 border border-red-200'
                        }`}>
                          {product.content.audience_fit?.learning_curve ? 
                            product.content.audience_fit.learning_curve.charAt(0).toUpperCase() + product.content.audience_fit.learning_curve.slice(1) : 
                            'Not specified'}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Right Column */}
                  <div className="space-y-6">
                    {/* Suitable Genres */}
                    {product.content.audience_fit?.suitable_genres && (
                      <div className="bg-gray-50 rounded-lg p-6">
                        <h4 className="font-semibold text-gray-900 mb-4 flex items-center">
                          <span className="mr-2">🎵</span>
                          Suitable Genres
                        </h4>
                        <div className="flex flex-wrap gap-2">
                          {product.content.audience_fit.suitable_genres.map((genre, index) => (
                            <span key={index} className="inline-flex items-center px-3 py-2 rounded-full text-sm font-medium bg-blue-100 text-blue-800 border border-blue-200">
                              {genre}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Studio/Live Role */}
                    {product.content.audience_fit?.studio_live_role && (
                      <div className="bg-gray-50 rounded-lg p-6">
                        <h4 className="font-semibold text-gray-900 mb-4 flex items-center">
                          <span className="mr-2">🎯</span>
                          Best Use Case
                        </h4>
                        <div className="text-center">
                          <span className={`inline-flex items-center px-6 py-3 rounded-lg text-sm font-semibold ${
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
                </div>
              </div>
            </div>
          )}


          {/* Accessory Recommendations */}
          {product.content?.accessory_recommendations && product.content.accessory_recommendations.length > 0 && (
            <div className="mb-12">
              <div className="card p-8">
                <div className="text-center mb-8">
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">🎯 Recommended Accessories</h2>
                  <p className="text-gray-600">Essential accessories to get the most out of your instrument</p>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {product.content.accessory_recommendations.map((accessory, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-6">
                      <h3 className="font-semibold text-gray-900 mb-3">{accessory.name}</h3>
                      <p className="text-sm text-gray-600">{accessory.why}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Category-Specific Metrics */}
          {product.content?.category_specific?.metrics && (
            <div className="mb-12">
              <div className="card p-8">
                <div className="text-center mb-8">
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">📊 Performance Metrics</h2>
                  <p className="text-gray-600">Category-specific performance measurements and ratings</p>
                </div>
                
                <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
                  {Object.entries(product.content.category_specific.metrics).map(([metric, value]) => (
                    <div key={metric} className="text-center bg-gray-50 rounded-lg p-4">
                      <div className="text-2xl font-bold text-purple-700 mb-1">{value}</div>
                      <div className="text-sm text-gray-600 capitalize">{metric.replace(/_/g, ' ')}</div>
                      <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                        <div 
                          className="bg-gradient-to-r from-purple-400 to-purple-600 h-2 rounded-full" 
                          style={{ width: `${Math.min(value, 100)}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* 3. ADDITIONAL INFORMATION SECTION */}
          <div className="space-y-12 mb-12">
            {/* Community Reviews */}
            {product.review_count > 0 && (
              <div className="card p-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                  <span className="mr-3">📝</span>
                  Community Reviews
                </h2>
                <ProductReviews product={product} />
              </div>
            )}
            
            {/* Related Products - Full Width */}
            <div className="card p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-8 flex items-center">
                <span className="mr-3">🔗</span>
                Related Products
              </h2>
              <RelatedProducts 
                categorySlug={product.category.slug}
                brandSlug={product.brand.slug}
                currentProductId={product.id}
              />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export const getServerSideProps: GetServerSideProps = async ({ params }) => {
  try {
    const slug = params?.slug as string;
    
    if (!slug) {
      return {
        notFound: true,
      };
    }

    const product = await fetchProduct(slug);

    if (!product) {
      return {
        notFound: true,
      };
    }

    // Preload affiliate stores to avoid extra client calls and rate limits
    let affiliateStores: any[] = [];
    try {
      const resp = await fetchProductAffiliateStores(product.id);
      affiliateStores = resp.affiliate_stores || [];
    } catch {}

    return {
      props: {
        product,
        affiliateStores,
      },
    };
  } catch (error) {
    console.error('Error fetching product:', error);
    
    return {
      notFound: true,
    };
  }
};
