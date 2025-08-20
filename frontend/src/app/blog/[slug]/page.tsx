import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import BlogProductCard from '@/components/BlogProductCard';
import ProductComparisonTable from '@/components/ProductComparisonTable';

interface BlogPostPageProps {
  params: {
    slug: string;
  };
}

// Generate metadata for SEO
export async function generateMetadata({ params }: BlogPostPageProps): Promise<Metadata> {
  const slug = params.slug;
  
  // In a real app, you would fetch the blog post data here
  // For now, we'll use sample data based on the slug
  const post = getBlogPostBySlug(slug);
  
  if (!post) {
    return {
      title: 'Blog Post Not Found - GetYourMusicGear',
      description: 'The requested blog post could not be found.',
    };
  }

  return {
    title: `${post.title} - GetYourMusicGear Blog`,
    description: post.excerpt,
    keywords: post.tags.join(', '),
    openGraph: {
      title: post.title,
      description: post.excerpt,
      type: 'article',
      url: `https://getyourmusicgear.com/blog/${slug}`,
      publishedTime: post.date,
      authors: [post.author],
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.excerpt,
    },
  };
}

// Sample product data for blog posts
const sampleProducts = {
  electricGuitars: [
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
      description: 'The Fender Player Stratocaster is an excellent choice for beginners who want a classic electric guitar sound with modern playability.'
    },
    {
      id: 'epiphone-les-paul',
      name: 'Epiphone Les Paul Standard',
      slug: 'epiphone-les-paul-standard',
      brand: 'Epiphone',
      category: 'Electric Guitar',
      price: 599,
      originalPrice: 699,
      image: '/product-images/gibson_les_paul_studio_eb_1.jpg',
      rating: 4.6,
      reviewCount: 892,
      affiliateUrl: 'https://amazon.com/dp/B07C7V3V8L',
      features: [
        'Humbucker pickups',
        'Mahogany body with maple top',
        'Set neck for excellent sustain',
        'Versatile tone controls'
      ],
      description: 'The Epiphone Les Paul Standard offers the iconic Les Paul sound at an affordable price point.'
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
      description: 'The Yamaha Pacifica 112V is known for its exceptional build quality and playability at an affordable price.'
    }
  ],
  digitalPianos: [
    {
      id: 'yamaha-p45',
      name: 'Yamaha P-45 Digital Piano',
      slug: 'yamaha-p45',
      brand: 'Yamaha',
      category: 'Digital Piano',
      price: 449,
      originalPrice: 499,
      image: '/product-images/yamaha_p125_bk_1.jpg',
      rating: 4.5,
      reviewCount: 2341,
      affiliateUrl: 'https://amazon.com/dp/B07C7V3V8L',
      features: [
        '88 weighted keys',
        '10 different voices',
        'Built-in metronome',
        'Headphone output'
      ],
      description: 'The Yamaha P-45 is an affordable and reliable digital piano perfect for beginners.'
    },
    {
      id: 'casio-px-s1000',
      name: 'Casio PX-S1000',
      slug: 'casio-px-s1000',
      brand: 'Casio',
      category: 'Digital Piano',
      price: 599,
      image: '/product-images/casio_px560_bk_1.jpg',
      rating: 4.4,
      reviewCount: 987,
      affiliateUrl: 'https://amazon.com/dp/B07C7V3V8L',
      features: [
        'Ultra-slim design',
        'Smart Scaled Hammer Action',
        'Bluetooth connectivity',
        '18 different tones'
      ],
      description: 'The Casio PX-S1000 features a slim design with great features for modern musicians.'
    }
  ],
  studioMonitors: [
    {
      id: 'krk-rokit-5',
      name: 'KRK Rokit 5 G4',
      slug: 'krk-rokit-5-g4',
      brand: 'KRK',
      category: 'Studio Monitors',
      price: 299,
      originalPrice: 349,
      image: '/product-images/focusrite_scarlett_2i2_3rd_1.jpg',
      rating: 4.6,
      reviewCount: 1876,
      affiliateUrl: 'https://amazon.com/dp/B07C7V3V8L',
      features: [
        '5-inch woofer',
        'DSP room tuning',
        'Multiple input options',
        'Professional sound'
      ],
      description: 'Excellent entry-level monitors with DSP room tuning for accurate sound reproduction.'
    },
    {
      id: 'yamaha-hs5',
      name: 'Yamaha HS5',
      slug: 'yamaha-hs5',
      brand: 'Yamaha',
      category: 'Studio Monitors',
      price: 399,
      image: '/product-images/focusrite_scarlett_2i2_3rd_2.jpg',
      rating: 4.7,
      reviewCount: 2156,
      affiliateUrl: 'https://amazon.com/dp/B07C7V3V8L',
      features: [
        '5-inch woofer',
        '1-inch dome tweeter',
        'Flat frequency response',
        'Professional build quality'
      ],
      description: 'Classic monitors known for their flat, honest sound reproduction.'
    }
  ]
};

// Sample blog post data - in a real app, this would come from a CMS or API
function getBlogPostBySlug(slug: string) {
  const blogPosts = {
    'best-electric-guitars-beginners-2025': {
      title: "Best Electric Guitars for Beginners in 2025",
      excerpt: "Choosing your first electric guitar can be overwhelming with so many options available. We've compiled a comprehensive guide to help you find the perfect instrument to start your musical journey.",
      content: `
        <h2 id="introduction">Introduction</h2>
        <p>When it comes to choosing your first electric guitar, there are several factors to consider including budget, playing style, and personal preferences. In this guide, we'll explore the top options for beginners in 2025.</p>
        
        <h2 id="what-to-look-for">What to Look for in Your First Electric Guitar</h2>
        <p>Before diving into specific recommendations, let's discuss the key factors that make a guitar suitable for beginners:</p>
        <ul>
          <li><strong>Playability:</strong> The guitar should be comfortable to hold and play</li>
          <li><strong>Build Quality:</strong> Look for solid construction that will last</li>
          <li><strong>Versatility:</strong> Choose a guitar that can handle multiple genres</li>
          <li><strong>Value:</strong> Get the best quality for your budget</li>
        </ul>
        
        <h2 id="top-guitars">Top Electric Guitars for Beginners</h2>
        
        <h3>1. Fender Player Stratocaster</h3>
        <p>The Fender Player Stratocaster is an excellent choice for beginners who want a classic electric guitar sound. It features:</p>
        <ul>
          <li>Three single-coil pickups for versatile tone</li>
          <li>Comfortable C-shaped neck profile</li>
          <li>Reliable tuning stability</li>
          <li>Classic Stratocaster design</li>
        </ul>
        
        <h3>2. Epiphone Les Paul Standard</h3>
        <p>The Epiphone Les Paul Standard offers the iconic Les Paul sound at an affordable price:</p>
        <ul>
          <li>Humbucker pickups for rich, warm tone</li>
          <li>Mahogany body with maple top</li>
          <li>Set neck for excellent sustain</li>
          <li>Versatile tone controls</li>
        </ul>
        
        <h3>3. Yamaha Pacifica 112V</h3>
        <p>The Yamaha Pacifica 112V is known for its exceptional build quality and playability:</p>
        <ul>
          <li>HSS pickup configuration for versatility</li>
          <li>Comfortable neck profile</li>
          <li>Excellent value for money</li>
          <li>Reliable hardware</li>
        </ul>
        
        <h2 id="accessories">Essential Accessories</h2>
        <p>Don't forget these essential accessories for your new electric guitar:</p>
        <ul>
          <li><strong>Amplifier:</strong> A good practice amp is essential</li>
          <li><strong>Cables:</strong> Quality instrument cables</li>
          <li><strong>Picks:</strong> Various thicknesses to try</li>
          <li><strong>Strap:</strong> For comfortable playing while standing</li>
          <li><strong>Case:</strong> To protect your investment</li>
        </ul>
        
        <h2 id="conclusion">Conclusion</h2>
        <p>Choosing your first electric guitar is an exciting journey. Take your time to research and try different options. Remember, the best guitar is the one that inspires you to play and practice regularly.</p>
      `,
      author: "Music Gear Team",
      category: "Buying Guide",
      date: "Jan 15, 2025",
      readTime: "8 min read",
      image: "/images/blog-electric-guitars.jpg",
      tags: ["Electric Guitar", "Beginner", "Buying Guide", "2025"],
      expertTested: true,
      rating: 4.8,
      tableOfContents: [
        { title: "Introduction", id: "introduction" },
        { title: "What to Look for in Your First Electric Guitar", id: "what-to-look-for" },
        { title: "Top Electric Guitars for Beginners", id: "top-guitars" },
        { title: "Essential Accessories", id: "accessories" },
        { title: "Conclusion", id: "conclusion" }
      ],
      products: sampleProducts.electricGuitars
    },
    'how-choose-right-digital-piano': {
      title: "How to Choose the Right Digital Piano",
      excerpt: "Digital pianos offer incredible versatility and features, but selecting the right one requires understanding your needs and the available options.",
      content: `
        <h2 id="understanding">Understanding Digital Pianos</h2>
        <p>Digital pianos have come a long way in recent years, offering features that traditional acoustic pianos simply can't match. From built-in metronomes to recording capabilities, modern digital pianos are incredibly versatile.</p>
        
        <h2 id="key-factors">Key Factors to Consider</h2>
        
        <h3>1. Key Action</h3>
        <p>The key action determines how the keys feel when you play them. Look for:</p>
        <ul>
          <li>Weighted keys that simulate acoustic piano feel</li>
          <li>Graded hammer action for authentic touch</li>
          <li>Responsive key response</li>
        </ul>
        
        <h3>2. Sound Quality</h3>
        <p>Consider the following aspects of sound:</p>
        <ul>
          <li>Number of voices and sounds</li>
          <li>Polyphony (how many notes can be played simultaneously)</li>
          <li>Speaker quality and wattage</li>
          <li>Headphone compatibility</li>
        </ul>
        
        <h3>3. Features and Connectivity</h3>
        <p>Modern digital pianos offer various features:</p>
        <ul>
          <li>USB connectivity for computer integration</li>
          <li>Bluetooth for wireless connectivity</li>
          <li>Built-in recording capabilities</li>
          <li>Learning features and apps</li>
        </ul>
        
        <h2 id="recommendations">Top Recommendations</h2>
        
        <h3>Beginner Level</h3>
        <p>For beginners, consider these excellent options:</p>
        <ul>
          <li><strong>Yamaha P-45:</strong> Affordable and reliable</li>
          <li><strong>Casio PX-S1000:</strong> Slim design with great features</li>
          <li><strong>Roland FP-10:</strong> Excellent key action</li>
        </ul>
        
        <h3>Intermediate Level</h3>
        <p>For more serious players:</p>
        <ul>
          <li><strong>Yamaha P-125:</strong> Great sound and features</li>
          <li><strong>Kawai ES110:</strong> Superior key action</li>
          <li><strong>Roland FP-30X:</strong> Bluetooth connectivity</li>
        </ul>
        
        <h2 id="conclusion">Conclusion</h2>
        <p>Choosing the right digital piano depends on your skill level, budget, and specific needs. Take the time to research and try different models to find the perfect match for your musical journey.</p>
      `,
      author: "Piano Expert",
      category: "Buying Guide",
      date: "Jan 12, 2025",
      readTime: "12 min read",
      image: "/images/blog-digital-piano.jpg",
      tags: ["Digital Piano", "Buying Guide", "Piano"],
      expertTested: true,
      rating: 4.6,
      tableOfContents: [
        { title: "Understanding Digital Pianos", id: "understanding" },
        { title: "Key Factors to Consider", id: "key-factors" },
        { title: "Top Recommendations", id: "recommendations" },
        { title: "Conclusion", id: "conclusion" }
      ],
      products: sampleProducts.digitalPianos
    },
    'top-10-studio-monitors-under-500': {
      title: "Top 10 Studio Monitors Under €500",
      excerpt: "Professional-quality studio monitors that won't break the bank for home recording setups and music production.",
      content: `
        <h2 id="why-monitors">Why Studio Monitors Matter</h2>
        <p>Studio monitors are essential for accurate mixing and mastering. While professional-grade monitors can cost thousands, there are excellent options available for under €500 that deliver impressive performance.</p>
        
        <h2 id="what-to-look-for">What to Look for in Studio Monitors</h2>
        <ul>
          <li><strong>Frequency Response:</strong> Flat, accurate reproduction</li>
          <li><strong>Driver Size:</strong> Larger drivers for better bass response</li>
          <li><strong>Connectivity:</strong> Multiple input options</li>
          <li><strong>Room Size:</strong> Choose monitors appropriate for your space</li>
        </ul>
        
        <h2 id="top-monitors">Top 10 Studio Monitors Under €500</h2>
        
        <h3>1. KRK Rokit 5 G4</h3>
        <p>Excellent entry-level monitors with DSP room tuning.</p>
        
        <h3>2. Yamaha HS5</h3>
        <p>Classic monitors known for their flat, honest sound.</p>
        
        <h3>3. Adam Audio T5V</p>
        <p>Ribbon tweeters for detailed high-frequency reproduction.</p>
        
        <h3>4. PreSonus Eris E3.5</p>
        <p>Compact monitors perfect for small home studios.</p>
        
        <h3>5. Mackie CR3-X</h3>
        <p>Affordable monitors with good build quality.</p>
        
        <h3>6. Behringer Truth B1030A</h3>
        <p>Professional sound at an affordable price.</p>
        
        <h3>7. Focal Alpha 50</h3>
        <p>French engineering with excellent clarity.</p>
        
        <h3>8. JBL 305P MkII</h3>
        <p>Popular choice with great bass response.</p>
        
        <h3>9. IK Multimedia iLoud Micro Monitor</h3>
        <p>Ultra-compact monitors with surprising performance.</p>
        
        <h3>10. M-Audio BX5 D3</h3>
        <p>Reliable monitors with good value for money.</p>
        
        <h2 id="setup">Setting Up Your Studio Monitors</h2>
        <p>Proper placement is crucial for getting the best sound from your monitors:</p>
        <ul>
          <li>Position monitors at ear level</li>
          <li>Form an equilateral triangle with your listening position</li>
          <li>Keep monitors away from walls and corners</li>
          <li>Use monitor stands or isolation pads</li>
        </ul>
        
        <h2 id="conclusion">Conclusion</h2>
        <p>You don't need to spend thousands to get professional-quality monitoring. These options under €500 will serve you well for years to come.</p>
      `,
      author: "Audio Engineer",
      category: "Reviews",
      date: "Jan 10, 2025",
      readTime: "10 min read",
      image: "/images/blog-studio-monitors.jpg",
      tags: ["Studio Monitors", "Audio", "Reviews", "Budget"],
      expertTested: true,
      rating: 4.4,
      tableOfContents: [
        { title: "Why Studio Monitors Matter", id: "why-monitors" },
        { title: "What to Look for in Studio Monitors", id: "what-to-look-for" },
        { title: "Top 10 Studio Monitors Under €500", id: "top-monitors" },
        { title: "Setting Up Your Studio Monitors", id: "setup" },
        { title: "Conclusion", id: "conclusion" }
      ],
      products: sampleProducts.studioMonitors
    }
  };

  return blogPosts[slug as keyof typeof blogPosts] || null;
}

export default function BlogPostPage({ params }: BlogPostPageProps) {
  const post = getBlogPostBySlug(params.slug);

  if (!post) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">Blog Post Not Found</h1>
            <p className="text-lg text-gray-600 mb-8">
              The blog post you're looking for doesn't exist or has been moved.
            </p>
            <Link
              href="/blog"
              className="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Back to Blog
            </Link>
          </div>
        </div>
      </div>
    );
  }

  // Product comparison features for different categories
  const comparisonFeatures = {
    electricGuitars: [
      { key: 'pickups', label: 'Pickup Type', type: 'text' as const },
      { key: 'neck', label: 'Neck Profile', type: 'text' as const },
      { key: 'body', label: 'Body Material', type: 'text' as const },
      { key: 'price', label: 'Price Range', type: 'text' as const },
      { key: 'versatility', label: 'Genre Versatility', type: 'rating' as const }
    ],
    digitalPianos: [
      { key: 'keys', label: 'Number of Keys', type: 'number' as const },
      { key: 'weighted', label: 'Weighted Keys', type: 'boolean' as const },
      { key: 'polyphony', label: 'Polyphony', type: 'number' as const },
      { key: 'bluetooth', label: 'Bluetooth', type: 'boolean' as const },
      { key: 'price', label: 'Price Range', type: 'text' as const }
    ],
    studioMonitors: [
      { key: 'woofer', label: 'Woofer Size', type: 'text' as const },
      { key: 'power', label: 'Power Output', type: 'text' as const },
      { key: 'frequency', label: 'Frequency Response', type: 'text' as const },
      { key: 'inputs', label: 'Input Options', type: 'text' as const },
      { key: 'price', label: 'Price Range', type: 'text' as const }
    ]
  };

  // Enhanced product data with comparison features
  const enhancedProducts = post.products?.map(product => ({
    ...product,
    features: {
      pickups: product.name.includes('Strat') ? 'Single-coil' : 'Humbucker',
      neck: 'C-shaped',
      body: 'Alder',
      price: `€${product.price}`,
      versatility: 4,
      keys: 88,
      weighted: true,
      polyphony: 64,
      bluetooth: false,
      woofer: '5-inch',
      power: '50W',
      frequency: '43Hz-20kHz',
      inputs: 'XLR, TRS, RCA'
    },
    pros: [
      'Excellent build quality',
      'Great value for money',
      'Versatile sound',
      'Reliable performance'
    ],
    cons: [
      'Basic features',
      'Limited connectivity',
      'Entry-level components'
    ],
    bestFor: 'Beginners and intermediate players looking for quality instruments'
  })) || [];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-700 text-white py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex items-center justify-center gap-4 mb-6">
              <span className="text-xs font-semibold text-blue-200 uppercase tracking-wide">{post.category}</span>
              <span className="text-blue-200">•</span>
              <span className="text-blue-200">{post.date}</span>
              <span className="text-blue-200">•</span>
              <span className="text-blue-200">{post.readTime}</span>
            </div>
            <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">{post.title}</h1>
            <p className="text-xl text-blue-100 max-w-3xl mx-auto leading-relaxed">{post.excerpt}</p>
            <div className="mt-6 flex items-center justify-center gap-4">
              <span className="text-blue-200">By {post.author}</span>
              {post.expertTested && (
                <span className="bg-green-600 text-white px-3 py-1 rounded-full text-sm font-bold flex items-center gap-1">
                  <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  Expert Tested
                </span>
              )}
              {post.rating && (
                <div className="bg-white bg-opacity-90 px-3 py-1 rounded-full">
                  <div className="flex items-center gap-1">
                    <span className="text-yellow-500">★</span>
                    <span className="text-sm font-bold text-gray-900">{post.rating}</span>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Breadcrumb */}
        <nav className="mb-8" aria-label="Breadcrumb">
          <ol className="flex items-center space-x-2 text-sm text-gray-600">
            <li><Link href="/" className="hover:text-blue-600">Home</Link></li>
            <li>/</li>
            <li><Link href="/blog" className="hover:text-blue-600">Blog</Link></li>
            <li>/</li>
            <li className="text-gray-900" aria-current="page">{post.title}</li>
          </ol>
        </nav>

        <div className="grid lg:grid-cols-4 gap-12">
          {/* Main Content */}
          <div className="lg:col-span-3">
            {/* Article Content */}
            <article className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
              {/* Featured Image */}
              <div className="h-64 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg mb-8 flex items-center justify-center">
                <span className="text-white text-6xl">📝</span>
              </div>

              {/* Tags */}
              <div className="flex flex-wrap gap-2 mb-8">
                {post.tags.map((tag) => (
                  <span
                    key={tag}
                    className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium"
                  >
                    {tag}
                  </span>
                ))}
              </div>

              {/* Article Body */}
              <div 
                className="prose prose-lg max-w-none"
                dangerouslySetInnerHTML={{ __html: post.content }}
              />

              {/* Featured Product Showcase */}
              {post.products && post.products.length > 0 && (
                <div className="mt-12">
                  <BlogProductCard 
                    product={post.products[0]} 
                    variant="detailed"
                  />
                </div>
              )}

              {/* Product Comparison Table */}
              {post.products && post.products.length > 1 && (
                <ProductComparisonTable
                  products={enhancedProducts}
                  features={comparisonFeatures[post.category.toLowerCase().replace(' ', '') as keyof typeof comparisonFeatures] || comparisonFeatures.electricGuitars}
                  title={`${post.category} Comparison`}
                  description={`Compare the top ${post.category.toLowerCase()} options to find the perfect match for your needs`}
                />
              )}

              {/* Additional Product Cards */}
              {post.products && post.products.slice(1).map((product, index) => (
                <div key={product.id} className="mt-8">
                  <BlogProductCard 
                    product={product} 
                    variant="compact"
                    position={index % 2 === 0 ? 'left' : 'right'}
                  />
                </div>
              ))}
            </article>

            {/* Related Posts */}
            <section className="mt-16">
              <h2 className="text-2xl font-bold text-gray-900 mb-8">Related Articles</h2>
              <div className="grid md:grid-cols-2 gap-8">
                {[
                  {
                    title: "Essential Home Recording Equipment for Musicians",
                    excerpt: "Build a professional-quality home studio without breaking the bank with our essential equipment guide.",
                    href: "/blog/essential-home-recording-equipment",
                    category: "Tutorial"
                  },
                  {
                    title: "Understanding Guitar Amp Tones and Settings",
                    excerpt: "Master your amplifier's controls and learn how to dial in the perfect tone for any musical style.",
                    href: "/blog/understanding-guitar-amp-tones-settings",
                    category: "Tutorial"
                  }
                ].map((relatedPost) => (
                  <Link
                    key={relatedPost.href}
                    href={relatedPost.href}
                    className="block bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
                  >
                    <div className="flex items-center gap-2 mb-3">
                      <span className="text-xs font-semibold text-blue-600 uppercase tracking-wide">{relatedPost.category}</span>
                    </div>
                    <h3 className="text-xl font-bold text-gray-900 mb-3 line-clamp-2">{relatedPost.title}</h3>
                    <p className="text-gray-600 line-clamp-3">{relatedPost.excerpt}</p>
                  </Link>
                ))}
              </div>
            </section>

            {/* Newsletter Signup */}
            <section className="mt-16 bg-gradient-to-r from-blue-600 to-purple-700 rounded-xl p-8 text-white">
              <div className="text-center">
                <h3 className="text-2xl font-bold mb-4">Stay Updated</h3>
                <p className="text-blue-100 mb-6 max-w-2xl mx-auto">
                  Get the latest articles, reviews, and buying guides delivered to your inbox. Join thousands of musicians who trust our expert advice.
                </p>
                <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
                  <input
                    type="email"
                    placeholder="Enter your email"
                    className="flex-1 px-4 py-3 border border-transparent rounded-lg focus:ring-2 focus:ring-white focus:border-transparent text-gray-900"
                  />
                  <button className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
                    Subscribe
                  </button>
                </div>
                <p className="text-xs text-blue-200 mt-3">
                  No spam, unsubscribe at any time. We respect your privacy.
                </p>
              </div>
            </section>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="sticky top-8 space-y-8">
              {/* Table of Contents */}
              {post.tableOfContents && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Table of Contents</h3>
                  <nav className="space-y-2">
                    {post.tableOfContents.map((item) => (
                      <a
                        key={item.id}
                        href={`#${item.id}`}
                        className="block text-sm text-gray-600 hover:text-blue-600 hover:font-medium transition-colors"
                      >
                        {item.title}
                      </a>
                    ))}
                  </nav>
                </div>
              )}

              {/* Author Info */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-4">About the Author</h3>
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                    <span className="text-white font-bold text-lg">
                      {post.author.split(' ').map(n => n[0]).join('')}
                    </span>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900">{post.author}</h4>
                    <p className="text-sm text-gray-600">Music Professional</p>
                  </div>
                </div>
                <p className="text-sm text-gray-600">
                  {post.author} is a certified music professional with years of experience in the industry. 
                  They specialize in {post.category.toLowerCase()} and are passionate about helping musicians find the right equipment.
                </p>
              </div>

              {/* Quick Stats */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-4">Article Stats</h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Read Time</span>
                    <span className="text-sm font-medium text-gray-900">{post.readTime}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Category</span>
                    <span className="text-sm font-medium text-gray-900">{post.category}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Published</span>
                    <span className="text-sm font-medium text-gray-900">{post.date}</span>
                  </div>
                  {post.rating && (
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Rating</span>
                      <div className="flex items-center gap-1">
                        <span className="text-yellow-500 text-sm">★</span>
                        <span className="text-sm font-medium text-gray-900">{post.rating}</span>
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Share Buttons */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-4">Share This Article</h3>
                <div className="flex gap-2">
                  <button className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors">
                    Facebook
                  </button>
                  <button className="flex-1 bg-blue-400 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-500 transition-colors">
                    Twitter
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
