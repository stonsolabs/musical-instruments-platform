import React from 'react';
import Link from 'next/link';
import BlogProductShowcase from './BlogProductShowcase';

interface Product {
  id: string;
  name: string;
  slug: string;
  brand: string;
  category: string;
  price: number;
  originalPrice?: number;
  image: string;
  rating: number;
  reviewCount: number;
  affiliateUrl: string;
  features: string[];
  description: string;
  pros?: string[];
  cons?: string[];
  bestFor?: string;
  isRecommended?: boolean;
  badge?: string;
}

const demoProducts: Product[] = [
  {
    id: 'fender-player-strat',
    name: 'Fender Player Stratocaster',
    slug: 'fender-player-stratocaster',
    brand: 'Fender',
    category: 'Electric Guitar',
    price: 699,
    originalPrice: 799,
    image: '/product-images/fender_player_strat_sss_1.jpg',
    rating: 4.8,
    reviewCount: 1247,
    affiliateUrl: 'https://amazon.com/dp/B07C7V3V8L',
    features: [
      'Three single-coil pickups',
      'Comfortable C-shaped neck',
      'Reliable tuning stability',
      'Classic Stratocaster design'
    ],
    description: 'The Fender Player Stratocaster is an excellent choice for beginners who want a classic electric guitar sound with modern playability.',
    isRecommended: true,
    badge: 'Best Overall',
    pros: [
      'Excellent build quality',
      'Classic Stratocaster tone',
      'Great for beginners and pros',
      'Reliable tuning stability'
    ],
    cons: [
      'Higher price point',
      'Basic features for the price'
    ],
    bestFor: 'Guitarists who want the classic Stratocaster sound and feel'
  },
  {
    id: 'yamaha-pacifica',
    name: 'Yamaha Pacifica 112V',
    slug: 'yamaha-pacifica-112v',
    brand: 'Yamaha',
    category: 'Electric Guitar',
    price: 299,
    image: '/product-images/fender_player_strat_sss_2.jpg',
    rating: 4.7,
    reviewCount: 1563,
    affiliateUrl: 'https://amazon.com/dp/B07C7V3V8L',
    features: [
      'HSS pickup configuration',
      'Comfortable neck profile',
      'Excellent value for money',
      'Reliable hardware'
    ],
    description: 'The Yamaha Pacifica 112V is known for its exceptional build quality and playability at an affordable price.',
    badge: 'Best Value',
    pros: [
      'Exceptional value for money',
      'Great build quality',
      'Versatile HSS configuration',
      'Perfect for beginners'
    ],
    cons: [
      'Basic electronics',
      'Limited color options'
    ],
    bestFor: 'Beginners and budget-conscious players'
  },
  {
    id: 'focusrite-scarlett-2i2',
    name: 'Focusrite Scarlett 2i2',
    slug: 'focusrite-scarlett-2i2',
    brand: 'Focusrite',
    category: 'Audio Interface',
    price: 169,
    image: '/product-images/focusrite_scarlett_2i2_3rd_1.jpg',
    rating: 4.8,
    reviewCount: 3247,
    affiliateUrl: 'https://amazon.com/dp/B07C7V3V8L',
    features: [
      '2 inputs, 2 outputs',
      'USB-C connectivity',
      'High-quality preamps',
      'Direct monitoring'
    ],
    description: 'The Focusrite Scarlett 2i2 is the perfect audio interface for home recording.',
    pros: [
      'Excellent sound quality',
      'Easy to use',
      'Great value for money',
      'Reliable performance'
    ],
    cons: [
      'Limited inputs',
      'No MIDI ports'
    ],
    bestFor: 'Home recording beginners and intermediate users'
  }
];

export default function BlogStyleDemo() {
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Blog Post Style Showcase</h1>
          <p className="text-xl text-gray-600">Explore different blog post layouts and product showcase styles</p>
        </div>

        {/* Style Navigation */}
        <div className="flex flex-wrap justify-center gap-4 mb-12">
          <Link
            href="/blog/best-electric-guitars-beginners-2025"
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Buying Guide Style
          </Link>
          <Link
            href="/blog/how-choose-right-digital-piano"
            className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            Comparison Style
          </Link>
          <Link
            href="/blog/top-10-studio-monitors-under-500"
            className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
          >
            Review Style
          </Link>
          <Link
            href="/blog/essential-home-recording-equipment"
            className="px-6 py-3 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-colors"
          >
            Tutorial Style
          </Link>
        </div>

        {/* Product Showcase Styles */}
        <div className="space-y-16">
          {/* Featured Style */}
          <section>
            <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Featured Product Showcase</h2>
            <BlogProductShowcase
              products={demoProducts}
              style="featured"
              title="Featured Products"
              subtitle="Beautiful showcase with recommended product and alternatives"
            />
          </section>

          {/* Grid Style */}
          <section>
            <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Grid Product Showcase</h2>
            <BlogProductShowcase
              products={demoProducts}
              style="grid"
              title="Product Grid"
              subtitle="Clean grid layout for multiple products"
            />
          </section>

          {/* Carousel Style */}
          <section>
            <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Carousel Product Showcase</h2>
            <BlogProductShowcase
              products={demoProducts}
              style="carousel"
              title="Product Carousel"
              subtitle="Horizontal scroll for mobile-friendly browsing"
            />
          </section>

          {/* Recommended Style */}
          <section>
            <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Recommended Product Showcase</h2>
            <BlogProductShowcase
              products={demoProducts}
              style="recommended"
              title="Our Top Recommendation"
              subtitle="Single recommended product with alternatives"
            />
          </section>
        </div>

        {/* Blog Post Examples */}
        <div className="mt-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Blog Post Examples</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              {
                title: "Best Electric Guitars for Beginners",
                excerpt: "Comprehensive guide to choosing your first electric guitar",
                href: "/blog/best-electric-guitars-beginners-2025",
                style: "buying-guide",
                color: "blue"
              },
              {
                title: "Digital Piano Comparison",
                excerpt: "Compare the top digital pianos side by side",
                href: "/blog/how-choose-right-digital-piano",
                style: "comparison",
                color: "green"
              },
              {
                title: "Studio Monitor Reviews",
                excerpt: "In-depth reviews of budget studio monitors",
                href: "/blog/top-10-studio-monitors-under-500",
                style: "review",
                color: "purple"
              },
              {
                title: "Home Recording Setup",
                excerpt: "Step-by-step tutorial for home recording",
                href: "/blog/essential-home-recording-equipment",
                style: "tutorial",
                color: "orange"
              }
            ].map((post) => (
              <Link
                key={post.href}
                href={post.href}
                className={`block bg-white rounded-xl shadow-lg border border-gray-200 p-6 hover:shadow-xl transition-shadow`}
              >
                <div className={`w-12 h-12 bg-${post.color}-600 rounded-lg mb-4 flex items-center justify-center`}>
                  <span className="text-white font-bold text-lg">
                    {post.style === 'buying-guide' ? '🛒' : 
                     post.style === 'comparison' ? '⚖️' : 
                     post.style === 'review' ? '⭐' : '📚'}
                  </span>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">{post.title}</h3>
                <p className="text-gray-600 mb-4">{post.excerpt}</p>
                <span className={`inline-block px-3 py-1 bg-${post.color}-100 text-${post.color}-800 rounded-full text-sm font-medium capitalize`}>
                  {post.style.replace('-', ' ')}
                </span>
              </Link>
            ))}
          </div>
        </div>

        {/* Features Overview */}
        <div className="mt-16 bg-white rounded-xl shadow-lg border border-gray-200 p-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Key Features</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                title: "Multiple Blog Styles",
                description: "5 different blog post layouts: Buying Guide, Comparison, Review, Tutorial, and News",
                icon: "📝"
              },
              {
                title: "Product Showcases",
                description: "4 beautiful product showcase styles: Featured, Grid, Carousel, and Recommended",
                icon: "🎯"
              },
              {
                title: "Affiliate Integration",
                description: "Seamless affiliate link integration with proper disclosure and tracking",
                icon: "🔗"
              },
              {
                title: "Comparison Tables",
                description: "Interactive comparison tables for detailed product analysis",
                icon: "📊"
              },
              {
                title: "Responsive Design",
                description: "Mobile-friendly layouts that work perfectly on all devices",
                icon: "📱"
              },
              {
                title: "SEO Optimized",
                description: "Built-in SEO features with proper metadata and structured data",
                icon: "🔍"
              }
            ].map((feature) => (
              <div key={feature.title} className="text-center">
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
