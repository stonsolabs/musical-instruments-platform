"use client";

import React from 'react';
import AdSense, { AdPlaceholder } from './AdSense';

interface AdSidebarProps {
  className?: string;
  compact?: boolean;
}

export default function AdSidebar({ className = '', compact = false }: AdSidebarProps) {
  const hasAdSenseClient = process.env.NEXT_PUBLIC_GOOGLE_ADSENSE_CLIENT_ID;
  
  if (compact) {
    return (
      <div className={`w-full space-y-4 ${className}`}>
        {/* Compact Top Advertisement */}
        <div>
          {hasAdSenseClient ? (
            <AdSense 
              adSlot="1234567890" // Replace with your actual ad slot ID
              adFormat="rectangle"
              className="w-full"
              style={{ minHeight: '200px' }}
            />
          ) : (
            <AdPlaceholder 
              title="Advertisement" 
              className="w-full h-48"
              style={{ minHeight: '200px' }}
            />
          )}
        </div>

        {/* Compact Bottom Advertisement */}
        <div>
          {hasAdSenseClient ? (
            <AdSense 
              adSlot="0987654321" // Replace with your actual ad slot ID
              adFormat="rectangle"
              className="w-full"
              style={{ minHeight: '200px' }}
            />
          ) : (
            <AdPlaceholder 
              title="Advertisement" 
              className="w-full h-48"
              style={{ minHeight: '200px' }}
            />
          )}
        </div>
      </div>
    );
  }

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
            style={{ minHeight: '280px' }}
          />
        ) : (
          <AdPlaceholder 
            title="Advertisement" 
            className="w-full h-70"
            style={{ minHeight: '280px' }}
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
