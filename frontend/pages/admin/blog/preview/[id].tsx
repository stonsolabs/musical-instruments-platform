import React from 'react';
import Head from 'next/head';
import { GetServerSideProps } from 'next';
import BlogProductShowcase from '../../../../src/components/BlogProductShowcase';
import SimpleBlogRenderer from '../../../../src/components/SimpleBlogRenderer';
import { AIBlogPost } from '../../../../src/types/blog';
import ReactMarkdown from 'react-markdown';
// @ts-ignore - optional plugin, ensure it's installed
import remarkGfm from 'remark-gfm';

interface PreviewProps {
  post: AIBlogPost;
}

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://getyourmusicgear-api.azurewebsites.net';

export default function BlogPreviewPage({ post }: PreviewProps) {
  const origin = typeof window !== 'undefined' ? window.location.origin : (process.env.NEXT_PUBLIC_APP_ORIGIN || 'https://www.getyourmusicgear.com');
  return (
    <>
      <Head>
        <title>Preview: {post.title} - GetYourMusicGear</title>
        <meta name="robots" content="noindex, nofollow" />
      </Head>
      <article className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6 p-3 rounded bg-yellow-50 border border-yellow-200 text-yellow-800 text-sm">
          Draft Preview — not publicly visible. Use Admin to publish.
        </div>

        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 leading-tight mb-3">{post.title}</h1>
        {post.excerpt && (
          <div className="text-lg text-gray-700 mb-6">{post.excerpt}</div>
        )}

        {post.featured_image && (
          <div className="relative h-64 md:h-96 bg-gray-100 rounded-lg overflow-hidden mb-8">
            <img src={post.featured_image} alt={post.title} className="w-full h-full object-cover" />
          </div>
        )}

        {/* Render using the simplified renderer when available */}
        {Boolean((post as any).content_json) ? (
          <div className="mb-12">
            <SimpleBlogRenderer content={(post as any).content_json} />
          </div>
        ) : (
          <div className="prose prose-lg lg:prose-xl max-w-none mb-12">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{post.content || ''}</ReactMarkdown>
          </div>
        )}

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

        {/* Inspector */}
        {(post as any).content_json && (
          <details className="mt-6 mb-12">
            <summary className="cursor-pointer text-sm text-gray-600">View structured JSON</summary>
            <pre className="mt-3 p-3 bg-gray-50 text-xs overflow-auto rounded border">
              {JSON.stringify((post as any).content_json, null, 2)}
            </pre>
          </details>
        )}
      </article>
    </>
  );
}

export const getServerSideProps: GetServerSideProps = async ({ params }) => {
  try {
    const { id } = params!;
    const response = await fetch(`${API_BASE}/api/v1/blog/ai-posts/${id}`);
    if (!response.ok) {
      return { notFound: true };
    }
    const post = await response.json();
    return { props: { post } };
  } catch (e) {
    return { notFound: true };
  }
};
