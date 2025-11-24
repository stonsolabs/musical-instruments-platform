/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable SSR by default
  reactStrictMode: true,
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'images.unsplash.com' },
      { protocol: 'https', hostname: 'via.placeholder.com' },
      { protocol: 'https', hostname: 'getyourmusicgear.blob.core.windows.net' },
      { protocol: 'https', hostname: 'www.travelerguitar.com' },
    ],
    formats: ['image/webp', 'image/avif'],
    minimumCacheTTL: 31536000, // 1 year cache
  },
  // Enable static optimization where possible
  trailingSlash: false,
  poweredByHeader: false,
  compress: true,
  generateEtags: true,
  async redirects() {
    return [
      // Redirect trailing slash URLs to non-trailing slash (301 permanent redirect)
      // This ensures consistency since trailingSlash is set to false
      {
        source: '/blog/:slug/',
        destination: '/blog/:slug',
        permanent: true,
      },
      {
        source: '/products/:slug/',
        destination: '/products/:slug',
        permanent: true,
      },
      // Redirect old URLs to new URLs (if they were previously used)
      {
        source: '/about',
        destination: '/',
        permanent: true,
      },
      {
        source: '/privacy-policy',
        destination: '/privacy',
        permanent: true,
      },
      {
        source: '/terms-of-service',
        destination: '/terms',
        permanent: true,
      },
    ];
  },
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
        ],
      },
      {
        source: '/(.*).(jpg|jpeg|png|gif|ico|svg|webp)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
    ];
  },
}

module.exports = nextConfig
