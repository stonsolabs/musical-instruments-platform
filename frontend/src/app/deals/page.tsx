import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';


export const metadata: Metadata = {
  title: 'Special Deals - Musical Instruments',
  description: 'Find the best deals and special offers on musical instruments from top retailers across Europe.',
  keywords: 'musical instrument deals, guitar deals, piano deals, music equipment sales, instrument discounts',
  openGraph: {
    title: 'Special Deals - Musical Instruments',
    description: 'Find the best deals and special offers on musical instruments from top retailers across Europe.',
    type: 'website',
    url: 'https://getyourmusicgear.com/deals',
  },
  twitter: {
    card: 'summary',
    title: 'Special Deals - Musical Instruments',
    description: 'Find the best deals and special offers on musical instruments from top retailers across Europe.',
  },
};

export default function DealsPage() {
  // Sample deals data - in a real app, this would come from an API
  const deals = [
    {
      id: 1,
      title: "Fender Player Stratocaster - 20% Off",
      description: "Limited time offer on the iconic Fender Player Stratocaster electric guitar",
      originalPrice: "€699",
      salePrice: "€559",
      discount: "20%",
      store: "Thomann",
      category: "Electric Guitars",
      image: "/images/fender-stratocaster.jpg",
      affiliateUrl: "https://www.thomann.de/fender_player_stratocaster.html",
      validUntil: "Jan 31, 2025",
      featured: true
    },
    {
      id: 2,
      title: "Yamaha P-45 Digital Piano Bundle",
      description: "Complete digital piano setup with stand, bench, and headphones included",
      originalPrice: "€499",
      salePrice: "€399",
      discount: "20%",
      store: "Gear4Music",
      category: "Digital Pianos",
      image: "/images/yamaha-p45.jpg",
      affiliateUrl: "https://www.gear4music.com/yamaha_p45_bundle.html",
      validUntil: "Feb 15, 2025",
      featured: false
    },
    {
      id: 3,
      title: "Roland TD-1DMK Electronic Drum Kit",
      description: "Professional electronic drum kit with mesh heads and realistic feel",
      originalPrice: "€799",
      salePrice: "€649",
      discount: "19%",
      store: "Music Store",
      category: "Electronic Drums",
      image: "/images/roland-td1dmk.jpg",
      affiliateUrl: "https://www.musicstore.com/roland_td1dmk.html",
      validUntil: "Jan 25, 2025",
      featured: true
    },
    {
      id: 4,
      title: "Shure SM58 Microphone + Cable",
      description: "Industry standard vocal microphone with professional XLR cable",
      originalPrice: "€129",
      salePrice: "€99",
      discount: "23%",
      store: "Thomann",
      category: "Microphones",
      image: "/images/shure-sm58.jpg",
      affiliateUrl: "https://www.thomann.de/shure_sm58_bundle.html",
      validUntil: "Feb 10, 2025",
      featured: false
    },
    {
      id: 5,
      title: "Focusrite Scarlett 2i2 Audio Interface",
      description: "Professional 2-channel USB audio interface for recording",
      originalPrice: "€149",
      salePrice: "€119",
      discount: "20%",
      store: "Gear4Music",
      category: "Studio and Recording Equipment",
      image: "/images/focusrite-scarlett.jpg",
      affiliateUrl: "https://www.gear4music.com/focusrite_scarlett_2i2.html",
      validUntil: "Jan 28, 2025",
      featured: false
    },
    {
      id: 6,
      title: "Gibson Les Paul Studio - Free Shipping",
      description: "Classic Gibson Les Paul Studio with free worldwide shipping",
      originalPrice: "€1,299",
      salePrice: "€1,199",
      discount: "8%",
      store: "Music Store",
      category: "Electric Guitars",
      image: "/images/gibson-les-paul.jpg",
      affiliateUrl: "https://www.musicstore.com/gibson_les_paul_studio.html",
      validUntil: "Feb 20, 2025",
      featured: true
    }
  ];

  const featuredDeals = deals.filter(deal => deal.featured);
  const regularDeals = deals.filter(deal => !deal.featured);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-gradient-to-r from-orange-500 to-red-600 text-white py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Special Deals</h1>
          <p className="text-xl text-orange-100 max-w-2xl mx-auto">
            Discover exclusive offers and discounts on musical instruments from Europe's top retailers
          </p>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Breadcrumb */}
        <nav className="mb-8" aria-label="Breadcrumb">
          <ol className="flex items-center space-x-2 text-sm text-gray-600">
            <li><Link href="/" className="hover:text-blue-600">Home</Link></li>
            <li>/</li>
            <li className="text-gray-900" aria-current="page">Deals</li>
          </ol>
        </nav>

        {/* Featured Deals */}
        {featuredDeals.length > 0 && (
          <section className="mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-8">Featured Deals</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {featuredDeals.map((deal) => (
                <div key={deal.id} className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden hover:shadow-xl transition-shadow duration-300">
                  <div className="relative">
                    <div className="h-48 bg-gradient-to-br from-orange-400 to-red-500 flex items-center justify-center">
                      <span className="text-white text-6xl">🎸</span>
                    </div>
                    <div className="absolute top-4 left-4">
                      <span className="bg-red-600 text-white px-3 py-1 rounded-full text-sm font-bold">
                        {deal.discount} OFF
                      </span>
                    </div>
                    <div className="absolute top-4 right-4">
                      <span className="bg-gray-900 text-white px-2 py-1 rounded text-xs">
                        {deal.store}
                      </span>
                    </div>
                  </div>
                  
                  <div className="p-6">
                    <div className="flex items-center gap-2 mb-3">
                      <span className="text-xs font-semibold text-blue-600 uppercase tracking-wide">{deal.category}</span>
                    </div>
                    
                    <h3 className="text-xl font-bold text-gray-900 mb-3 line-clamp-2">{deal.title}</h3>
                    <p className="text-gray-600 mb-4 line-clamp-2">{deal.description}</p>
                    
                    <div className="flex items-center gap-3 mb-4">
                      <span className="text-2xl font-bold text-green-600">{deal.salePrice}</span>
                      <span className="text-lg text-gray-400 line-through">{deal.originalPrice}</span>
                    </div>
                    
                    <div className="flex items-center justify-between mb-4">
                      <span className="text-sm text-gray-500">Valid until {deal.validUntil}</span>
                    </div>
                    
                    {deal.store === "Thomann" ? (
                      <a
                        href={deal.affiliateUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="fp-table__button fp-table__button--thomann w-full"
                      >
                        <span>View Price at</span>
                        <img src="/thomann-100.png" alt="th•mann" className="w-16 h-8 object-contain" style={{ backgroundColor: 'white' }} />
                      </a>
                    ) : deal.store === "Gear4Music" ? (
                      <a
                        href={deal.affiliateUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="fp-table__button fp-table__button--gear4music w-full"
                      >
                        <span>View Price at</span>
                        <img src="/gear-100.png" alt="Gear4music" className="w-16 h-8 object-contain" style={{ backgroundColor: 'white' }} />
                      </a>
                    ) : (
                      <a
                        href={deal.affiliateUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="block w-full text-center bg-orange-500 text-white py-3 rounded-lg hover:bg-orange-600 transition-colors font-semibold"
                      >
                        Shop Now at {deal.store}
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* All Deals */}
        <section>
          <h2 className="text-3xl font-bold text-gray-900 mb-8">All Deals</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {regularDeals.map((deal) => (
              <div key={deal.id} className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
                <div className="relative">
                  <div className="h-40 bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center">
                    <span className="text-white text-4xl">🎹</span>
                  </div>
                  <div className="absolute top-3 left-3">
                    <span className="bg-red-600 text-white px-2 py-1 rounded text-xs font-bold">
                      {deal.discount} OFF
                    </span>
                  </div>
                </div>
                
                <div className="p-5">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-xs font-semibold text-blue-600 uppercase tracking-wide">{deal.category}</span>
                  </div>
                  
                  <h3 className="text-lg font-bold text-gray-900 mb-2 line-clamp-2">{deal.title}</h3>
                  <p className="text-gray-600 mb-3 text-sm line-clamp-2">{deal.description}</p>
                  
                  <div className="flex items-center gap-2 mb-3">
                    <span className="text-xl font-bold text-green-600">{deal.salePrice}</span>
                    <span className="text-sm text-gray-400 line-through">{deal.originalPrice}</span>
                  </div>
                  
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs text-gray-500">Valid until {deal.validUntil}</span>
                    <span className="text-xs text-gray-600">{deal.store}</span>
                  </div>
                  
                  {deal.store === "Thomann" ? (
                    <a
                      href={deal.affiliateUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="fp-table__button fp-table__button--thomann w-full"
                    >
                      <span>View Price at</span>
                      <img src="/thomann-100.png" alt="th•mann" className="w-16 h-8 object-contain" style={{ backgroundColor: 'white' }} />
                    </a>
                  ) : deal.store === "Gear4Music" ? (
                    <a
                      href={deal.affiliateUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="fp-table__button fp-table__button--gear4music w-full"
                    >
                      <span>View Price at</span>
                      <img src="/gear-100.png" alt="Gear4music" className="w-16 h-8 object-contain" style={{ backgroundColor: 'white' }} />
                    </a>
                  ) : (
                    <a
                      href={deal.affiliateUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block w-full text-center bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm font-semibold"
                    >
                      Shop Now
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Newsletter Signup */}
        <section className="mt-16 bg-white rounded-xl shadow-sm border border-gray-200 p-8">
          <div className="text-center">
            <h3 className="text-2xl font-bold text-gray-900 mb-4">Never Miss a Deal</h3>
            <p className="text-gray-600 mb-6">
              Subscribe to our newsletter and be the first to know about new deals and special offers
            </p>
            <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
              <input
                type="email"
                placeholder="Enter your email"
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors">
                Subscribe
              </button>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
