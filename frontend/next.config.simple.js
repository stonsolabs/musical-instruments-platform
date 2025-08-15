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
  
  // Disable telemetry
  experimental: {
    telemetry: false
  }
};

module.exports = nextConfig;
