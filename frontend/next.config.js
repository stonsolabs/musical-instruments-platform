/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  experimental: {
    serverComponentsExternalPackages: []
  },
  
  // Webpack optimizations for build reliability
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    // Improve module resolution
    config.resolve.fallback = {
      ...config.resolve.fallback,
      fs: false,
      path: false,
      os: false,
    };

    // Optimize for production builds
    if (!dev && !isServer) {
      config.resolve.alias = {
        ...config.resolve.alias,
        'react/jsx-runtime.js': 'react/jsx-runtime',
        'react/jsx-dev-runtime.js': 'react/jsx-dev-runtime',
      };
    }

    // Fix case sensitivity issues
    config.resolve.plugins = config.resolve.plugins || [];
    
    return config;
  },

  // Improved compiler options
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production' ? {
      exclude: ['error']
    } : false,
  },

  // Build performance optimizations
  onDemandEntries: {
    maxInactiveAge: 25 * 1000,
    pagesBufferLength: 2,
  },

  images: {
    domains: [
      'example.com',
      'images.unsplash.com',
      'thomann.de',
      'gear4music.com',
      'amazon.es',
      'kytary.de',
      'getyourmusicgear.com'
    ],
    unoptimized: process.env.NODE_ENV === 'production'
  },

  // Generate source maps for better debugging
  productionBrowserSourceMaps: false,

  async rewrites() {
    return [
      {
        source: '/sitemap.xml',
        destination: '/api/sitemap',
      },
    ];
  },

  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
        ],
      },
    ];
  },

  // Error handling
  eslint: {
    ignoreDuringBuilds: false,
  },
  typescript: {
    ignoreBuildErrors: false,
  },
};

module.exports = nextConfig;
