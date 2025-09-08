import React from 'react';
import Link from 'next/link';
import { GiftIcon, TruckIcon, StarIcon } from '@heroicons/react/24/outline';

export default function SpecialOffers() {
  return (
    <div className="text-center text-white">
      <h2 className="text-3xl font-bold mb-8">🎵 Special Offers!</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
        {/* Fender Offer */}
        <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
          <div className="text-4xl mb-4">🎸</div>
          <h3 className="text-xl font-bold mb-2">Fender Special</h3>
          <p className="text-white/90 mb-4">Get 15% off on all Fender guitars this month</p>
          <Link
            href="/products?brand=fender&sale=true"
            className="inline-block bg-white text-brand-blue hover:bg-gray-100 px-6 py-2 rounded-full font-medium transition-colors"
          >
            Shop Now
          </Link>
        </div>

        {/* Thomann Offer */}
        <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
          <div className="text-4xl mb-4">🚚</div>
          <h3 className="text-xl font-bold mb-2">Thomann Special</h3>
          <p className="text-white/90 mb-4">Free shipping on orders over €199</p>
          <Link
            href="/products?store=thomann"
            className="inline-block bg-white text-brand-blue hover:bg-gray-100 px-6 py-2 rounded-full font-medium transition-colors"
          >
            Learn More
          </Link>
        </div>

        {/* General Sale */}
        <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
          <div className="text-4xl mb-4">🔥</div>
          <h3 className="text-xl font-bold mb-2">Sale</h3>
          <p className="text-white/90 mb-4">Up to 40% off on selected instruments</p>
          <Link
            href="/products?sale=true"
            className="inline-block bg-white text-brand-blue hover:bg-gray-100 px-6 py-2 rounded-full font-medium transition-colors"
          >
            Shop Sale
          </Link>
        </div>
      </div>

      {/* Newsletter Signup */}
      <div className="bg-white/10 backdrop-blur-sm rounded-lg p-8 border border-white/20 max-w-2xl mx-auto">
        <h3 className="text-2xl font-bold mb-4">Stay Updated with the Latest</h3>
        <p className="text-white/90 mb-6">
          Get expert instrument reviews, buying guides, and industry insights delivered to your inbox
        </p>
        
        <form className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
          <input
            type="email"
            placeholder="Enter your email"
            className="flex-1 px-4 py-3 rounded-lg border-0 text-gray-900 placeholder-gray-500 focus:ring-2 focus:ring-white/50 focus:outline-none"
            required
          />
          <button
            type="submit"
            className="bg-brand-orange hover:bg-orange-600 text-white px-6 py-3 rounded-lg font-medium transition-colors whitespace-nowrap"
          >
            Subscribe
          </button>
        </form>
      </div>
    </div>
  );
}

