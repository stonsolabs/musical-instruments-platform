import { GetServerSideProps } from 'next';

// This component is never rendered, it just generates the blog sitemap
function BlogSitemap() {
  return null;
}

export const getServerSideProps: GetServerSideProps = async ({ res }) => {
  const baseUrl = 'https://www.getyourmusicgear.com';
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://getyourmusicgear-api.azurewebsites.net';
  
  try {
    // Fetch all published blog posts
    const response = await fetch(`${API_BASE}/api/v1/blog/posts?limit=1000&status=published`);
    const blogPosts = response.ok ? await response.json() : [];
    
    const blogPages = [
      '/blog',
      // Add individual blog post URLs
      ...blogPosts.map((post: any) => `/blog/${post.slug}`)
    ];

    const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>${baseUrl}/blog</loc>
    <lastmod>${new Date().toISOString()}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>
  ${blogPosts
    .map((post: any) => {
      const lastmod = post.updated_at || post.published_at || post.created_at || new Date().toISOString();
      return `
    <url>
      <loc>${baseUrl}/blog/${post.slug}</loc>
      <lastmod>${lastmod}</lastmod>
      <changefreq>weekly</changefreq>
      <priority>0.8</priority>
    </url>`;
    })
    .join('')}
</urlset>`;

    res.setHeader('Content-Type', 'text/xml');
    res.setHeader('Cache-Control', 'public, s-maxage=86400, stale-while-revalidate');
    res.write(sitemap);
    res.end();

    return {
      props: {},
    };
  } catch (error) {
    console.error('Error generating blog sitemap:', error);
    
    const fallbackSitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>${baseUrl}/blog</loc>
    <lastmod>${new Date().toISOString()}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>`;

    res.setHeader('Content-Type', 'text/xml');
    res.setHeader('Cache-Control', 'public, s-maxage=86400, stale-while-revalidate');
    res.write(fallbackSitemap);
    res.end();

    return {
      props: {},
    };
  }
};

export default BlogSitemap;