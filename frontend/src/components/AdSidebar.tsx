"use client";

import React from 'react';
import AdSense, { AdPlaceholder } from './AdSense';

interface AdSidebarProps {
  className?: string;
}

export default function AdSidebar({ className = '' }: AdSidebarProps) {
  const hasAdSenseClient = process.env.NEXT_PUBLIC_GOOGLE_ADSENSE_CLIENT_ID;
  
  return (
    <div className={`w-full lg:w-80 space-y-6 ${className}`}>
      {/* Top Advertisement */}
      <div className="sticky top-24">
        {hasAdSenseClient ? (
          <AdSense 
            adSlot="1234567890" // Replace with your actual ad slot ID
            adFormat="rectangle"
            className="w-full"
            style={{ minHeight: '240px' }}
          />
        ) : (
          <AdPlaceholder 
            title="Advertisement" 
            className="w-full h-60"
            style={{ minHeight: '240px' }}
          />
        )}
      </div>

      {/* Middle Advertisement */}
      <div>
        {hasAdSenseClient ? (
          <AdSense 
            adSlot="0987654321" // Replace with your actual ad slot ID
            adFormat="rectangle"
            className="w-full"
            style={{ minHeight: '320px' }}
          />
        ) : (
          <AdPlaceholder 
            title="Advertisement" 
            className="w-full h-80"
            style={{ minHeight: '320px' }}
          />
        )}
      </div>

      {/* Bottom Advertisement */}
      <div>
        {hasAdSenseClient ? (
          <AdSense 
            adSlot="1122334455" // Replace with your actual ad slot ID
            adFormat="rectangle"
            className="w-full"
            style={{ minHeight: '240px' }}
          />
        ) : (
          <AdPlaceholder 
            title="Advertisement" 
            className="w-full h-60"
            style={{ minHeight: '240px' }}
          />
        )}
      </div>
    </div>
  );
}
