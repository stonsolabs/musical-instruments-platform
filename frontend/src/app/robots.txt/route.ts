import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://getyourmusicgear.com';
  
  const robotsTxt = `User-agent: *
Allow: /

# Disallow admin and private paths
Disallow: /api/
Disallow: /admin/
Disallow: /_next/
Disallow: /private/

# Allow important pages
Allow: /api/sitemap

# Sitemap
Sitemap: ${baseUrl}/sitemap.xml

# Crawl-delay for respectful crawling
Crawl-delay: 1`;

  return new NextResponse(robotsTxt, {
    headers: {
      'Content-Type': 'text/plain',
      'Cache-Control': 'public, max-age=86400, s-maxage=86400'
    },
  });
}