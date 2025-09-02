import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import BlogProductShowcase from './BlogProductShowcase';
import ProductComparisonTable from './ProductComparisonTable';

interface Product {
  id: string;
  name: string;
  slug: string;
  brand: string;
  category: string;
  price: number;
  originalPrice?: number;
  image: string;
  rating: number;
  reviewCount: number;
  affiliateUrl: string;
  features: string[];
  description: string;
  pros?: string[];
  cons?: string[];
  bestFor?: string;
  isRecommended?: boolean;
  badge?: string;
}

interface BlogPost {
  title: string;
  excerpt: string;
  content: string;
  author: string;
  category: string;
  date: string;
  readTime: string;
  image: string;
  tags: string[];
  expertTested: boolean;
  rating?: number;
  tableOfContents?: { title: string; id: string }[];
  products: Product[];
  style?: 'buying-guide' | 'comparison' | 'review' | 'tutorial' | 'news' | 'buyers-guide' | 'step-by-step' | 'lists-rankings' | 'educational' | 'extended-comparison' | 'trends-news' | 'maintenance-accessories' | 'inspiration-culture' | string;
}

interface BlogPostLayoutProps {
  post: BlogPost;
  children?: React.ReactNode;
}

export default function BlogPostLayout({ post, children }: BlogPostLayoutProps) {
  const getLayoutStyle = () => {
    switch (post.style) {
      case 'buying-guide':
        return 'buying-guide-layout';
      case 'comparison':
        return 'comparison-layout';
      case 'review':
        return 'review-layout';
      case 'tutorial':
        return 'tutorial-layout';
      case 'news':
        return 'news-layout';
      case 'buyers-guide':
        return 'buyers-guide-layout';
      case 'step-by-step':
        return 'step-by-step-layout';
      case 'lists-rankings':
        return 'lists-rankings-layout';
      case 'educational':
        return 'educational-layout';
      case 'extended-comparison':
        return 'extended-comparison-layout';
      case 'trends-news':
        return 'trends-news-layout';
      case 'maintenance-accessories':
        return 'maintenance-accessories-layout';
      case 'inspiration-culture':
        return 'inspiration-culture-layout';
      default:
        return 'default-layout';
    }
  };

  const renderBuyingGuideLayout = () => (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-700 text-white py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="flex items-center justify-center gap-4 mb-6">
            <span className="text-xs font-semibold text-blue-200 uppercase tracking-wide">{post.category}</span>
            <span className="text-blue-200">•</span>
            <span className="text-blue-200">{post.date}</span>
            <span className="text-blue-200">•</span>
            <span className="text-blue-200">{post.readTime}</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">{post.title}</h1>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto leading-relaxed">{post.excerpt}</p>
          <div className="mt-8 flex items-center justify-center gap-4">
            <span className="text-blue-200">By {post.author}</span>
            {post.expertTested && (
              <span className="bg-green-600 text-white px-3 py-1 rounded-full text-sm font-bold flex items-center gap-1">
                <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Expert Tested
              </span>
            )}
          </div>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid lg:grid-cols-4 gap-12">
          {/* Main Content */}
          <div className="lg:col-span-3">
            <article className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
              {/* Featured Product Showcase */}
              <BlogProductShowcase
                products={post.products}
                style="recommended"
                title="Our Top Recommendations"
                subtitle="Hand-picked products that offer the best value and performance"
              />

              {/* Article Content */}
              <div 
                className="prose prose-lg max-w-none mt-12"
                dangerouslySetInnerHTML={{ __html: post.content }}
              />

              {/* Product Grid */}
              <BlogProductShowcase
                products={post.products}
                style="grid"
                title="All Recommended Products"
                maxProducts={6}
              />

              {/* Comparison Table */}
              {post.products.length > 1 && (
                <ProductComparisonTable
                  products={post.products.map(product => ({
                    ...product,
                    features: {
                      price: `€${product.price}`,
                      rating: product.rating,
                      reviews: product.reviewCount,
                      brand: product.brand,
                      category: product.category
                    },
                    pros: product.pros || product.features.slice(0, 3),
                    cons: product.cons || ['Check individual reviews for details'],
                    bestFor: product.bestFor || 'General use'
                  }))}
                  features={[
                    { key: 'price', label: 'Price', type: 'text' },
                    { key: 'rating', label: 'Rating', type: 'rating' },
                    { key: 'reviews', label: 'Reviews', type: 'number' },
                    { key: 'brand', label: 'Brand', type: 'text' }
                  ]}
                  title="Product Comparison"
                  description="Compare all recommended products side by side"
                />
              )}
            </article>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="sticky top-8 space-y-8">
              {/* Table of Contents */}
              {post.tableOfContents && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Table of Contents</h3>
                  <nav className="space-y-2">
                    {post.tableOfContents.map((item) => (
                      <a
                        key={item.id}
                        href={`#${item.id}`}
                        className="block text-sm text-gray-600 hover:text-blue-600 hover:font-medium transition-colors"
                      >
                        {item.title}
                      </a>
                    ))}
                  </nav>
                </div>
              )}

              {/* Quick Product Picks */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-4">Quick Picks</h3>
                <div className="space-y-4">
                  {post.products.slice(0, 3).map((product) => (
                    <div key={product.id} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                      <div className="relative h-12 w-12 bg-gray-100 rounded overflow-hidden">
                        <Image
                          src={product.image}
                          alt={product.name}
                          fill
                          className=""
                          style={{ objectFit: 'contain', backgroundColor: 'white' }}
                        />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h4 className="font-semibold text-gray-900 text-sm truncate">{product.name}</h4>
                        <p className="text-sm font-bold text-gray-900">€{product.price}</p>
                      </div>
                      <Link
                        href={product.affiliateUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="bg-blue-600 text-white px-3 py-1 rounded text-xs font-semibold hover:bg-blue-700 transition-colors"
                      >
                        View
                      </Link>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderComparisonLayout = () => (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-green-600 to-blue-700 text-white py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">{post.title}</h1>
          <p className="text-xl text-green-100 max-w-3xl mx-auto leading-relaxed">{post.excerpt}</p>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <article className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
          {/* Product Showcase */}
          <BlogProductShowcase
            products={post.products}
            style="featured"
            title="Products Compared"
            subtitle="Detailed comparison of the top products in this category"
          />

          {/* Article Content */}
          <div 
            className="prose prose-lg max-w-none mt-12"
            dangerouslySetInnerHTML={{ __html: post.content }}
          />

          {/* Detailed Comparison Table */}
          <ProductComparisonTable
            products={post.products.map(product => ({
              ...product,
              features: {
                price: `€${product.price}`,
                rating: product.rating,
                reviews: product.reviewCount,
                brand: product.brand,
                category: product.category,
                features: product.features.join(', ')
              },
              pros: product.pros || product.features.slice(0, 4),
              cons: product.cons || ['Check individual reviews for details'],
              bestFor: product.bestFor || 'General use'
            }))}
            features={[
              { key: 'price', label: 'Price', type: 'text' },
              { key: 'rating', label: 'Rating', type: 'rating' },
              { key: 'reviews', label: 'Reviews', type: 'number' },
              { key: 'brand', label: 'Brand', type: 'text' },
              { key: 'features', label: 'Key Features', type: 'text' }
            ]}
            title="Detailed Comparison"
            description="Compare all features and specifications"
          />
        </article>
      </div>
    </div>
  );

  const renderReviewLayout = () => (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-purple-600 to-pink-700 text-white py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">{post.title}</h1>
          <p className="text-xl text-purple-100 max-w-3xl mx-auto leading-relaxed">{post.excerpt}</p>
          {post.rating && (
            <div className="mt-6 flex items-center justify-center gap-2">
              <div className="flex items-center gap-1">
                {[...Array(5)].map((_, i) => (
                  <span key={i} className={`text-2xl ${i < Math.floor(post.rating!) ? 'text-yellow-400' : 'text-gray-300'}`}>
                    ★
                  </span>
                ))}
              </div>
              <span className="text-xl font-bold">{post.rating}/5</span>
            </div>
          )}
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid lg:grid-cols-3 gap-12">
          {/* Main Content */}
          <div className="lg:col-span-2">
            <article className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
              {/* Featured Product */}
              <BlogProductShowcase
                products={post.products}
                style="recommended"
                title="Product Review"
                subtitle="In-depth analysis and testing results"
              />

              {/* Article Content */}
              <div 
                className="prose prose-lg max-w-none mt-12"
                dangerouslySetInnerHTML={{ __html: post.content }}
              />
            </article>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="sticky top-8 space-y-8">
              {/* Rating Summary */}
              {post.rating && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Rating Summary</h3>
                  <div className="text-center">
                    <div className="text-4xl font-bold text-gray-900 mb-2">{post.rating}/5</div>
                    <div className="flex items-center justify-center gap-1 mb-4">
                      {[...Array(5)].map((_, i) => (
                        <span key={i} className={`text-xl ${i < Math.floor(post.rating!) ? 'text-yellow-400' : 'text-gray-300'}`}>
                          ★
                        </span>
                      ))}
                    </div>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span>Build Quality</span>
                        <span className="font-semibold">9/10</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Value for Money</span>
                        <span className="font-semibold">8/10</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Features</span>
                        <span className="font-semibold">9/10</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Pros & Cons */}
              {post.products[0] && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Quick Verdict</h3>
                  <div className="space-y-4">
                    <div>
                      <h4 className="font-semibold text-green-700 mb-2">Pros</h4>
                      <ul className="space-y-1">
                        {(post.products[0].pros || post.products[0].features.slice(0, 3)).map((pro, index) => (
                          <li key={index} className="text-sm text-gray-600 flex items-center gap-2">
                            <span className="text-green-500">✓</span>
                            {pro}
                          </li>
                        ))}
                      </ul>
                    </div>
                    {post.products[0].cons && (
                      <div>
                        <h4 className="font-semibold text-red-700 mb-2">Cons</h4>
                        <ul className="space-y-1">
                          {post.products[0].cons.map((con, index) => (
                            <li key={index} className="text-sm text-gray-600 flex items-center gap-2">
                              <span className="text-red-500">✗</span>
                              {con}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderTutorialLayout = () => (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-orange-600 to-red-700 text-white py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">{post.title}</h1>
          <p className="text-xl text-orange-100 max-w-3xl mx-auto leading-relaxed">{post.excerpt}</p>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid lg:grid-cols-4 gap-12">
          {/* Main Content */}
          <div className="lg:col-span-3">
            <article className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
              {/* Article Content */}
              <div 
                className="prose prose-lg max-w-none"
                dangerouslySetInnerHTML={{ __html: post.content }}
              />

              {/* Product Recommendations */}
              <BlogProductShowcase
                products={post.products}
                style="grid"
                title="Recommended Equipment"
                subtitle="Tools and products mentioned in this tutorial"
                maxProducts={4}
              />
            </article>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="sticky top-8 space-y-8">
              {/* Table of Contents */}
              {post.tableOfContents && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Tutorial Steps</h3>
                  <nav className="space-y-2">
                    {post.tableOfContents.map((item) => (
                      <a
                        key={item.id}
                        href={`#${item.id}`}
                        className="block text-sm text-gray-600 hover:text-orange-600 hover:font-medium transition-colors"
                      >
                        {item.title}
                      </a>
                    ))}
                  </nav>
                </div>
              )}

              {/* Equipment Needed */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-4">Equipment Needed</h3>
                <div className="space-y-3">
                  {post.products.slice(0, 3).map((product) => (
                    <div key={product.id} className="flex items-center gap-3">
                      <div className="relative h-10 w-10 bg-gray-100 rounded overflow-hidden">
                        <Image
                          src={product.image}
                          alt={product.name}
                          fill
                          className=""
                          style={{ objectFit: 'contain', backgroundColor: 'white' }}
                        />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="font-semibold text-gray-900 text-sm truncate">{product.name}</p>
                        <p className="text-sm text-gray-600">€{product.price}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderNewsLayout = () => (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-indigo-600 to-purple-700 text-white py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="flex items-center justify-center gap-4 mb-6">
            <span className="text-xs font-semibold text-indigo-200 uppercase tracking-wide">News</span>
            <span className="text-indigo-200">•</span>
            <span className="text-indigo-200">{post.date}</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">{post.title}</h1>
          <p className="text-xl text-indigo-100 max-w-3xl mx-auto leading-relaxed">{post.excerpt}</p>
        </div>
      </section>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <article className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
          {/* Article Content */}
          <div 
            className="prose prose-lg max-w-none"
            dangerouslySetInnerHTML={{ __html: post.content }}
          />

          {/* Related Products */}
          {post.products.length > 0 && (
            <BlogProductShowcase
              products={post.products}
              style="carousel"
              title="Related Products"
              subtitle="Products mentioned in this news article"
            />
          )}
        </article>
      </div>
    </div>
  );

  // Buyer's Guide Layout - Comprehensive buying advice
  const renderBuyersGuideLayout = () => (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-teal-600 to-cyan-700 text-white py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="flex items-center justify-center gap-4 mb-6">
            <span className="text-xs font-semibold text-teal-200 uppercase tracking-wide">{post.category}</span>
            <span className="text-teal-200">•</span>
            <span className="text-teal-200">{post.date}</span>
            <span className="text-teal-200">•</span>
            <span className="text-teal-200">{post.readTime}</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">{post.title}</h1>
          <p className="text-xl text-teal-100 max-w-3xl mx-auto leading-relaxed">{post.excerpt}</p>
          <div className="mt-8 flex items-center justify-center gap-4">
            <span className="text-teal-200">By {post.author}</span>
            {post.expertTested && (
              <span className="bg-green-600 text-white px-3 py-1 rounded-full text-sm font-bold flex items-center gap-1">
                <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Expert Tested
              </span>
            )}
          </div>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid lg:grid-cols-4 gap-12">
          {/* Main Content */}
          <div className="lg:col-span-3">
            <article className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
              {/* Featured Product Showcase */}
              <BlogProductShowcase
                products={post.products}
                style="recommended"
                title="Our Top Recommendations"
                subtitle="Hand-picked products that offer the best value and performance"
              />

              {/* Article Content */}
              <div 
                className="prose prose-lg max-w-none mt-12"
                dangerouslySetInnerHTML={{ __html: post.content }}
              />

              {/* Product Grid */}
              <BlogProductShowcase
                products={post.products}
                style="grid"
                title="All Recommended Products"
                maxProducts={8}
              />

              {/* Comparison Table */}
              {post.products.length > 1 && (
                <ProductComparisonTable
                  products={post.products.map(product => ({
                    ...product,
                    features: {
                      price: `€${product.price}`,
                      rating: product.rating,
                      reviews: product.reviewCount,
                      brand: product.brand,
                      category: product.category
                    },
                    pros: product.pros || product.features.slice(0, 3),
                    cons: product.cons || ['Check individual reviews for details'],
                    bestFor: product.bestFor || 'General use'
                  }))}
                  features={[
                    { key: 'price', label: 'Price', type: 'text' },
                    { key: 'rating', label: 'Rating', type: 'rating' },
                    { key: 'reviews', label: 'Reviews', type: 'number' },
                    { key: 'brand', label: 'Brand', type: 'text' }
                  ]}
                  title="Product Comparison"
                  description="Compare all recommended products side by side"
                />
              )}
            </article>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="sticky top-8 space-y-8">
              {/* Table of Contents */}
              {post.tableOfContents && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Buying Guide</h3>
                  <nav className="space-y-2">
                    {post.tableOfContents.map((item) => (
                      <a
                        key={item.id}
                        href={`#${item.id}`}
                        className="block text-sm text-gray-600 hover:text-teal-600 hover:font-medium transition-colors"
                      >
                        {item.title}
                      </a>
                    ))}
                  </nav>
                </div>
              )}

              {/* Quick Product Picks */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-4">Quick Picks</h3>
                <div className="space-y-4">
                  {post.products.slice(0, 3).map((product) => (
                    <div key={product.id} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                      <div className="relative h-12 w-12 bg-gray-100 rounded-lg overflow-hidden">
                        <Image
                          src={product.image}
                          alt={product.name}
                          fill
                          className=""
                          style={{ objectFit: 'contain', backgroundColor: 'white' }}
                        />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h4 className="font-semibold text-gray-900 text-sm truncate">{product.name}</h4>
                        <p className="text-sm font-bold text-gray-900">€{product.price}</p>
                      </div>
                      <Link
                        href={product.affiliateUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="bg-teal-600 text-white px-3 py-1 rounded text-xs font-semibold hover:bg-teal-700 transition-colors"
                      >
                        View
                      </Link>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  // Step-by-Step Tutorial Layout
  const renderStepByStepLayout = () => (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-emerald-600 to-green-700 text-white py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">{post.title}</h1>
          <p className="text-xl text-emerald-100 max-w-3xl mx-auto leading-relaxed">{post.excerpt}</p>
          <div className="mt-6 flex items-center justify-center gap-4">
            <span className="text-emerald-200">By {post.author}</span>
            <span className="text-emerald-200">•</span>
            <span className="text-emerald-200">{post.readTime}</span>
          </div>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid lg:grid-cols-4 gap-12">
          {/* Main Content */}
          <div className="lg:col-span-3">
            <article className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
              {/* Article Content */}
              <div 
                className="prose prose-lg max-w-none"
                dangerouslySetInnerHTML={{ __html: post.content }}
              />

              {/* Product Recommendations */}
              <BlogProductShowcase
                products={post.products}
                style="grid"
                title="Equipment Needed"
                subtitle="Tools and products mentioned in this tutorial"
                maxProducts={6}
              />
            </article>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="sticky top-8 space-y-8">
              {/* Tutorial Steps */}
              {post.tableOfContents && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Tutorial Steps</h3>
                  <nav className="space-y-2">
                    {post.tableOfContents.map((item, index) => (
                      <a
                        key={item.id}
                        href={`#${item.id}`}
                        className="block text-sm text-gray-600 hover:text-emerald-600 hover:font-medium transition-colors"
                      >
                        <span className="inline-block w-6 h-6 bg-emerald-100 text-emerald-800 rounded-full text-xs font-bold text-center mr-2">
                          {index + 1}
                        </span>
                        {item.title}
                      </a>
                    ))}
                  </nav>
                </div>
              )}

              {/* Equipment Needed */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-4">Equipment Needed</h3>
                <div className="space-y-3">
                  {post.products.slice(0, 4).map((product) => (
                    <div key={product.id} className="flex items-center gap-3">
                      <div className="relative h-10 w-10 bg-gray-100 rounded-lg overflow-hidden">
                        <Image
                          src={product.image}
                          alt={product.name}
                          fill
                          className=""
                          style={{ objectFit: 'contain', backgroundColor: 'white' }}
                        />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="font-semibold text-gray-900 text-sm truncate">{product.name}</p>
                        <p className="text-sm text-gray-600">€{product.price}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  // Lists and Rankings Layout
  const renderListsRankingsLayout = () => (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-amber-600 to-yellow-700 text-white py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">{post.title}</h1>
          <p className="text-xl text-amber-100 max-w-3xl mx-auto leading-relaxed">{post.excerpt}</p>
          {post.rating && (
            <div className="mt-6 flex items-center justify-center gap-2">
              <div className="flex items-center gap-1">
                {[...Array(5)].map((_, i) => (
                  <span key={i} className={`text-2xl ${i < Math.floor(post.rating!) ? 'text-yellow-400' : 'text-gray-300'}`}>
                    ★
                  </span>
                ))}
              </div>
              <span className="text-xl font-bold">{post.rating}/5</span>
            </div>
          )}
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <article className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
          {/* Article Content */}
          <div 
            className="prose prose-lg max-w-none"
            dangerouslySetInnerHTML={{ __html: post.content }}
          />

          {/* Product Rankings */}
          <BlogProductShowcase
            products={post.products}
            style="featured"
            title="Top Products Ranked"
            subtitle="Our expert picks ranked by performance and value"
          />

          {/* Product Grid */}
          <BlogProductShowcase
            products={post.products}
            style="grid"
            title="All Ranked Products"
            maxProducts={10}
          />
        </article>
      </div>
    </div>
  );

  // Educational Layout
  const renderEducationalLayout = () => (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-violet-600 to-purple-700 text-white py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">{post.title}</h1>
          <p className="text-xl text-violet-100 max-w-3xl mx-auto leading-relaxed">{post.excerpt}</p>
          <div className="mt-6 flex items-center justify-center gap-4">
            <span className="text-violet-200">By {post.author}</span>
            <span className="text-violet-200">•</span>
            <span className="text-violet-200">{post.readTime}</span>
          </div>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid lg:grid-cols-4 gap-12">
          {/* Main Content */}
          <div className="lg:col-span-3">
            <article className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
              {/* Article Content */}
              <div 
                className="prose prose-lg max-w-none"
                dangerouslySetInnerHTML={{ __html: post.content }}
              />

              {/* Related Products */}
              {post.products.length > 0 && (
                <BlogProductShowcase
                  products={post.products}
                  style="recommended"
                  title="Products Mentioned"
                  subtitle="Equipment and tools referenced in this educational content"
                />
              )}
            </article>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="sticky top-8 space-y-8">
              {/* Table of Contents */}
              {post.tableOfContents && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Learning Path</h3>
                  <nav className="space-y-2">
                    {post.tableOfContents.map((item) => (
                      <a
                        key={item.id}
                        href={`#${item.id}`}
                        className="block text-sm text-gray-600 hover:text-violet-600 hover:font-medium transition-colors"
                      >
                        {item.title}
                      </a>
                    ))}
                  </nav>
                </div>
              )}

              {/* Key Concepts */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-4">Key Concepts</h3>
                <div className="space-y-2">
                  {post.tags.slice(0, 5).map((tag) => (
                    <span key={tag} className="inline-block px-3 py-1 bg-violet-100 text-violet-800 rounded-full text-sm font-medium mr-2 mb-2">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  // Extended Comparison Layout
  const renderExtendedComparisonLayout = () => (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-rose-600 to-pink-700 text-white py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">{post.title}</h1>
          <p className="text-xl text-rose-100 max-w-3xl mx-auto leading-relaxed">{post.excerpt}</p>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <article className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
          {/* Product Showcase */}
          <BlogProductShowcase
            products={post.products}
            style="featured"
            title="Products Compared"
            subtitle="Detailed comparison of the top products in this category"
          />

          {/* Article Content */}
          <div 
            className="prose prose-lg max-w-none mt-12"
            dangerouslySetInnerHTML={{ __html: post.content }}
          />

          {/* Detailed Comparison Table */}
          <ProductComparisonTable
            products={post.products.map(product => ({
              ...product,
              features: {
                price: `€${product.price}`,
                rating: product.rating,
                reviews: product.reviewCount,
                brand: product.brand,
                category: product.category,
                features: product.features.join(', ')
              },
              pros: product.pros || product.features.slice(0, 4),
              cons: product.cons || ['Check individual reviews for details'],
              bestFor: product.bestFor || 'General use'
            }))}
            features={[
              { key: 'price', label: 'Price', type: 'text' },
              { key: 'rating', label: 'Rating', type: 'rating' },
              { key: 'reviews', label: 'Reviews', type: 'number' },
              { key: 'brand', label: 'Brand', type: 'text' },
              { key: 'features', label: 'Key Features', type: 'text' }
            ]}
            title="Detailed Comparison"
            description="Compare all features and specifications"
          />
        </article>
      </div>
    </div>
  );

  // Trends and News Layout
  const renderTrendsNewsLayout = () => (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-sky-600 to-blue-700 text-white py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="flex items-center justify-center gap-4 mb-6">
            <span className="text-xs font-semibold text-sky-200 uppercase tracking-wide">Industry News</span>
            <span className="text-sky-200">•</span>
            <span className="text-sky-200">{post.date}</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">{post.title}</h1>
          <p className="text-xl text-sky-100 max-w-3xl mx-auto leading-relaxed">{post.excerpt}</p>
        </div>
      </section>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <article className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
          {/* Article Content */}
          <div 
            className="prose prose-lg max-w-none"
            dangerouslySetInnerHTML={{ __html: post.content }}
          />

          {/* Related Products */}
          {post.products.length > 0 && (
            <BlogProductShowcase
              products={post.products}
              style="carousel"
              title="Related Products"
              subtitle="Products mentioned in this industry news"
            />
          )}
        </article>
      </div>
    </div>
  );

  // Maintenance and Accessories Layout
  const renderMaintenanceAccessoriesLayout = () => (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-lime-600 to-green-700 text-white py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">{post.title}</h1>
          <p className="text-xl text-lime-100 max-w-3xl mx-auto leading-relaxed">{post.excerpt}</p>
          <div className="mt-6 flex items-center justify-center gap-4">
            <span className="text-lime-200">By {post.author}</span>
            <span className="text-lime-200">•</span>
            <span className="text-lime-200">{post.readTime}</span>
          </div>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid lg:grid-cols-4 gap-12">
          {/* Main Content */}
          <div className="lg:col-span-3">
            <article className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
              {/* Article Content */}
              <div 
                className="prose prose-lg max-w-none"
                dangerouslySetInnerHTML={{ __html: post.content }}
              />

              {/* Product Recommendations */}
              <BlogProductShowcase
                products={post.products}
                style="grid"
                title="Maintenance & Accessories"
                subtitle="Essential tools and products for care and preservation"
                maxProducts={8}
              />
            </article>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="sticky top-8 space-y-8">
              {/* Maintenance Tips */}
              {post.tableOfContents && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Maintenance Tips</h3>
                  <nav className="space-y-2">
                    {post.tableOfContents.map((item) => (
                      <a
                        key={item.id}
                        href={`#${item.id}`}
                        className="block text-sm text-gray-600 hover:text-lime-600 hover:font-medium transition-colors"
                      >
                        {item.title}
                      </a>
                    ))}
                  </nav>
                </div>
              )}

              {/* Essential Tools */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-4">Essential Tools</h3>
                <div className="space-y-3">
                  {post.products.slice(0, 4).map((product) => (
                    <div key={product.id} className="flex items-center gap-3">
                      <div className="relative h-10 w-10 bg-gray-100 rounded-lg overflow-hidden">
                        <Image
                          src={product.image}
                          alt={product.name}
                          fill
                          className=""
                          style={{ objectFit: 'contain', backgroundColor: 'white' }}
                        />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="font-semibold text-gray-900 text-sm truncate">{product.name}</p>
                        <p className="text-sm text-gray-600">€{product.price}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  // Inspiration and Culture Layout
  const renderInspirationCultureLayout = () => (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-fuchsia-600 to-purple-700 text-white py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">{post.title}</h1>
          <p className="text-xl text-fuchsia-100 max-w-3xl mx-auto leading-relaxed">{post.excerpt}</p>
          <div className="mt-6 flex items-center justify-center gap-4">
            <span className="text-fuchsia-200">By {post.author}</span>
            <span className="text-fuchsia-200">•</span>
            <span className="text-fuchsia-200">{post.readTime}</span>
          </div>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid lg:grid-cols-4 gap-12">
          {/* Main Content */}
          <div className="lg:col-span-3">
            <article className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
              {/* Article Content */}
              <div 
                className="prose prose-lg max-w-none"
                dangerouslySetInnerHTML={{ __html: post.content }}
              />

              {/* Related Products */}
              {post.products.length > 0 && (
                <BlogProductShowcase
                  products={post.products}
                  style="recommended"
                  title="Inspired by This Content"
                  subtitle="Products and equipment related to this cultural content"
                />
              )}
            </article>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="sticky top-8 space-y-8">
              {/* Cultural Topics */}
              {post.tableOfContents && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Topics Covered</h3>
                  <nav className="space-y-2">
                    {post.tableOfContents.map((item) => (
                      <a
                        key={item.id}
                        href={`#${item.id}`}
                        className="block text-sm text-gray-600 hover:text-fuchsia-600 hover:font-medium transition-colors"
                      >
                        {item.title}
                      </a>
                    ))}
                  </nav>
                </div>
              )}

              {/* Related Topics */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-4">Related Topics</h3>
                <div className="space-y-2">
                  {post.tags.slice(0, 6).map((tag) => (
                    <span key={tag} className="inline-block px-3 py-1 bg-fuchsia-100 text-fuchsia-800 rounded-full text-sm font-medium mr-2 mb-2">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  // Render based on layout style
  switch (getLayoutStyle()) {
    case 'buying-guide-layout':
      return renderBuyingGuideLayout();
    case 'comparison-layout':
      return renderComparisonLayout();
    case 'review-layout':
      return renderReviewLayout();
    case 'tutorial-layout':
      return renderTutorialLayout();
    case 'news-layout':
      return renderNewsLayout();
    case 'buyers-guide-layout':
      return renderBuyersGuideLayout();
    case 'step-by-step-layout':
      return renderStepByStepLayout();
    case 'lists-rankings-layout':
      return renderListsRankingsLayout();
    case 'educational-layout':
      return renderEducationalLayout();
    case 'extended-comparison-layout':
      return renderExtendedComparisonLayout();
    case 'trends-news-layout':
      return renderTrendsNewsLayout();
    case 'maintenance-accessories-layout':
      return renderMaintenanceAccessoriesLayout();
    case 'inspiration-culture-layout':
      return renderInspirationCultureLayout();
    default:
      return renderBuyingGuideLayout();
  }
}
