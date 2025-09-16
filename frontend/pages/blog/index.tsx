import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import { GetServerSideProps } from 'next';
import BlogPostCard from '../../src/components/BlogPostCard';
import { BlogPostSummary, BlogCategory } from '../../src/types/blog';
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';

interface BlogPageProps {
  posts: BlogPostSummary[];
  categories: BlogCategory[];
  totalPosts: number;
  currentCategory?: string;
  currentTag?: string;
  featuredPosts: BlogPostSummary[];
  mostRead: BlogPostSummary[];
  popularTags: { id: number; name: string; slug: string }[];
}

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://getyourmusicgear-api.azurewebsites.net';
const PROXY_BASE = '/api/proxy/v1';

export default function BlogPage({ 
  posts, 
  categories, 
  totalPosts, 
  currentCategory, 
  currentTag,
  featuredPosts,
  mostRead,
  popularTags,
}: BlogPageProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<BlogPostSummary[]>([]);
  const [isSearching, setIsSearching] = useState(false);

  const handleSearch = async (query: string) => {
    if (query.trim().length < 2) {
      setSearchResults([]);
      return;
    }

    setIsSearching(true);
    try {
      const response = await fetch(`${PROXY_BASE}/blog/search?q=${encodeURIComponent(query)}`);
      const data = await response.json();
      setSearchResults(data.results || []);
    } catch (error) {
      console.error('Search failed:', error);
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      handleSearch(searchQuery);
    }, 300);

    return () => clearTimeout(timer);
  }, [searchQuery]);

  const displayPosts = searchQuery.trim() ? searchResults : posts;
  const pageTitle = currentCategory 
    ? `${categories.find(c => c.slug === currentCategory)?.name} - Blog` 
    : currentTag
      ? `#${currentTag} - Blog`
      : 'Blog';

  return (
    <>
      <Head>
        <title>{pageTitle} - GetYourMusicGear</title>
        <meta 
          name="description" 
          content="Expert music gear guides, reviews, and tutorials. Find the best instruments with our comprehensive buying guides, product comparisons, and pro tips from industry experts." 
        />
        <meta property="og:title" content={`${pageTitle} - GetYourMusicGear`} />
        <meta property="og:description" content="Expert music gear guides, reviews, and tutorials. Find the best instruments with our comprehensive buying guides and product comparisons." />
        <meta property="og:type" content="website" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large" />
        <link rel="canonical" href={`https://getyourmusicgear.com/blog${currentCategory ? `?category=${currentCategory}` : ''}${currentTag ? `?tag=${currentTag}` : ''}`} />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              '@context': 'https://schema.org',
              '@type': 'Blog',
              name: 'GetYourMusicGear Blog',
              description: 'Expert music gear guides, reviews, and tutorials',
              url: 'https://getyourmusicgear.com/blog',
              publisher: {
                '@type': 'Organization',
                name: 'GetYourMusicGear',
                logo: 'https://getyourmusicgear.com/logo.png'
              },
              mainEntityOfPage: 'https://getyourmusicgear.com/blog'
            })
          }}
        />
      </Head>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Featured */}
        {!currentCategory && !currentTag && featuredPosts && featuredPosts.length > 0 && (
          <section className="mb-16">
            <div className="relative h-[600px] rounded-2xl overflow-hidden bg-gradient-to-br from-gray-900 to-gray-800 shadow-2xl">
              {featuredPosts[0].featured_image && (
                <img 
                  src={featuredPosts[0].featured_image} 
                  alt={featuredPosts[0].title} 
                  className="absolute inset-0 w-full h-full object-cover opacity-40" 
                />
              )}
              <div className="absolute inset-0 bg-gradient-to-r from-black/60 via-black/40 to-transparent" />
              <div className="relative h-full flex items-center">
                <div className="max-w-2xl mx-auto px-8 text-white">
                  <div className="inline-flex items-center px-4 py-2 rounded-full bg-brand-primary/20 backdrop-blur-sm border border-brand-primary/30 mb-6">
                    <span className="text-brand-primary font-semibold">Featured Article</span>
                  </div>
                  <h1 className="text-5xl md:text-6xl font-extrabold leading-tight mb-6">
                    {featuredPosts[0].title}
                  </h1>
                  {featuredPosts[0].excerpt && (
                    <p className="text-xl text-gray-300 leading-relaxed mb-8 line-clamp-3">
                      {featuredPosts[0].excerpt}
                    </p>
                  )}
                  <div className="flex items-center gap-6 mb-8">
                    <div className="flex items-center gap-2">
                      <img 
                        src={`https://ui-avatars.com/api/?name=${encodeURIComponent(featuredPosts[0].author_name)}&background=0D8ABC&color=fff`} 
                        alt={featuredPosts[0].author_name} 
                        className="w-10 h-10 rounded-full" 
                      />
                      <span className="font-medium">{featuredPosts[0].author_name}</span>
                    </div>
                    {featuredPosts[0].reading_time && (
                      <span className="text-gray-300">{featuredPosts[0].reading_time} min read</span>
                    )}
                  </div>
                  <a 
                    href={`/blog/${featuredPosts[0].slug}`}
                    className="inline-flex items-center px-8 py-4 bg-brand-primary hover:bg-brand-dark text-white font-semibold rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
                  >
                    Read Full Article
                    <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                    </svg>
                  </a>
                </div>
              </div>
            </div>
            
            {/* Secondary featured grid */}
            {featuredPosts.length > 1 && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mt-12">
                {featuredPosts.slice(1, 4).map((fp) => (
                  <article key={fp.id} className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden group">
                    {fp.featured_image && (
                      <div className="h-48 overflow-hidden">
                        <img 
                          src={fp.featured_image} 
                          alt={fp.title} 
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" 
                        />
                      </div>
                    )}
                    <div className="p-6">
                      <div className="flex items-center gap-2 mb-3">
                        <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-brand-primary/10 text-brand-primary">
                          Trending
                        </span>
                        {fp.reading_time && (
                          <span className="text-gray-500 text-sm">{fp.reading_time} min</span>
                        )}
                      </div>
                      <h3 className="text-xl font-bold text-gray-900 mb-3 line-clamp-2 group-hover:text-brand-primary transition-colors">
                        <a href={`/blog/${fp.slug}`}>{fp.title}</a>
                      </h3>
                      {fp.excerpt && (
                        <p className="text-gray-600 line-clamp-3 mb-4">{fp.excerpt}</p>
                      )}
                      <a 
                        href={`/blog/${fp.slug}`}
                        className="inline-flex items-center text-brand-primary hover:text-brand-dark font-medium transition-colors"
                      >
                        Read More
                        <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                      </a>
                    </div>
                  </article>
                ))}
              </div>
            )}
          </section>
        )}

        {/* Search Bar with Enhanced Design */}
        <div className="max-w-2xl mx-auto mb-12">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <MagnifyingGlassIcon className="h-6 w-6 text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="Search guides, reviews, and tutorials..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-12 py-4 text-lg border-2 border-gray-200 rounded-2xl focus:ring-2 focus:ring-brand-primary focus:border-brand-primary transition-all duration-300 shadow-sm hover:shadow-md"
            />
            {isSearching && (
              <div className="absolute right-4 top-1/2 transform -translate-y-1/2">
                <div className="animate-spin h-6 w-6 border-2 border-brand-primary border-t-transparent rounded-full"></div>
              </div>
            )}
            {!isSearching && searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            )}
          </div>
          {searchQuery && searchResults.length > 0 && (
            <div className="mt-2 text-center text-gray-600">
              Found {searchResults.length} articles
            </div>
          )}
        </div>

        {/* Enhanced Category Filter */}
        {!searchQuery && (
          <div className="mb-12">
            <div className="bg-white/90 backdrop-blur-sm sticky top-16 z-10 py-6 -mx-4 px-4 sm:-mx-6 sm:px-6 lg:-mx-8 lg:px-8 border-b border-gray-200">
              <div className="max-w-7xl mx-auto">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-lg font-semibold text-gray-900">Browse by Category</h2>
                  <div className="text-sm text-gray-500">
                    {categories.length + 1} categories
                  </div>
                </div>
                <div className="flex flex-wrap gap-3">
                  <a
                    href="/blog"
                    className={`px-6 py-3 rounded-xl font-semibold transition-all duration-300 ${
                      !currentCategory
                        ? 'bg-brand-primary text-white shadow-lg scale-105'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200 hover:scale-105'
                    }`}
                  >
                    All Posts
                  </a>
                  {categories.map((category) => (
                    <a
                      key={category.id}
                      href={`/blog?category=${category.slug}`}
                      className={`px-6 py-3 rounded-xl font-semibold transition-all duration-300 inline-flex items-center ${
                        currentCategory === category.slug
                          ? 'bg-brand-primary text-white shadow-lg scale-105'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200 hover:scale-105'
                      }`}
                    >
                      {category.icon && <span className="mr-2 text-lg">{category.icon}</span>}
                      {category.name}
                    </a>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Featured Posts Section (enhanced) */}
        {!currentCategory && !currentTag && !searchQuery && featuredPosts.length > 3 && (
          <div className="mb-16">
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-3xl font-bold text-gray-900 flex items-center">
                Featured Articles
              </h2>
              <a href="/blog?featured=true" className="text-brand-primary hover:text-brand-dark font-medium">
                View All Featured →
              </a>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
              {featuredPosts.slice(3, 6).map((post) => (
                <BlogPostCard
                  key={post.id}
                  post={post}
                  size="large"
                  showExcerpt={true}
                  showCategory={true}
                  showMeta={true}
                />
              ))}
            </div>
          </div>
        )}

        {/* Enhanced Content Sections */}
        {!currentCategory && !currentTag && !searchQuery && (
          <div className="mb-16">
            {/* Most Read Section */}
            <div className="mb-12">
              <div className="flex items-center justify-between mb-8">
                <h2 className="text-3xl font-bold text-gray-900 flex items-center">
                  Most Read This Week
                </h2>
                <a href="/blog?sort=views" className="text-brand-primary hover:text-brand-dark font-medium">
                  View All →
                </a>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {mostRead.slice(0, 4).map((post) => (
                  <BlogPostCard
                    key={post.id}
                    post={post}
                    size="small"
                    showExcerpt={false}
                    showCategory={true}
                    showMeta={true}
                  />
                ))}
              </div>
            </div>


            {/* Popular Tags Cloud */}
            <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">Popular Topics</h2>
              <div className="flex flex-wrap justify-center gap-3">
                {popularTags.map((tag, index) => (
                  <a 
                    key={tag.id} 
                    href={`/blog?tag=${tag.slug}`} 
                    className={`px-4 py-2 rounded-full font-medium transition-all duration-300 hover:scale-105 ${
                      index < 3 
                        ? 'bg-brand-primary text-white shadow-lg' 
                        : index < 8
                        ? 'bg-white text-brand-primary border-2 border-brand-primary shadow-md'
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                  >
                    #{tag.name}
                  </a>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Search Results Info */}
        {searchQuery && (
          <div className="mb-8 text-center">
            <p className="text-gray-600">
              {isSearching 
                ? 'Searching...' 
                : `Found ${searchResults.length} posts for "${searchQuery}"`
              }
            </p>
          </div>
        )}

        {/* Blog Posts Grid */}
        {displayPosts.length > 0 ? (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 mb-12">
            {/* Main Content */}
            <main className="lg:col-span-8">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {displayPosts.map((post) => (
                  <BlogPostCard
                    key={post.id}
                    post={post}
                    size="medium"
                    showExcerpt={true}
                    showCategory={true}
                    showMeta={true}
                  />
                ))}
              </div>
            </main>
            
            {/* Enhanced Sidebar */}
            <aside className="lg:col-span-4 space-y-8">
              {/* Newsletter Signup */}
              <div className="bg-gradient-to-br from-brand-primary to-brand-dark rounded-xl p-6 text-white">
                <h3 className="text-xl font-bold mb-3">Expert Music Gear Insights</h3>
                <p className="text-brand-light mb-4 text-sm">
                  Get weekly buying guides, deal alerts, and pro tips delivered to your inbox.
                </p>
                <form className="space-y-3">
                  <input
                    type="email"
                    placeholder="your@email.com"
                    className="w-full px-4 py-2 rounded-lg text-gray-900 placeholder-gray-500 focus:ring-2 focus:ring-white focus:outline-none"
                  />
                  <button className="w-full py-2 bg-white text-brand-primary font-semibold rounded-lg hover:bg-gray-100 transition-colors">
                    Subscribe Free
                  </button>
                </form>
                <p className="text-xs text-brand-light mt-3">
                  No spam. Unsubscribe anytime.
                </p>
              </div>

              {/* Trending This Week */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                  Trending This Week
                </h3>
                <div className="space-y-4">
                  {mostRead.slice(0, 5).map((post, index) => (
                    <a key={post.id} href={`/blog/${post.slug}`} className="block group">
                      <div className="flex items-start gap-3">
                        <span className="flex-shrink-0 w-6 h-6 bg-brand-primary text-white text-xs font-bold rounded-full flex items-center justify-center">
                          {index + 1}
                        </span>
                        <div className="flex-1">
                          <h4 className="font-medium text-gray-900 group-hover:text-brand-primary line-clamp-2 transition-colors">
                            {post.title}
                          </h4>
                          {post.view_count && (
                            <p className="text-xs text-gray-500 mt-1">
                              {post.view_count} views
                            </p>
                          )}
                        </div>
                      </div>
                    </a>
                  ))}
                </div>
              </div>

              {/* Quick Navigation */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-4">Quick Navigation</h3>
                <div className="space-y-2">
                  <a href="/blog?category=buying-guide" className="block p-3 rounded-lg hover:bg-gray-50 transition-colors">
                    <div className="font-medium text-gray-900">Buying Guides</div>
                    <div className="text-sm text-gray-600">Expert recommendations & comparisons</div>
                  </a>
                  <a href="/blog?category=reviews" className="block p-3 rounded-lg hover:bg-gray-50 transition-colors">
                    <div className="font-medium text-gray-900">Product Reviews</div>
                    <div className="text-sm text-gray-600">In-depth analysis & testing</div>
                  </a>
                  <a href="/blog?category=deals" className="block p-3 rounded-lg hover:bg-gray-50 transition-colors">
                    <div className="font-medium text-gray-900">Deal Alerts</div>
                    <div className="text-sm text-gray-600">Latest discounts & bargains</div>
                  </a>
                  <a href="/blog?category=tutorial" className="block p-3 rounded-lg hover:bg-gray-50 transition-colors">
                    <div className="font-medium text-gray-900">Tutorials</div>
                    <div className="text-sm text-gray-600">How-to guides & tips</div>
                  </a>
                </div>
              </div>

              {/* Popular Tags */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-4">Popular Topics</h3>
                <div className="flex flex-wrap gap-2">
                  {popularTags.slice(0, 12).map((tag) => (
                    <a 
                      key={tag.id} 
                      href={`/blog?tag=${tag.slug}`} 
                      className="px-3 py-2 rounded-lg bg-gray-100 text-gray-700 hover:bg-brand-primary hover:text-white transition-colors text-sm font-medium"
                    >
                      #{tag.name}
                    </a>
                  ))}
                </div>
              </div>

              {/* Help & Support */}
              <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-6 border border-gray-200">
                <h3 className="text-lg font-bold text-gray-900 mb-3">Need Help Choosing?</h3>
                <p className="text-gray-600 text-sm mb-4">
                  Our music gear experts are here to help you find the perfect instrument for your needs and budget.
                </p>
                <div className="space-y-3">
                  <a href="/contact" className="block w-full py-2 px-4 bg-brand-primary text-white font-medium rounded-lg hover:bg-brand-dark transition-colors text-center">
                    Ask an Expert
                  </a>
                  <a href="/compare" className="block w-full py-2 px-4 bg-white border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors text-center">
                    Compare Products
                  </a>
                </div>
              </div>
            </aside>
          </div>
        ) : (
          <div className="text-center py-16">
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              {searchQuery ? 'No posts found' : 'No posts available'}
            </h3>
            <p className="text-gray-600 mb-6">
              {searchQuery 
                ? `We couldn't find any posts matching "${searchQuery}". Try a different search term.`
                : 'We\'re working on creating amazing content for you. Check back soon!'
              }
            </p>
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="px-6 py-3 bg-brand-primary text-white font-semibold rounded-lg hover:bg-brand-dark transition-colors"
              >
                Clear Search
              </button>
            )}
          </div>
        )}

        {/* Load More / Pagination */}
        {!searchQuery && displayPosts.length > 0 && displayPosts.length < totalPosts && (
          <div className="text-center py-12">
            <div className="mb-6">
              <p className="text-gray-600 mb-4">
                Showing {displayPosts.length} of {totalPosts} articles
              </p>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-brand-primary h-2 rounded-full transition-all duration-300"
                  style={{ width: `${(displayPosts.length / totalPosts) * 100}%` }}
                ></div>
              </div>
            </div>
            <button className="px-8 py-4 bg-gradient-to-r from-brand-primary to-brand-dark text-white font-semibold rounded-xl hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1">
              Load More Articles
            </button>
          </div>
        )}
        
        {/* Footer CTA */}
        {!searchQuery && (
          <div className="bg-gradient-to-r from-gray-900 to-gray-800 rounded-2xl p-8 md:p-12 text-white text-center">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Ready to Find Your Perfect Gear?
            </h2>
            <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
              Explore our comprehensive product database with expert reviews, detailed comparisons, and unbeatable deals.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a href="/products" className="px-8 py-4 bg-brand-primary hover:bg-brand-dark text-white font-semibold rounded-xl transition-colors">
                Browse All Products
              </a>
              <a href="/compare" className="px-8 py-4 bg-white/10 hover:bg-white/20 text-white font-semibold rounded-xl transition-colors border border-white/20">
                Compare Products
              </a>
            </div>
          </div>
        )}
      </div>
    </>
  );
}

export const getServerSideProps: GetServerSideProps = async ({ query }) => {
  try {
    const { category, tag, limit = '12' } = query;
    
    // Build query parameters
    const params = new URLSearchParams();
    if (category) params.append('category', category as string);
    if (tag) params.append('tag', tag as string);
    params.append('limit', limit as string);

    // Fetch blog posts
    const postsResponse = await fetch(`${API_BASE}/api/v1/blog/posts?${params.toString()}`);
    const posts = postsResponse.ok ? await postsResponse.json() : [];

    // Fetch categories
    const categoriesResponse = await fetch(`${API_BASE}/api/v1/blog/categories`);
    const categories = categoriesResponse.ok ? await categoriesResponse.json() : [];

    // Fetch featured, most read, and popular tags (only on main page)
    let featuredPosts = [];
    let mostRead = [];
    let popularTags = [];
    if (!category && !tag) {
      const [featuredResponse, mostReadResponse, tagsResponse] = await Promise.all([
        fetch(`${API_BASE}/api/v1/blog/posts?featured=true&limit=3`),
        fetch(`${API_BASE}/api/v1/blog/posts?sort_by=views&limit=6`),
        fetch(`${API_BASE}/api/v1/blog/tags/popular?limit=20`),
      ]);
      featuredPosts = featuredResponse.ok ? await featuredResponse.json() : [];
      mostRead = mostReadResponse.ok ? await mostReadResponse.json() : [];
      popularTags = tagsResponse.ok ? await tagsResponse.json() : [];
    }

    return {
      props: {
        posts,
        categories,
        totalPosts: posts.length, // In real implementation, get from pagination
        currentCategory: category || null,
        currentTag: tag || null,
        featuredPosts,
        mostRead,
        popularTags,
      },
    };
  } catch (error) {
    console.error('Error fetching blog data:', error);
    return {
      props: {
        posts: [],
        categories: [],
        totalPosts: 0,
        featuredPosts: [],
        mostRead: [],
        popularTags: [],
      },
    };
  }
};
