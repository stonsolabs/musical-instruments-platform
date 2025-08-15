/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  
  // Minimal configuration for reliable builds
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  
  // Basic image optimization
  images: {
    unoptimized: true
  },
  
  // API routing handled by nginx reverse proxy
  
  // Webpack configuration for path resolution
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': require('path').resolve(__dirname, './src'),
    };
    return config;
  }
};

module.exports = nextConfig;
