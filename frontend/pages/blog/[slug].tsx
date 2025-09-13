import React from 'react';
import Head from 'next/head';
import { GetServerSideProps } from 'next';
import BlogProductShowcase from '../../src/components/BlogProductShowcase';
import { BlogPost } from '../../src/types/blog';
import { ClockIcon, EyeIcon, CalendarIcon } from '@heroicons/react/24/outline';
import { ShareIcon } from '@heroicons/react/24/solid';

interface BlogPostPageProps {
  post: BlogPost;
}

const PROXY_BASE = '/api/proxy/v1';

const categoryColors = {
  'buying-guide': 'bg-blue-100 text-blue-800 border-blue-200',
  'reviews': 'bg-green-100 text-green-800 border-green-200', 
  'tutorial': 'bg-yellow-100 text-yellow-800 border-yellow-200',
  'history': 'bg-purple-100 text-purple-800 border-purple-200',
  'default': 'bg-gray-100 text-gray-800 border-gray-200'
};

const getCategoryColorClass = (categorySlug?: string) => {
  if (!categorySlug) return categoryColors.default;
  return categoryColors[categorySlug as keyof typeof categoryColors] || categoryColors.default;
};

export default function BlogPostPage({ post }: BlogPostPageProps) {
  const origin = typeof window !== 'undefined' ? window.location.origin : (process.env.NEXT_PUBLIC_APP_ORIGIN || 'https://www.getyourmusicgear.com');
  const canonicalUrl = `${origin}/blog/${post.slug}`;
  const shareUrl = canonicalUrl;
  
  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: post.title,
          text: post.excerpt || '',
          url: shareUrl,
        });
      } catch (err) {
        // ignore share errors in non-supporting environments
      }
    } else {
      // Fallback: copy to clipboard
      if (navigator.clipboard) {
        await navigator.clipboard.writeText(shareUrl);
        alert('Link copied to clipboard!');
      }
    }
  };

  return (
    <>
      <Head>
        <title>{post.seo_title || post.title} - GetYourMusicGear</title>
        <meta 
          name="description" 
          content={post.seo_description || post.excerpt || `Read our ${post.category?.name.toLowerCase()} about ${post.title}`}
        />
        <link rel="canonical" href={canonicalUrl} />
        <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
        <meta property="og:title" content={post.title} />
        <meta property="og:description" content={post.excerpt || ''} />
        {post.featured_image && (
          <meta property="og:image" content={post.featured_image} />
        )}
        <meta property="og:type" content="article" />
        <meta property="og:url" content={canonicalUrl} />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content={post.title} />
        <meta name="twitter:description" content={post.excerpt || ''} />
        {post.featured_image && <meta name="twitter:image" content={post.featured_image} />}
        {post.published_at && (
          <meta property="article:published_time" content={post.published_at} />
        )}
        {post.category && (
          <meta property="article:section" content={post.category.name} />
        )}
        {post.tags.map((tag) => (
          <meta key={tag.id} property="article:tag" content={tag.name} />
        ))}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              '@context': 'https://schema.org',
              '@type': 'BlogPosting',
              headline: post.seo_title || post.title,
              description: post.seo_description || post.excerpt || undefined,
              image: post.featured_image || undefined,
              author: { '@type': 'Person', name: post.author_name || 'GetYourMusicGear Team' },
              publisher: { '@type': 'Organization', name: 'GetYourMusicGear', logo: { '@type': 'ImageObject', url: `${origin}/logo.png` } },
              datePublished: post.published_at || undefined,
              dateModified: post.updated_at || undefined,
              mainEntityOfPage: canonicalUrl,
              keywords: post.tags?.map(t => t.name).join(', '),
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
                { '@type': 'ListItem', position: 2, name: 'Blog', item: `${origin}/blog` },
                ...(post.category ? [{ '@type': 'ListItem', position: 3, name: post.category.name, item: `${origin}/blog?category=${post.category.slug}` }] : []),
                { '@type': 'ListItem', position: post.category ? 4 : 3, name: post.title, item: canonicalUrl },
              ],
            }),
          }}
        />
      </Head>

      <article className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Article Header */}
        <header className="mb-8">
          {/* Category Badge */}
          {post.category && (
            <div className="mb-4">
              <span className={`inline-flex items-center px-4 py-2 rounded-full text-sm font-medium border ${getCategoryColorClass(post.category.slug)}`}>
                {post.category.icon && (
                  <span className="mr-2">{post.category.icon}</span>
                )}
                {post.category.name}
              </span>
            </div>
          )}

          {/* Title */}
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 leading-tight mb-6">
            {post.title}
          </h1>

          {/* Meta Information */}
          <div className="flex flex-wrap items-center gap-6 text-sm text-gray-600 mb-6">
            <span className="font-medium">{post.author_name}</span>
            
            {post.published_at && (
              <div className="flex items-center space-x-1">
                <CalendarIcon className="w-4 h-4" />
                <span>{new Date(post.published_at).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'long', 
                  day: 'numeric'
                })}</span>
              </div>
            )}
            
            {post.reading_time && (
              <div className="flex items-center space-x-1">
                <ClockIcon className="w-4 h-4" />
                <span>{post.reading_time} min read</span>
              </div>
            )}
            
            <div className="flex items-center space-x-1">
              <EyeIcon className="w-4 h-4" />
              <span>{post.view_count} views</span>
            </div>
          </div>

          {/* Featured Image */}
          {post.featured_image && (
            <div className="relative h-64 md:h-96 bg-gray-100 rounded-lg overflow-hidden mb-8">
              <img
                src={post.featured_image}
                alt={post.title}
                className="w-full h-full object-cover"
              />
            </div>
          )}

          {/* Excerpt */}
          {post.excerpt && (
            <div className="text-xl text-gray-700 leading-relaxed mb-8 p-6 bg-gray-50 rounded-lg border-l-4 border-brand-primary">
              {post.excerpt}
            </div>
          )}

          {/* Share Button */}
          <div className="flex justify-between items-center pb-6 border-b border-gray-200">
            <div className="flex flex-wrap gap-2">
              {post.tags.map((tag) => (
                <a
                  key={tag.id}
                  href={`/blog?tag=${tag.slug}`}
                  className="inline-block px-3 py-1 text-sm font-medium text-gray-600 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors"
                >
                  #{tag.name}
                </a>
              ))}
            </div>
            
            <button
              onClick={handleShare}
              className="flex items-center space-x-2 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
            >
              <ShareIcon className="w-4 h-4" />
              <span>Share</span>
            </button>
          </div>
        </header>

        {/* Article Content */}
        <div className="prose prose-lg max-w-none mb-12">
          <div 
            dangerouslySetInnerHTML={{ __html: post.content.replace(/\n/g, '<br />') }}
            className="text-gray-800 leading-relaxed"
          />
        </div>

        {/* Featured Products */}
        {post.products && post.products.length > 0 && (
          <div className="mb-12 p-8 bg-gray-50 rounded-lg">
            <BlogProductShowcase
              products={post.products}
              title="Products Featured in This Article"
              layout="grid"
              showAffiliateButtons={true}
            />
          </div>
        )}

        {/* Article Footer */}
        <footer className="border-t border-gray-200 pt-8">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">About the Author</h3>
              <p className="text-gray-600">
                Written by {post.author_name}, part of the GetYourMusicGear expert team.
              </p>
            </div>
            
            <div className="text-center">
              <button
                onClick={handleShare}
                className="inline-flex items-center space-x-2 px-6 py-3 bg-brand-primary text-white font-medium rounded-lg hover:bg-brand-dark transition-colors"
              >
                <ShareIcon className="w-5 h-5" />
                <span>Share This Article</span>
              </button>
            </div>
          </div>

          {/* Back to Blog */}
          <div className="mt-8 text-center">
            <a
              href="/blog"
              className="inline-flex items-center text-brand-primary hover:text-brand-dark font-medium transition-colors"
            >
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Back to Blog
            </a>
          </div>
        </footer>
      </article>
    </>
  );
}

export const getServerSideProps: GetServerSideProps = async ({ params }) => {
  try {
    const { slug } = params!;
    
    const response = await fetch(`${PROXY_BASE}/blog/posts/${slug}`);
    
    if (!response.ok) {
      if (response.status === 404) {
        return {
          notFound: true,
        };
      }
      throw new Error('Failed to fetch blog post');
    }
    
    const post = await response.json();
    
    return {
      props: {
        post,
      },
    };
  } catch (error) {
    console.error('Error fetching blog post:', error);
    return {
      notFound: true,
    };
  }
};
