"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';

export function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-white border-b border-gray-300 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          {/* Logo - Increased size */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center hover:opacity-80 transition-opacity">
              <Image 
                src="/logo.png" 
                alt="GetYourMusicGear Logo" 
                width={200} 
                height={60}
                className="h-16 w-auto"
              />
            </Link>
          </div>

          {/* Desktop Navigation - Updated with all categories and optimized spacing */}
          <nav className="hidden xl:flex items-center space-x-4">
            <Link href="/products?category=acoustic-guitars" className="text-gray-900 hover:text-gray-700 transition-colors text-xs font-medium whitespace-nowrap">Acoustic Guitars</Link>
            <Link href="/products?category=electric-guitars" className="text-gray-900 hover:text-gray-700 transition-colors text-xs font-medium whitespace-nowrap">Electric Guitars</Link>
            <Link href="/products?category=bass-guitars" className="text-gray-900 hover:text-gray-700 transition-colors text-xs font-medium whitespace-nowrap">Bass Guitars</Link>
            <Link href="/products?category=drums-percussion" className="text-gray-900 hover:text-gray-700 transition-colors text-xs font-medium whitespace-nowrap">Drums & Percussion</Link>
            <Link href="/products?category=pianos-keyboards" className="text-gray-900 hover:text-gray-700 transition-colors text-xs font-medium whitespace-nowrap">Pianos & Keyboards</Link>
            <Link href="/products?category=orchestral" className="text-gray-900 hover:text-gray-700 transition-colors text-xs font-medium whitespace-nowrap">Orchestral</Link>
            <Link href="/products?category=live-sound-lighting" className="text-gray-900 hover:text-gray-700 transition-colors text-xs font-medium whitespace-nowrap">Live Sound & Lighting</Link>
            <Link href="/products?category=studio-production" className="text-gray-900 hover:text-gray-700 transition-colors text-xs font-medium whitespace-nowrap">Studio & Production</Link>
            <Link href="/products?category=music-software" className="text-gray-900 hover:text-gray-700 transition-colors text-xs font-medium whitespace-nowrap">Music Software</Link>
            <Link href="/products?category=dj-equipment" className="text-gray-900 hover:text-gray-700 transition-colors text-xs font-medium whitespace-nowrap">DJ Equipment</Link>
            <Link href="/products?category=home-audio" className="text-gray-900 hover:text-gray-700 transition-colors text-xs font-medium whitespace-nowrap">Home Audio</Link>
          </nav>

          {/* Right side */}
          <div className="flex items-center space-x-4">
            {/* Mobile menu button */}
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="xl:hidden text-gray-900 hover:text-gray-700 p-2 rounded-md transition-colors"
            >
              <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {isMenuOpen && (
        <div className="xl:hidden bg-white border-t border-gray-300 animate-slide-up">
          <div className="px-4 pt-4 pb-3 space-y-3">
            <Link href="/products?category=acoustic-guitars" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Acoustic Guitars</Link>
            <Link href="/products?category=electric-guitars" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Electric Guitars</Link>
            <Link href="/products?category=bass-guitars" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Bass Guitars</Link>
            <Link href="/products?category=drums-percussion" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Drums & Percussion</Link>
            <Link href="/products?category=pianos-keyboards" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Pianos & Keyboards</Link>
            <Link href="/products?category=orchestral" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Orchestral</Link>
            <Link href="/products?category=live-sound-lighting" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Live Sound & Lighting</Link>
            <Link href="/products?category=studio-production" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Studio & Production</Link>
            <Link href="/products?category=music-software" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Music Software</Link>
            <Link href="/products?category=dj-equipment" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">DJ Equipment</Link>
            <Link href="/products?category=home-audio" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Home Audio</Link>
          </div>
        </div>
      )}
    </header>
  );
}

export default Header;


