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
          content="Expert guides, reviews, tutorials and stories about musical instruments. Learn from our comprehensive buying guides and in-depth product reviews." 
        />
      </Head>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Featured */}
        {!currentCategory && !currentTag && featuredPosts && featuredPosts.length > 0 && (
          <section className="mb-12 grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Hero main */}
            <a href={`/blog/${featuredPosts[0].slug}`} className="lg:col-span-2 group block bg-white rounded-xl overflow-hidden shadow hover:shadow-lg transition-shadow">
              {featuredPosts[0].featured_image && (
                <div className="h-72 w-full overflow-hidden">
                  <img src={featuredPosts[0].featured_image} alt={featuredPosts[0].title} className="w-full h-full object-cover group-hover:scale-[1.02] transition-transform" />
                </div>
              )}
              <div className="p-6">
                <div className="text-sm text-brand-primary font-semibold mb-2">Featured</div>
                <h2 className="text-3xl font-extrabold text-gray-900 mb-2 line-clamp-2">{featuredPosts[0].title}</h2>
                {featuredPosts[0].excerpt && <p className="text-gray-600 line-clamp-3">{featuredPosts[0].excerpt}</p>}
              </div>
            </a>
            {/* Secondary featured */}
            <div className="space-y-6">
              {featuredPosts.slice(1,3).map((fp) => (
                <a key={fp.id} href={`/blog/${fp.slug}`} className="group block bg-white rounded-xl overflow-hidden shadow hover:shadow-lg transition-shadow">
                  {fp.featured_image && (
                    <div className="h-32 w-full overflow-hidden">
                      <img src={fp.featured_image} alt={fp.title} className="w-full h-full object-cover group-hover:scale-[1.02] transition-transform" />
                    </div>
                  )}
                  <div className="p-4">
                    <h3 className="text-lg font-bold text-gray-900 line-clamp-2">{fp.title}</h3>
                    {fp.excerpt && <p className="text-gray-600 text-sm line-clamp-2 mt-1">{fp.excerpt}</p>}
                  </div>
                </a>
              ))}
            </div>
          </section>
        )}

        {/* Search Bar */}
        <div className="max-w-md mx-auto mb-8">
          <div className="relative">
            <input
              type="text"
              placeholder="Search blog posts..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-primary focus:border-transparent"
            />
            <MagnifyingGlassIcon className="absolute left-3 top-3.5 h-5 w-5 text-gray-400" />
            {isSearching && (
              <div className="absolute right-3 top-3.5">
                <div className="animate-spin h-5 w-5 border-2 border-brand-primary border-t-transparent rounded-full"></div>
              </div>
            )}
          </div>
        </div>

        {/* Category Filter */}
        {!searchQuery && (
          <div className="flex flex-wrap justify-center gap-3 mb-12 sticky top-16 bg-white/80 backdrop-blur z-10 py-3">
            <a
              href="/blog"
              className={`px-6 py-3 rounded-full font-medium transition-colors ${
                !currentCategory
                  ? 'bg-brand-primary text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              All Posts
            </a>
            {categories.map((category) => (
              <a
                key={category.id}
                href={`/blog?category=${category.slug}`}
                className={`px-6 py-3 rounded-full font-medium transition-colors inline-flex items-center ${
                  currentCategory === category.slug
                    ? 'bg-brand-primary text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {category.icon && <span className="mr-2">{category.icon}</span>}
                {category.name}
              </a>
            ))}
          </div>
        )}

        {/* Featured Posts (only on main blog page) */}
        {!currentCategory && !currentTag && !searchQuery && featuredPosts.length > 0 && (
          <div className="mb-16">
            <h2 className="text-2xl font-bold text-gray-900 mb-8">Featured Posts</h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
              {featuredPosts.slice(0, 3).map((post) => (
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

        {/* Most Read + Popular Tags (main page only) */}
        {!currentCategory && !currentTag && !searchQuery && (
          <div className="mb-16 grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Most Read</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
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
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Popular Tags</h2>
              <div className="flex flex-wrap gap-2">
                {popularTags.map((tag) => (
                  <a key={tag.id} href={`/blog?tag=${tag.slug}`} className="px-3 py-1 rounded-full bg-gray-100 text-gray-700 hover:bg-gray-200 text-sm">#{tag.name}</a>
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
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mb-12">
            {/* Main grid */}
            <div className="lg:col-span-8 grid grid-cols-1 md:grid-cols-2 gap-8">
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
            {/* Sidebar */}
            <aside className="lg:col-span-4 space-y-8">
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Most Read</h2>
                <div className="space-y-4">
                  {mostRead.map((p) => (
                    <a key={p.id} href={`/blog/${p.slug}`} className="block group">
                      <h3 className="font-medium text-gray-900 group-hover:text-brand-primary line-clamp-2">{p.title}</h3>
                      {p.excerpt && <p className="text-gray-600 text-sm line-clamp-2">{p.excerpt}</p>}
                    </a>
                  ))}
                </div>
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Popular Tags</h2>
                <div className="flex flex-wrap gap-2">
                  {popularTags.map((tag) => (
                    <a key={tag.id} href={`/blog?tag=${tag.slug}`} className="px-3 py-1 rounded-full bg-gray-100 text-gray-700 hover:bg-gray-200 text-sm">#{tag.name}</a>
                  ))}
                </div>
              </div>
            </aside>
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">
              {searchQuery 
                ? 'No posts found for your search.'
                : 'No blog posts available at the moment.'
              }
            </p>
          </div>
        )}

        {/* Load More Button (placeholder for pagination) */}
        {!searchQuery && displayPosts.length > 0 && displayPosts.length < totalPosts && (
          <div className="text-center">
            <button className="px-8 py-3 bg-brand-primary text-white font-medium rounded-lg hover:bg-brand-dark transition-colors">
              Load More Posts
            </button>
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
