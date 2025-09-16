import React from 'react';
import Link from 'next/link';
import { BlogPost, BlogPostSummary, BlogCategory } from '../types/blog';
import { ClockIcon, EyeIcon } from '@heroicons/react/24/outline';

interface BlogPostCardProps {
  post: BlogPost | BlogPostSummary;
  size?: 'small' | 'medium' | 'large';
  showExcerpt?: boolean;
  showCategory?: boolean;
  showMeta?: boolean;
  hrefOverride?: string;
}

const categoryColors = {
  'buying-guide': 'bg-blue-100 text-blue-800',
  'reviews': 'bg-green-100 text-green-800', 
  'tutorial': 'bg-yellow-100 text-yellow-800',
  'history': 'bg-purple-100 text-purple-800',
  'default': 'bg-gray-100 text-gray-800'
};

const getCategoryColorClass = (categorySlug?: string) => {
  if (!categorySlug) return categoryColors.default;
  return categoryColors[categorySlug as keyof typeof categoryColors] || categoryColors.default;
};

export default function BlogPostCard({ 
  post, 
  size = 'medium', 
  showExcerpt = true, 
  showCategory = true,
  showMeta = true,
  hrefOverride,
}: BlogPostCardProps) {
  const sizeClasses = {
    small: 'max-w-sm',
    medium: 'max-w-md',
    large: 'max-w-2xl'
  };

  const imageClasses = {
    small: 'h-40',
    medium: 'h-48',
    large: 'h-64'
  };

  const titleClasses = {
    small: 'text-lg',
    medium: 'text-xl',
    large: 'text-2xl'
  };

  // Ensure post has required properties with defaults
  const safePost = {
    ...post,
    tags: post.tags || [],
    view_count: post.view_count || 0,
  };
  const href = hrefOverride || `/blog/${safePost.slug}`;

  return (
    <article className={`bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-all duration-300 hover:-translate-y-2 group ${sizeClasses[size]}`}>
      {/* Featured Image */}
      {safePost.featured_image && (
        <div className={`relative ${imageClasses[size]} overflow-hidden`}>
          <Link href={href}>
            <img
              src={safePost.featured_image}
              alt={safePost.title}
              className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
            />
          </Link>
          
          {/* Gradient Overlay */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
          
          {/* Category Badge */}
          {showCategory && safePost.category && (
            <div className="absolute top-4 left-4">
              <span className={`inline-flex items-center px-3 py-2 rounded-xl text-sm font-semibold backdrop-blur-sm border border-white/20 shadow-lg ${getCategoryColorClass(safePost.category.slug)}`}>
                {safePost.category.icon && (
                  <span className="mr-2 text-lg">{safePost.category.icon}</span>
                )}
                {safePost.category.name}
              </span>
            </div>
          )}
          
          {/* Featured Badge */}
          {safePost.featured && (
            <div className="absolute top-4 right-4">
              <span className="inline-flex items-center px-3 py-2 rounded-xl text-xs font-bold bg-gradient-to-r from-red-500 to-pink-500 text-white shadow-lg">
                ✨ Featured
              </span>
            </div>
          )}
          
          {/* Quick Action Button */}
          <div className="absolute bottom-4 right-4 opacity-0 group-hover:opacity-100 transition-all duration-300 transform translate-y-2 group-hover:translate-y-0">
            <Link href={href} className="inline-flex items-center px-4 py-2 bg-white/90 backdrop-blur-sm rounded-lg text-gray-900 font-medium shadow-lg hover:bg-white transition-colors">
              Read Now
              <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </Link>
          </div>
        </div>
      )}

      {/* Content */}
      <div className="p-6">
        {/* Category (if no image) */}
        {showCategory && !safePost.featured_image && safePost.category && (
          <div className="mb-4">
            <span className={`inline-flex items-center px-4 py-2 rounded-xl text-sm font-semibold ${getCategoryColorClass(safePost.category.slug)}`}>
              {safePost.category.icon && (
                <span className="mr-2 text-lg">{safePost.category.icon}</span>
              )}
              {safePost.category.name}
            </span>
          </div>
        )}

        {/* Title */}
        <h3 className={`font-bold text-gray-900 mb-4 line-clamp-2 group-hover:text-brand-primary transition-colors leading-tight ${titleClasses[size]}`}>
          <Link href={href}>
            {safePost.title}
          </Link>
        </h3>

        {/* Excerpt */}
        {showExcerpt && safePost.excerpt && (
          <p className="text-gray-600 mb-5 line-clamp-3 leading-relaxed">
            {safePost.excerpt}
          </p>
        )}

        {/* Tags */}
        {safePost.tags && safePost.tags.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-5">
            {safePost.tags.slice(0, 3).map((tag) => (
              <Link
                key={tag.id}
                href={`/blog?tag=${tag.slug}`}
                className="inline-block px-3 py-1 text-xs font-medium text-brand-primary bg-brand-primary/10 rounded-lg hover:bg-brand-primary/20 transition-colors"
              >
                #{tag.name}
              </Link>
            ))}
            {safePost.tags.length > 3 && (
              <span className="inline-flex items-center px-2 py-1 text-xs text-gray-500 bg-gray-100 rounded-lg">
                +{safePost.tags.length - 3} more
              </span>
            )}
          </div>
        )}

        {/* Meta Information */}
        {showMeta && (
          <div className="flex items-center justify-between text-sm mb-5">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <img 
                  src={`https://ui-avatars.com/api/?name=${encodeURIComponent(safePost.author_name)}&background=0D8ABC&color=fff&size=32`} 
                  alt={safePost.author_name} 
                  className="w-8 h-8 rounded-full" 
                />
                <span className="font-medium text-gray-700">{safePost.author_name}</span>
              </div>
              
              {safePost.reading_time && (
                <div className="flex items-center gap-1 text-gray-500">
                  <ClockIcon className="w-4 h-4" />
                  <span>{safePost.reading_time} min</span>
                </div>
              )}
              
              <div className="flex items-center gap-1 text-gray-500">
                <EyeIcon className="w-4 h-4" />
                <span>{safePost.view_count}</span>
              </div>
            </div>

            <div className="text-xs text-gray-500">
              {safePost.published_at && new Date(safePost.published_at).toLocaleDateString()}
            </div>
          </div>
        )}

        {/* Read More Link */}
        <div className="pt-4 border-t border-gray-100">
          <Link
            href={href}
            className="inline-flex items-center w-full justify-center px-4 py-3 bg-gradient-to-r from-brand-primary to-brand-dark text-white font-semibold rounded-xl hover:shadow-lg transition-all duration-300 transform hover:-translate-y-0.5"
          >
            Read Full Article
            <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </Link>
        </div>
      </div>
    </article>
  );
}
