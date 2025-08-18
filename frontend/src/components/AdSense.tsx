"use client";

import React from 'react';

interface AdSenseProps {
  adSlot: string;
  adFormat?: 'auto' | 'rectangle' | 'vertical' | 'horizontal';
  className?: string;
  style?: React.CSSProperties;
}

export default function AdSense({ 
  adSlot, 
  adFormat = 'auto', 
  className = '',
  style = {}
}: AdSenseProps) {
  const [isAdBlocked, setIsAdBlocked] = React.useState(false);

  React.useEffect(() => {
    // Check if ads are blocked
    const checkAdBlock = () => {
      const testAd = document.createElement('div');
      testAd.innerHTML = '&nbsp;';
      testAd.className = 'adsbox';
      document.body.appendChild(testAd);
      
      const isBlocked = testAd.offsetHeight === 0;
      document.body.removeChild(testAd);
      
      setIsAdBlocked(isBlocked);
    };

    checkAdBlock();
  }, []);

  if (isAdBlocked) {
    return (
      <div className={`bg-gray-100 border border-gray-200 rounded-lg p-4 text-center ${className}`} style={style}>
        <div className="text-gray-500 text-sm">
          <div className="mb-2">📢 Advertisement</div>
          <div className="text-xs">Please disable your ad blocker to see relevant ads</div>
        </div>
      </div>
    );
  }

  return (
    <div className={`ad-container ${className}`} style={style}>
      <div className="ad-label text-xs text-gray-500 mb-1">Advertisement</div>
      <ins
        className="adsbygoogle"
        style={{ display: 'block' }}
        data-ad-client={process.env.NEXT_PUBLIC_GOOGLE_ADSENSE_CLIENT_ID}
        data-ad-slot={adSlot}
        data-ad-format={adFormat}
        data-full-width-responsive="true"
      />
      <script>
        {`(adsbygoogle = window.adsbygoogle || []).push({});`}
      </script>
    </div>
  );
}

// Placeholder ad component for development/testing
export function AdPlaceholder({ 
  title = "Advertisement", 
  className = '',
  style = {}
}: { 
  title?: string; 
  className?: string;
  style?: React.CSSProperties;
}) {
  return (
    <div className={`bg-gray-50 border border-gray-200 rounded-lg p-4 text-center ${className}`} style={style}>
      <div className="text-gray-500 text-sm">
        <div className="mb-2 flex items-center justify-center">
          <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
          </svg>
          {title}
        </div>
        <div className="text-xs text-gray-400">Ad space for Google AdSense</div>
      </div>
    </div>
  );
}
