import React from 'react';
import Head from 'next/head';
import { GetServerSideProps } from 'next';
import BlogProductShowcase from '../../src/components/BlogProductShowcase';
import SimpleBlogRenderer from '../../src/components/SimpleBlogRenderer';
import { BlogPost } from '../../src/types/blog';
import ReactMarkdown from 'react-markdown';
// @ts-ignore - optional plugin, ensure it's installed in the app
import remarkGfm from 'remark-gfm';
import ProsCons from '../../src/components/ProsCons';
import BlogComparisonTable from '../../src/components/BlogComparisonTable';
import SpecsList from '../../src/components/SpecsList';
import { ClockIcon, EyeIcon, CalendarIcon } from '@heroicons/react/24/outline';
import { ShareIcon } from '@heroicons/react/24/solid';

interface BlogPostPageProps {
  post: BlogPost;
  relatedPosts?: any[];
}

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://getyourmusicgear-api.azurewebsites.net';

const categoryColors = {
  'buying-guide': 'bg-gray-100 text-gray-800 border-gray-200',
  'review': 'bg-gray-100 text-gray-800 border-gray-200',
  'reviews': 'bg-gray-100 text-gray-800 border-gray-200', 
  'comparison': 'bg-gray-100 text-gray-800 border-gray-200',
  'artist-spotlight': 'bg-gray-100 text-gray-800 border-gray-200',
  'instrument-history': 'bg-gray-100 text-gray-800 border-gray-200',
  'gear-tips': 'bg-gray-100 text-gray-800 border-gray-200',
  'news-feature': 'bg-gray-100 text-gray-800 border-gray-200',
  'tutorial': 'bg-gray-100 text-gray-800 border-gray-200',
  'history': 'bg-gray-100 text-gray-800 border-gray-200',
  'default': 'bg-gray-100 text-gray-800 border-gray-200'
};

const getCategoryColorClass = (categorySlug?: string) => {
  if (!categorySlug) return categoryColors.default;
  return categoryColors[categorySlug as keyof typeof categoryColors] || categoryColors.default;
};

export default function BlogPostPage({ post, relatedPosts = [] }: BlogPostPageProps) {
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
        <meta name="robots" content={post.noindex ? 'noindex, nofollow' : 'index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1'} />
        <meta property="og:site_name" content="GetYourMusicGear" />
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
              author: { '@type': 'Person', name: post.author_name || 'GetYourMusicGear Team', url: `${origin}/about`, image: `${origin}/logo.png` },
              publisher: { '@type': 'Organization', name: 'GetYourMusicGear', logo: { '@type': 'ImageObject', url: `${origin}/logo.png` } },
              datePublished: post.published_at || undefined,
              dateModified: post.updated_at || undefined,
              mainEntityOfPage: canonicalUrl,
              keywords: post.tags?.map(t => t.name).join(', '),
              articleSection: post.category?.name || undefined,
              wordCount: (() => {
                try {
                  const text = (post as any).content_json?.sections?.map((s:any)=>s.content||'').join(' ') || post.content || '';
                  return String(text.split(/\s+/).filter(Boolean).length);
                } catch { return undefined; }
              })(),
            }),
          }}
        />
        {(post as any).content_json?.faqs && Array.isArray((post as any).content_json.faqs) && (
          <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{
              __html: JSON.stringify({
                '@context': 'https://schema.org',
                '@type': 'FAQPage',
                mainEntity: (post as any).content_json.faqs.map((f:any)=>({
                  '@type': 'Question',
                  name: f.q || f.question,
                  acceptedAnswer: { '@type': 'Answer', text: f.a || f.answer }
                }))
              })
            }}
          />
        )}
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
          <h1 className="text-3xl md:text-4xl lg:text-5xl font-black text-gray-900 leading-tight mb-6" style={{fontFamily: 'Montserrat, sans-serif'}}>
            {post.title}
          </h1>

          {/* Author Box */}
          <div className="flex flex-wrap items-center gap-6 text-sm text-gray-600 mb-6">
            <div className="flex items-center gap-3">
              <img src={`https://ui-avatars.com/api/?name=${encodeURIComponent(post.author_name || 'GetYourMusicGear Team')}&background=0D8ABC&color=fff`} alt={post.author_name || 'GetYourMusicGear Team'} className="w-8 h-8 rounded-full" />
              <div className="flex items-center gap-2">
                <span className="font-medium">{post.author_name || 'GetYourMusicGear Team'}</span>
                <span className="inline-flex items-center text-xs text-green-700 bg-green-100 px-2 py-0.5 rounded">Verified</span>
              </div>
            </div>
            
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
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 mb-12">
          {/* Main content */}
          <div className="lg:col-span-8">
            {(() => {
              const hydrateMap: Record<string, any> = {};
              try {
                (post as any).products?.forEach((p: any) => {
                  const slug = p.product_slug || p.slug;
                  if (!p.product_id) return;
                  hydrateMap[String(p.product_id)] = {
                    id: p.product_id,
                    name: p.product_name || p.name,
                    slug,
                    affiliate_url: slug ? `/products/${slug}` : undefined,
                    store_url: slug ? `/products/${slug}` : undefined,
                  };
                });
              } catch {}
              return (
                <SimpleBlogRenderer 
                  content={(post as any).content_json || { sections: [{ type: 'content', content: post.content || '' }] }} 
                  hydrate={hydrateMap}
                />
              );
            })()}
          </div>
          {/* Side rail TOC */}
          <aside className="lg:col-span-4 lg:sticky lg:top-24 h-max">
            <div className="rounded-lg border bg-white p-5 shadow-sm">
              <h3 className="text-sm font-semibold text-gray-700 mb-3">On this page</h3>
              <ul className="space-y-2 text-sm">
                {Array.isArray((post as any).content_json?.sections) ? 
                  (post as any).content_json.sections.map((sec: any, idx: number) => (
                    <li key={idx}>
                      <a href={`#sec-${idx}`} className="text-gray-600 hover:text-gray-900">
                        {sec.title || `Section ${idx+1}`}
                      </a>
                    </li>
                  )) : (
                    <li>
                      <a href="#content" className="text-gray-600 hover:text-gray-900">Article Content</a>
                    </li>
                  )
                }
              </ul>
            </div>
          </aside>
        </div>

        {/* Inline spotlights preferred; hide end-of-article showcase */}

        {/* Key Takeaways */}
        {(post as any).content_json?.key_takeaways && (
          <div className="mb-12 p-6 bg-blue-50 border border-blue-200 rounded-lg">
            <h3 className="text-xl font-semibold mb-3">Key Takeaways</h3>
            <ReactMarkdown>{String((post as any).content_json.key_takeaways)}</ReactMarkdown>
          </div>
        )}

        {/* FAQs */}
        {Array.isArray((post as any).content_json?.faqs) && (post as any).content_json.faqs.length > 0 && (
          <div className="mb-12">
            <h2 className="text-2xl font-bold mb-4">Frequently Asked Questions</h2>
            <div className="space-y-3">
              {(post as any).content_json.faqs.map((f: any, idx: number) => (
                <details key={idx} className="group border rounded-md p-4 bg-white">
                  <summary className="cursor-pointer font-medium text-gray-800 group-open:text-brand-primary">{f.q || f.question}</summary>
                  <div className="mt-2 text-gray-700">
                    <ReactMarkdown>{String(f.a || f.answer || '')}</ReactMarkdown>
                  </div>
                </details>
              ))}
            </div>
          </div>
        )}

        {/* Related Posts */}
        {relatedPosts && relatedPosts.length > 0 && (
          <div className="mb-12">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Related Posts</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {relatedPosts.map((p) => (
                <a key={p.id} href={`/blog/${p.slug}`} className="block bg-white rounded-lg shadow hover:shadow-md transition-shadow overflow-hidden">
                  {p.featured_image && (
                    <img src={p.featured_image} alt={p.title} className="w-full h-40 object-cover" />
                  )}
                  <div className="p-4">
                    <h3 className="font-semibold text-gray-900">{p.title}</h3>
                    {p.excerpt && <p className="text-gray-600 text-sm mt-2">{p.excerpt}</p>}
                  </div>
                </a>
              ))}
            </div>
          </div>
        )}

        {/* Newsletter CTA */}
        <div className="mb-12 p-6 bg-gray-50 border rounded-lg">
          <h3 className="text-xl font-semibold mb-2">Get the best music gear guides in your inbox</h3>
          <p className="text-gray-600 mb-3">No spam. Just practical buying advice, tutorials, and deals.</p>
          <form action="#" onSubmit={(e)=>e.preventDefault()} className="flex gap-2">
            <input type="email" required placeholder="you@example.com" className="flex-1 px-3 py-2 border rounded" />
            <button className="px-4 py-2 bg-brand-primary text-white rounded">Subscribe</button>
          </form>
        </div>

        {/* Article Footer */}
        <footer className="border-t border-gray-200 pt-8">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">About the Author</h3>
              <p className="text-gray-600">
                Written by {post.author_name || 'GetYourMusicGear Team'}, part of the GetYourMusicGear expert team.
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
    
    const response = await fetch(`${API_BASE}/api/v1/blog/posts/${slug}`);
    
    if (!response.ok) {
      if (response.status === 404) {
        return {
          notFound: true,
        };
      }
      throw new Error('Failed to fetch blog post');
    }
    
    const post = await response.json();
    let relatedPosts: any[] = [];
    try {
      if ((post as any).category?.slug) {
        const relRes = await fetch(`${API_BASE}/api/v1/blog/posts?category=${encodeURIComponent((post as any).category.slug)}&limit=6`);
        if (relRes.ok) {
          const rel = await relRes.json();
          relatedPosts = (rel || []).filter((p: any) => p.slug !== slug).slice(0, 6);
        }
      }
    } catch {}
    
    return {
      props: {
        post,
        relatedPosts,
      },
    };
  } catch (error) {
    console.error('Error fetching blog post:', error);
    return {
      notFound: true,
    };
  }
};
