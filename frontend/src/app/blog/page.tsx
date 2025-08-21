import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Blog - Musical Instruments News & Reviews',
  description: 'Stay updated with the latest instrument reviews, buying guides, industry insights, and musical instrument news.',
  keywords: 'musical instrument blog, guitar reviews, piano reviews, music equipment news, instrument buying guides',
  openGraph: {
    title: 'Blog - Musical Instruments News & Reviews',
    description: 'Stay updated with the latest instrument reviews, buying guides, industry insights, and musical instrument news.',
    type: 'website',
    url: 'https://getyourmusicgear.com/blog',
  },
  twitter: {
    card: 'summary',
    title: 'Blog - Musical Instruments News & Reviews',
    description: 'Stay updated with the latest instrument reviews, buying guides, industry insights, and musical instrument news.',
  },
};

export default function BlogPage() {
  // Sample blog posts data - in a real app, this would come from a CMS or API
  const blogPosts = [
    {
      id: 1,
      title: "Best Electric Guitars for Beginners in 2025",
      excerpt: "Choosing your first electric guitar can be overwhelming with so many options available. We've compiled a comprehensive guide to help you find the perfect instrument to start your musical journey.",
      content: "When it comes to choosing your first electric guitar, there are several factors to consider including budget, playing style, and personal preferences. In this guide, we'll explore the top options for beginners in 2025...",
      author: "Music Gear Team",
      category: "Buying Guide",
      date: "Jan 15, 2025",
      readTime: "8 min read",
      image: "/images/blog-electric-guitars.jpg",
      slug: "best-electric-guitars-beginners-2025",
      featured: true,
      tags: ["Electric Guitar", "Beginner", "Buying Guide", "2025"],
      expertTested: true,
      rating: 4.8
    },
    {
      id: 2,
      title: "How to Choose the Right Digital Piano",
      excerpt: "Digital pianos offer incredible versatility and features, but selecting the right one requires understanding your needs and the available options.",
      content: "Digital pianos have come a long way in recent years, offering features that traditional acoustic pianos simply can't match. From built-in metronomes to recording capabilities, modern digital pianos are incredibly versatile...",
      author: "Piano Expert",
      category: "Buying Guide",
      date: "Jan 12, 2025",
      readTime: "12 min read",
      image: "/images/blog-digital-piano.jpg",
      slug: "how-choose-right-digital-piano",
      featured: true,
      tags: ["Digital Piano", "Buying Guide", "Piano"],
      expertTested: true,
      rating: 4.6
    },
    {
      id: 3,
      title: "Top 10 Studio Monitors Under €500",
      excerpt: "Professional-quality studio monitors that won't break the bank for home recording setups and music production.",
      content: "Studio monitors are essential for accurate mixing and mastering. While professional-grade monitors can cost thousands, there are excellent options available for under €500 that deliver impressive performance...",
      author: "Audio Engineer",
      category: "Reviews",
      date: "Jan 10, 2025",
      readTime: "10 min read",
      image: "/images/blog-studio-monitors.jpg",
      slug: "top-10-studio-monitors-under-500",
      featured: true,
      tags: ["Studio Monitors", "Audio", "Reviews", "Budget"],
      expertTested: true,
      rating: 4.4
    },
    {
      id: 4,
      title: "The Evolution of Guitar Effects Pedals",
      excerpt: "From simple analog circuits to complex digital processors, explore how guitar effects have evolved over the decades.",
      content: "Guitar effects pedals have transformed the way we think about electric guitar tone. What started as simple analog circuits in the 1960s has evolved into sophisticated digital processors...",
      author: "Guitar Tech",
      category: "History",
      date: "Jan 8, 2025",
      readTime: "15 min read",
      image: "/images/blog-effects-pedals.jpg",
      slug: "evolution-guitar-effects-pedals",
      featured: false,
      tags: ["Effects Pedals", "Guitar", "History", "Technology"],
      expertTested: false,
      rating: 4.2
    },
    {
      id: 5,
      title: "Essential Home Recording Equipment for Musicians",
      excerpt: "Build a professional-quality home studio without breaking the bank with our essential equipment guide.",
      content: "Creating a home recording studio is more accessible than ever before. With the right equipment and some basic knowledge, you can produce professional-quality recordings from the comfort of your home...",
      author: "Recording Expert",
      category: "Tutorial",
      date: "Jan 5, 2025",
      readTime: "14 min read",
      image: "/images/blog-home-recording.jpg",
      slug: "essential-home-recording-equipment",
      featured: false,
      tags: ["Home Recording", "Studio", "Equipment", "Tutorial"],
      expertTested: true,
      rating: 4.5
    },
    {
      id: 6,
      title: "Understanding Guitar Amp Tones and Settings",
      excerpt: "Master your amplifier's controls and learn how to dial in the perfect tone for any musical style.",
      content: "Your guitar amplifier is one of the most important components in your signal chain. Understanding how to properly set your amp can make the difference between a great tone and a mediocre one...",
      author: "Amp Specialist",
      category: "Tutorial",
      date: "Jan 3, 2025",
      readTime: "11 min read",
      image: "/images/blog-amp-tones.jpg",
      slug: "understanding-guitar-amp-tones-settings",
      featured: false,
      tags: ["Guitar Amp", "Tone", "Tutorial", "Settings"],
      expertTested: true,
      rating: 4.3
    }
  ];

  const featuredPosts = blogPosts.filter(post => post.featured);
  const regularPosts = blogPosts.filter(post => !post.featured);

  const categories = [
    { name: "All", count: blogPosts.length },
    { name: "Buying Guide", count: blogPosts.filter(post => post.category === "Buying Guide").length },
    { name: "Reviews", count: blogPosts.filter(post => post.category === "Reviews").length },
    { name: "Tutorial", count: blogPosts.filter(post => post.category === "Tutorial").length },
    { name: "History", count: blogPosts.filter(post => post.category === "History").length }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-700 text-white py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Blog</h1>
          <p className="text-xl text-blue-100 max-w-2xl mx-auto">
            Stay updated with the latest instrument reviews, buying guides, industry insights, and musical instrument news
          </p>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Breadcrumb */}
        <nav className="mb-8" aria-label="Breadcrumb">
          <ol className="flex items-center space-x-2 text-sm text-gray-600">
            <li><Link href="/" className="hover:text-blue-600">Home</Link></li>
            <li>/</li>
            <li className="text-gray-900" aria-current="page">Blog</li>
          </ol>
        </nav>

        {/* Expert Testing Badge */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-8">
          <div className="flex items-center gap-3">
            <div className="flex-shrink-0">
              <svg className="w-6 h-6 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-blue-900">Expert Tested</h3>
              <p className="text-sm text-blue-700">Our team of music professionals personally tests and reviews every product featured in our articles to ensure quality and performance you can trust.</p>
            </div>
          </div>
        </div>

        {/* Categories Filter */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Browse by Category</h2>
          <div className="flex flex-wrap gap-4">
            {categories.map((category) => (
              <button
                key={category.name}
                className="px-6 py-3 rounded-lg border border-gray-300 text-gray-700 hover:bg-blue-600 hover:text-white hover:border-blue-600 transition-colors font-medium"
              >
                {category.name} ({category.count})
              </button>
            ))}
          </div>
        </div>

        {/* Featured Posts */}
        {featuredPosts.length > 0 && (
          <section className="mb-16">
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-3xl font-bold text-gray-900">Featured Articles</h2>
              <Link href="/blog" className="text-blue-600 hover:text-blue-700 font-medium">
                View All Articles →
              </Link>
            </div>
            <div className="grid lg:grid-cols-2 gap-8">
              {featuredPosts.map((post) => (
                <article key={post.id} className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden hover:shadow-xl transition-shadow duration-300">
                  <div className="relative">
                    <div className="h-64 bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                      <span className="text-white text-6xl">📝</span>
                    </div>
                    <div className="absolute top-4 left-4 flex gap-2">
                      <span className="bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-bold">
                        Featured
                      </span>
                      {post.expertTested && (
                        <span className="bg-green-600 text-white px-3 py-1 rounded-full text-sm font-bold flex items-center gap-1">
                          <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                          </svg>
                          Expert Tested
                        </span>
                      )}
                    </div>
                    {post.rating && (
                      <div className="absolute top-4 right-4 bg-white bg-opacity-90 px-3 py-1 rounded-full">
                        <div className="flex items-center gap-1">
                          <span className="text-yellow-500">★</span>
                          <span className="text-sm font-bold text-gray-900">{post.rating}</span>
                        </div>
                      </div>
                    )}
                  </div>
                  
                  <div className="p-8">
                    <div className="flex items-center gap-4 mb-4">
                      <span className="text-sm font-semibold text-blue-600 uppercase tracking-wide">{post.category}</span>
                      <span className="text-sm text-gray-500">•</span>
                      <span className="text-sm text-gray-500">{post.date}</span>
                      <span className="text-sm text-gray-500">•</span>
                      <span className="text-sm text-gray-500">{post.readTime}</span>
                    </div>
                    
                    <h3 className="text-2xl font-bold text-gray-900 mb-4 line-clamp-2">{post.title}</h3>
                    <p className="text-gray-600 mb-6 line-clamp-3">{post.excerpt}</p>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-500">By {post.author}</span>
                      <Link
                        href={`/blog/${post.slug}`}
                        className="inline-flex items-center text-blue-600 font-medium hover:text-blue-700"
                      >
                        Read More
                        <svg className="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                      </Link>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          </section>
        )}

        {/* All Posts */}
        <section>
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-3xl font-bold text-gray-900">Latest Articles</h2>
            <div className="flex items-center gap-4">
              <select className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                <option>Sort by Date</option>
                <option>Sort by Rating</option>
                <option>Sort by Read Time</option>
              </select>
            </div>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {regularPosts.map((post) => (
              <article key={post.id} className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
                <div className="relative">
                  <div className="h-48 bg-gradient-to-br from-green-500 to-blue-600 flex items-center justify-center">
                    <span className="text-white text-4xl">📝</span>
                  </div>
                  {post.expertTested && (
                    <div className="absolute top-3 left-3">
                      <span className="bg-green-600 text-white px-2 py-1 rounded-full text-xs font-bold flex items-center gap-1">
                        <svg className="w-2 h-2" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                        Expert
                      </span>
                    </div>
                  )}
                  {post.rating && (
                    <div className="absolute top-3 right-3 bg-white bg-opacity-90 px-2 py-1 rounded-full">
                      <div className="flex items-center gap-1">
                        <span className="text-yellow-500 text-xs">★</span>
                        <span className="text-xs font-bold text-gray-900">{post.rating}</span>
                      </div>
                    </div>
                  )}
                </div>
                
                <div className="p-6">
                  <div className="flex items-center gap-2 mb-3">
                    <span className="text-xs font-semibold text-blue-600 uppercase tracking-wide">{post.category}</span>
                    <span className="text-xs text-gray-500">•</span>
                    <span className="text-xs text-gray-500">{post.date}</span>
                  </div>
                  
                  <h3 className="text-xl font-bold text-gray-900 mb-3 line-clamp-2">{post.title}</h3>
                  <p className="text-gray-600 mb-4 line-clamp-3">{post.excerpt}</p>
                  
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-sm text-gray-500">{post.readTime}</span>
                    <span className="text-sm text-gray-500">By {post.author}</span>
                  </div>
                  
                  <Link
                    href={`/blog/${post.slug}`}
                    className="inline-flex items-center text-blue-600 font-medium hover:text-blue-700"
                  >
                    Read More
                    <svg className="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </Link>
                </div>
              </article>
            ))}
          </div>
        </section>

        {/* Newsletter Signup */}
        <section className="mt-16 bg-gradient-to-r from-blue-600 to-purple-700 rounded-xl p-8 text-white">
          <div className="text-center">
            <h3 className="text-2xl font-bold mb-4">Stay Updated</h3>
            <p className="text-blue-100 mb-6 max-w-2xl mx-auto">
              Subscribe to our newsletter and get the latest articles, reviews, and buying guides delivered to your inbox. Join thousands of musicians who trust our expert advice.
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
    </div>
  );
}
