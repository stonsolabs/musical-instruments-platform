"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';

export function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-white border-b border-gray-300 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo - Optimized size */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center hover:opacity-80 transition-opacity">
              <Image 
                src="/logo.png" 
                alt="GetYourMusicGear Logo" 
                width={160} 
                height={50}
                className="h-12 w-auto"
              />
            </Link>
          </div>

          {/* Desktop Navigation - Optimized spacing and text size */}
          <nav className="hidden lg:flex items-center space-x-6">
            <Link href="/products?category=electric-guitars" className="text-gray-900 hover:text-gray-700 transition-colors text-sm font-medium">Electric Guitars</Link>
            <Link href="/products?category=acoustic-guitars" className="text-gray-900 hover:text-gray-700 transition-colors text-sm font-medium">Acoustic Guitars</Link>
            <Link href="/products?category=digital-keyboards" className="text-gray-900 hover:text-gray-700 transition-colors text-sm font-medium">Keyboards</Link>
            <Link href="/products?category=amplifiers" className="text-gray-900 hover:text-gray-700 transition-colors text-sm font-medium">Amplifiers</Link>
            <Link href="/products?category=bass-guitars" className="text-gray-900 hover:text-gray-700 transition-colors text-sm font-medium">Bass Guitars</Link>
            <Link href="/products?category=drums-percussion" className="text-gray-900 hover:text-gray-700 transition-colors text-sm font-medium">Drums</Link>
            <Link href="/products?category=effects-pedals" className="text-gray-900 hover:text-gray-700 transition-colors text-sm font-medium">Effects</Link>
            <Link href="/products?category=dj-equipment" className="text-gray-900 hover:text-gray-700 transition-colors text-sm font-medium">DJ</Link>
            <Link href="/products?category=studio-and-recording-equipment" className="text-gray-900 hover:text-gray-700 transition-colors text-sm font-medium">Studio</Link>
          </nav>

          {/* Right side */}
          <div className="flex items-center space-x-4">
            {/* Mobile menu button */}
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="lg:hidden text-gray-900 hover:text-gray-700 p-2 rounded-md transition-colors"
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
        <div className="lg:hidden bg-white border-t border-gray-300 animate-slide-up">
          <div className="px-4 pt-4 pb-3 space-y-3">
            <Link href="/products?category=electric-guitars" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Electric Guitars</Link>
            <Link href="/products?category=acoustic-guitars" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Acoustic Guitars</Link>
            <Link href="/products?category=digital-keyboards" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Digital Keyboards</Link>
            <Link href="/products?category=amplifiers" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Amplifiers</Link>
            <Link href="/products?category=bass-guitars" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Bass Guitars</Link>
            <Link href="/products?category=drums-percussion" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Drums & Percussion</Link>
            <Link href="/products?category=effects-pedals" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Effects Pedals</Link>
            <Link href="/products?category=dj-equipment" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">DJ Equipment</Link>
            <Link href="/products?category=studio-and-recording-equipment" className="block px-3 py-2 text-gray-900 hover:text-gray-700 transition-colors text-base">Studio & Recording</Link>
          </div>
        </div>
      )}
    </header>
  );
}

export default Header;


