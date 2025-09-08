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
}

const API_BASE_URL = (process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000') + '/api/v1';

export default function BlogPage({ 
  posts, 
  categories, 
  totalPosts, 
  currentCategory, 
  currentTag,
  featuredPosts 
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
      const response = await fetch(`${API_BASE_URL}/blog/search?q=${encodeURIComponent(query)}`);
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
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            {currentCategory 
              ? categories.find(c => c.slug === currentCategory)?.name
              : currentTag
                ? `Posts tagged with #${currentTag}`
                : 'Blog'
            }
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Expert insights, buying guides, and tutorials to help you make the best music gear decisions.
          </p>
        </div>

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
          <div className="flex flex-wrap justify-center gap-4 mb-12">
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
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
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
    const postsResponse = await fetch(`${API_BASE_URL}/blog/posts?${params.toString()}`);
    const posts = postsResponse.ok ? await postsResponse.json() : [];

    // Fetch categories
    const categoriesResponse = await fetch(`${API_BASE_URL}/blog/categories`);
    const categories = categoriesResponse.ok ? await categoriesResponse.json() : [];

    // Fetch featured posts (only if on main page)
    let featuredPosts = [];
    if (!category && !tag) {
      const featuredResponse = await fetch(`${API_BASE_URL}/blog/posts?featured=true&limit=3`);
      featuredPosts = featuredResponse.ok ? await featuredResponse.json() : [];
    }

    return {
      props: {
        posts,
        categories,
        totalPosts: posts.length, // In real implementation, get from pagination
        currentCategory: category || null,
        currentTag: tag || null,
        featuredPosts,
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
      },
    };
  }
};
