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
  showMeta = true 
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

  return (
    <article className={`bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300 ${sizeClasses[size]}`}>
      {/* Featured Image */}
      {safePost.featured_image && (
        <div className={`relative ${imageClasses[size]} overflow-hidden`}>
          <Link href={`/blog/${safePost.slug}`}>
            <img
              src={safePost.featured_image}
              alt={safePost.title}
              className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
            />
          </Link>
          
          {/* Category Badge */}
          {showCategory && safePost.category && (
            <div className="absolute top-4 left-4">
              <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getCategoryColorClass(safePost.category.slug)}`}>
                {safePost.category.icon && (
                  <span className="mr-1">{safePost.category.icon}</span>
                )}
                {safePost.category.name}
              </span>
            </div>
          )}
          
          {/* Featured Badge */}
          {safePost.featured && (
            <div className="absolute top-4 right-4">
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
                Featured
              </span>
            </div>
          )}
        </div>
      )}

      {/* Content */}
      <div className="p-6">
        {/* Category (if no image) */}
        {showCategory && !safePost.featured_image && safePost.category && (
          <div className="mb-3">
            <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getCategoryColorClass(safePost.category.slug)}`}>
              {safePost.category.icon && (
                <span className="mr-1">{safePost.category.icon}</span>
              )}
              {safePost.category.name}
            </span>
          </div>
        )}

        {/* Title */}
        <h3 className={`font-bold text-gray-900 mb-3 line-clamp-2 hover:text-brand-primary transition-colors ${titleClasses[size]}`}>
          <Link href={`/blog/${safePost.slug}`}>
            {safePost.title}
          </Link>
        </h3>

        {/* Excerpt */}
        {showExcerpt && safePost.excerpt && (
          <p className="text-gray-600 mb-4 line-clamp-3">
            {safePost.excerpt}
          </p>
        )}

        {/* Tags */}
        {safePost.tags && safePost.tags.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-4">
            {safePost.tags.slice(0, 3).map((tag) => (
              <Link
                key={tag.id}
                href={`/blog?tag=${tag.slug}`}
                className="inline-block px-2 py-1 text-xs font-medium text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors"
              >
                #{tag.name}
              </Link>
            ))}
            {safePost.tags.length > 3 && (
              <span className="text-xs text-gray-500">
                +{safePost.tags.length - 3} more
              </span>
            )}
          </div>
        )}

        {/* Meta Information */}
        {showMeta && (
          <div className="flex items-center justify-between text-sm text-gray-500">
            <div className="flex items-center space-x-4">
              <span>{safePost.author_name}</span>
              
              {safePost.reading_time && (
                <div className="flex items-center space-x-1">
                  <ClockIcon className="w-4 h-4" />
                  <span>{safePost.reading_time} min read</span>
                </div>
              )}
              
              <div className="flex items-center space-x-1">
                <EyeIcon className="w-4 h-4" />
                <span>{safePost.view_count}</span>
              </div>
            </div>

            <div className="text-xs">
              {safePost.published_at && new Date(safePost.published_at).toLocaleDateString()}
            </div>
          </div>
        )}

        {/* Read More Link */}
        <div className="mt-4 pt-4 border-t border-gray-100">
          <Link
            href={`/blog/${safePost.slug}`}
            className="inline-flex items-center text-brand-primary hover:text-brand-dark font-medium transition-colors"
          >
            Read More
            <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </Link>
        </div>
      </div>
    </article>
  );
}
