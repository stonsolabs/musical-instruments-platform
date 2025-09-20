import React from 'react';
import Link from 'next/link';
import Image from 'next/image';

interface BlogPost {
  id: number;
  title: string;
  slug: string;
  excerpt: string;
  author_name: string;
  created_at: string;
  category: string;
  featured_image?: string;
  read_time?: number;
}

interface BlogHomepageProps {
  featuredPosts: BlogPost[];
  recentPosts: BlogPost[];
  categories: Array<{
    name: string;
    slug: string;
    count: number;
  }>;
}

const BlogCard: React.FC<{ post: BlogPost; featured?: boolean }> = ({ post, featured = false }) => {
  const cardClasses = featured 
    ? "bg-white rounded-lg shadow-sm overflow-hidden hover:shadow-lg transition-shadow border border-gray-200"
    : "bg-white rounded-lg shadow-sm overflow-hidden hover:shadow-lg transition-shadow border border-gray-200";

  return (
    <article className={cardClasses}>
      <Link href={`/blog/${post.slug}`}>
        <div className="cursor-pointer">
          {/* Image */}
          <div className={`relative ${featured ? 'h-64' : 'h-48'} bg-gray-100`}>
            {post.featured_image ? (
              <Image
                src={post.featured_image}
                alt={post.title}
                fill
                className="object-cover"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center">
                <svg className="w-12 h-12 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
                </svg>
              </div>
            )}
            {/* Category Badge */}
            <div className="absolute top-4 left-4">
              <span className="inline-block px-3 py-1 text-xs font-semibold text-white rounded-full"
                    style={{backgroundColor: '#cd2418', fontFamily: 'Montserrat, sans-serif'}}>
                {post.category.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}
              </span>
            </div>
          </div>

          {/* Content */}
          <div className="p-6">
            <h3 className={`font-bold text-gray-900 mb-3 line-clamp-2 ${featured ? 'text-xl' : 'text-lg'}`}
                style={{fontFamily: 'Montserrat, sans-serif'}}>
              {post.title}
            </h3>
            
            <p className="text-gray-600 text-sm mb-4 line-clamp-3">
              {post.excerpt}
            </p>

            {/* Meta */}
            <div className="flex items-center justify-between text-xs text-gray-500">
              <div className="flex items-center space-x-4">
                <span style={{fontFamily: 'Montserrat, sans-serif'}}>
                  By {post.author_name}
                </span>
                <span>{new Date(post.created_at).toLocaleDateString()}</span>
              </div>
              {post.read_time && (
                <span>{post.read_time} min read</span>
              )}
            </div>
          </div>
        </div>
      </Link>
    </article>
  );
};

const CategoryCard: React.FC<{ category: { name: string; slug: string; count: number } }> = ({ category }) => (
  <Link href={`/blog/category/${category.slug}`}>
    <div className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-lg transition-shadow cursor-pointer">
      <h3 className="font-semibold text-gray-900 mb-2" style={{fontFamily: 'Montserrat, sans-serif'}}>
        {category.name.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}
      </h3>
      <p className="text-sm text-gray-600">{category.count} articles</p>
    </div>
  </Link>
);

const BlogHomepage: React.FC<BlogHomepageProps> = ({ featuredPosts, recentPosts, categories }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-4" style={{fontFamily: 'Montserrat, sans-serif'}}>
              Music Gear Blog
            </h1>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Expert reviews, buying guides, and insights to help you find the perfect musical instruments and gear.
            </p>
          </div>
          
          {/* Navigation */}
          <nav className="mt-8">
            <div className="flex flex-wrap justify-center gap-6">
              <Link href="/blog" className="text-sm font-medium text-red-600 border-b-2 border-red-600 pb-2" style={{fontFamily: 'Montserrat, sans-serif'}}>
                Latest
              </Link>
              <Link href="/blog/category/buying-guide" className="text-sm font-medium text-gray-600 hover:text-red-600 transition-colors pb-2" style={{fontFamily: 'Montserrat, sans-serif'}}>
                Buying Guides
              </Link>
              <Link href="/blog/category/review" className="text-sm font-medium text-gray-600 hover:text-red-600 transition-colors pb-2" style={{fontFamily: 'Montserrat, sans-serif'}}>
                Reviews
              </Link>
              <Link href="/blog/category/comparison" className="text-sm font-medium text-gray-600 hover:text-red-600 transition-colors pb-2" style={{fontFamily: 'Montserrat, sans-serif'}}>
                Comparisons
              </Link>
              <Link href="/blog/category/artist-spotlight" className="text-sm font-medium text-gray-600 hover:text-red-600 transition-colors pb-2" style={{fontFamily: 'Montserrat, sans-serif'}}>
                Artist Spotlights
              </Link>
              <Link href="/blog/category/gear-tips" className="text-sm font-medium text-gray-600 hover:text-red-600 transition-colors pb-2" style={{fontFamily: 'Montserrat, sans-serif'}}>
                Tips & Guides
              </Link>
            </div>
          </nav>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Featured Posts */}
        {featuredPosts.length > 0 && (
          <section className="mb-16">
            <h2 className="text-2xl font-bold text-gray-900 mb-8" style={{fontFamily: 'Montserrat, sans-serif'}}>
              Featured Articles
            </h2>
            <div className="grid lg:grid-cols-2 gap-8">
              {featuredPosts.slice(0, 2).map((post) => (
                <BlogCard key={post.id} post={post} featured={true} />
              ))}
            </div>
          </section>
        )}

        <div className="grid lg:grid-cols-3 gap-12">
          {/* Main Content */}
          <div className="lg:col-span-2">
            {/* Recent Posts */}
            <section>
              <div className="flex items-center justify-between mb-8">
                <h2 className="text-2xl font-bold text-gray-900" style={{fontFamily: 'Montserrat, sans-serif'}}>
                  Latest Articles
                </h2>
                <Link href="/blog/all" className="text-sm font-medium text-red-600 hover:text-red-700" style={{fontFamily: 'Montserrat, sans-serif'}}>
                  View All →
                </Link>
              </div>
              
              <div className="grid md:grid-cols-2 gap-6">
                {recentPosts.map((post) => (
                  <BlogCard key={post.id} post={post} />
                ))}
              </div>
            </section>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            {/* Categories */}
            <section className="mb-12">
              <h3 className="text-xl font-bold text-gray-900 mb-6" style={{fontFamily: 'Montserrat, sans-serif'}}>
                Browse by Category
              </h3>
              <div className="space-y-4">
                {categories.map((category, index) => (
                  <CategoryCard key={index} category={category} />
                ))}
              </div>
            </section>

            {/* Newsletter Signup */}
            <section className="bg-white border border-gray-200 rounded-lg p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4" style={{fontFamily: 'Montserrat, sans-serif'}}>
                Stay Updated
              </h3>
              <p className="text-gray-600 text-sm mb-4">
                Get the latest reviews, buying guides, and gear recommendations delivered to your inbox.
              </p>
              <form className="space-y-4">
                <input
                  type="email"
                  placeholder="Your email address"
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  style={{fontFamily: 'Arial, Helvetica, sans-serif'}}
                />
                <button
                  type="submit"
                  className="w-full text-white px-4 py-2 rounded-md hover:opacity-90 transition-colors font-semibold"
                  style={{backgroundColor: '#cd2418', fontFamily: 'Montserrat, sans-serif'}}
                >
                  Subscribe
                </button>
              </form>
            </section>

            {/* Popular Tags */}
            <section className="mt-8">
              <h3 className="text-xl font-bold text-gray-900 mb-6" style={{fontFamily: 'Montserrat, sans-serif'}}>
                Popular Tags
              </h3>
              <div className="flex flex-wrap gap-2">
                {['electric-guitar', 'midi-controller', 'home-studio', 'beginner-guide', 'professional-gear', 'budget-friendly', 'vintage', 'reviews'].map((tag) => (
                  <Link key={tag} href={`/blog/tag/${tag}`}>
                    <span className="inline-block px-3 py-1 text-xs font-medium text-gray-600 bg-gray-100 rounded-full hover:bg-gray-200 cursor-pointer transition-colors">
                      #{tag.replace('-', ' ')}
                    </span>
                  </Link>
                ))}
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BlogHomepage;