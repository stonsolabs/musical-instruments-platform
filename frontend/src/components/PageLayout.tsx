"use client";

import React from 'react';
import AdSidebar from './AdSidebar';

interface PageLayoutProps {
  children: React.ReactNode;
  className?: string;
  showSidebar?: boolean;
  layout?: 'default' | 'preserve-grid' | 'full-width';
}

export default function PageLayout({ 
  children, 
  className = '',
  showSidebar = true,
  layout = 'default'
}: PageLayoutProps) {
  if (layout === 'preserve-grid') {
    // For pages that already have their own grid layout (like products page)
    return (
      <div className={`max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 ${className}`}>
        {children}
      </div>
    );
  }

  if (layout === 'full-width') {
    // For pages that need full width without ads
    return (
      <div className={`w-full ${className}`}>
        {children}
      </div>
    );
  }

  // Default layout with sidebar
  return (
    <div className={`max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 ${className}`}>
      <div className="flex flex-col lg:flex-row gap-6 lg:gap-8">
        {/* Main Content */}
        <div className="flex-1 min-w-0">
          {children}
        </div>

        {/* Sidebar with Ads */}
        {showSidebar && (
          <div className="lg:flex-shrink-0 lg:w-80 xl:w-96">
            <AdSidebar />
          </div>
        )}
      </div>
    </div>
  );
}
