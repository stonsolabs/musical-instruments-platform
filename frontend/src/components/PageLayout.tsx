"use client";

import React from 'react';
import AdSidebar from './AdSidebar';

interface PageLayoutProps {
  children: React.ReactNode;
  className?: string;
  showSidebar?: boolean;
}

export default function PageLayout({ 
  children, 
  className = '',
  showSidebar = true 
}: PageLayoutProps) {
  return (
    <div className={`max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 ${className}`}>
      <div className="flex flex-col lg:flex-row gap-8">
        {/* Main Content */}
        <div className="flex-1 min-w-0">
          {children}
        </div>

        {/* Sidebar with Ads */}
        {showSidebar && (
          <div className="lg:flex-shrink-0">
            <AdSidebar />
          </div>
        )}
      </div>
    </div>
  );
}
