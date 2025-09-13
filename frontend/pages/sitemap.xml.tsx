import { GetServerSideProps } from 'next';
import { fetchProducts, fetchCategories } from '../src/lib/api';

// This component is never rendered, it just generates the sitemap
function Sitemap() {
  return null;
}

export const getServerSideProps: GetServerSideProps = async ({ res }) => {
  const baseUrl = 'https://www.getyourmusicgear.com';
  
  // Static pages (define outside try block so it's accessible in catch)
  const staticPages = [
    '',
    '/products',
    '/compare',
    '/blog',
    '/about',
    '/contact',
    '/privacy-policy',
    '/terms-of-service',
  ];
  
  try {
    // Fetch data for dynamic pages
    const [productsData, categories] = await Promise.all([
      fetchProducts({ limit: 1000 }), // Get all products
      fetchCategories()
    ]);

    // Generate sitemap XML
    const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  ${staticPages
    .map(page => {
      return `
    <url>
      <loc>${baseUrl}${page}</loc>
      <lastmod>${new Date().toISOString()}</lastmod>
      <changefreq>${page === '' ? 'daily' : page === '/products' ? 'daily' : 'weekly'}</changefreq>
      <priority>${page === '' ? '1.0' : page === '/products' ? '0.9' : '0.8'}</priority>
    </url>`;
    })
    .join('')}
  ${productsData.products
    .map(product => {
      return `
    <url>
      <loc>${baseUrl}/products/${product.slug}</loc>
      <lastmod>${new Date().toISOString()}</lastmod>
      <changefreq>weekly</changefreq>
      <priority>0.7</priority>
    </url>`;
    })
    .join('')}
  ${categories
    .filter(cat => cat.is_active)
    .map(category => {
      return `
    <url>
      <loc>${baseUrl}/products?category=${category.slug}</loc>
      <lastmod>${new Date().toISOString()}</lastmod>
      <changefreq>daily</changefreq>
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
    console.error('Error generating sitemap:', error);
    
    // Fallback sitemap with just static pages
    const fallbackSitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  ${staticPages
    .map(page => {
      return `
    <url>
      <loc>${baseUrl}${page}</loc>
      <lastmod>${new Date().toISOString()}</lastmod>
      <changefreq>weekly</changefreq>
      <priority>0.8</priority>
    </url>`;
    })
    .join('')}
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

export default Sitemap;