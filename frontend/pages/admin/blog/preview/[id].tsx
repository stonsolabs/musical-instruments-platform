import React from 'react';
import Head from 'next/head';
import { GetServerSideProps } from 'next';
import BlogProductShowcase from '../../../../src/components/BlogProductShowcase';
import { AIBlogPost } from '../../../../src/types/blog';

interface PreviewProps {
  post: AIBlogPost;
}

const PROXY_BASE = '/api/proxy/v1';

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

        {/* Structured sections if present */}
        {Array.isArray((post as any).structured_content?.sections) && (post as any).structured_content.sections.length > 0 ? (
          <div className="space-y-10 mb-12">
            {(post as any).structured_content.sections.map((sec: any, idx: number) => (
              <section key={idx} className="prose prose-lg max-w-none">
                {sec.title && <h2 className="mt-0">{sec.title}</h2>}
                {sec.content && (
                  <div
                    dangerouslySetInnerHTML={{ __html: String(sec.content).replace(/\n/g, '<br />') }}
                    className="text-gray-800 leading-relaxed"
                  />
                )}
              </section>
            ))}
          </div>
        ) : (
          <div className="prose prose-lg max-w-none mb-12">
            <div
              dangerouslySetInnerHTML={{ __html: (post.content || '').replace(/\n/g, '<br />') }}
              className="text-gray-800 leading-relaxed"
            />
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
      </article>
    </>
  );
}

export const getServerSideProps: GetServerSideProps = async ({ params }) => {
  try {
    const { id } = params!;
    const response = await fetch(`${PROXY_BASE}/blog/ai-posts/${id}`);
    if (!response.ok) {
      return { notFound: true };
    }
    const post = await response.json();
    return { props: { post } };
  } catch (e) {
    return { notFound: true };
  }
};
        {/* Inspector */}
        {(post as any).structured_content && (
          <details className="mt-6 mb-12">
            <summary className="cursor-pointer text-sm text-gray-600">View structured JSON</summary>
            <pre className="mt-3 p-3 bg-gray-50 text-xs overflow-auto rounded border">
              {JSON.stringify((post as any).structured_content, null, 2)}
            </pre>
          </details>
        )}
