/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable SSR by default
  reactStrictMode: true,
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'images.unsplash.com' },
      { protocol: 'https', hostname: 'via.placeholder.com' },
    ],
    formats: ['image/webp', 'image/avif'],
  },
  // Enable static optimization where possible
  trailingSlash: false,
  poweredByHeader: false,
}

module.exports = nextConfig
