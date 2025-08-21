import React from 'react';
import Image from 'next/image';

interface AffiliateButtonProps {
  store: 'thomann' | 'gear4music';
  href: string;
  className?: string;
  children?: React.ReactNode;
  onClick?: (e: React.MouseEvent) => void;
}

export default function AffiliateButton({ store, href, className = '', children, onClick }: AffiliateButtonProps) {
  const storeConfig = {
    thomann: {
      bgColor: 'bg-cyan-500',
      hoverColor: 'hover:bg-cyan-600',
      text: 'View Price at th•mann',
      logo: '/thomann-100.png',
      altText: 'Thomann'
    },
    gear4music: {
      bgColor: 'bg-orange-500',
      hoverColor: 'hover:bg-orange-600',
      text: 'View Price at Gear4music',
      logo: '/gear-100.png',
      altText: 'Gear4music'
    }
  };

  const config = storeConfig[store];

  // Determine if this is a compact button (based on custom children or className)
  const isCompact = children && children !== config.text;
  const hasCustomClass = className.includes('px-') || className.includes('py-');

  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      onClick={onClick}
      className={`block text-center transition-colors font-medium text-white ${config.bgColor} ${config.hoverColor} ${
        hasCustomClass 
          ? className 
          : `w-full py-2 px-3 rounded-lg text-sm ${className}`
      }`}
    >
      <div className={`flex items-center justify-center ${isCompact && !hasCustomClass ? 'gap-1' : 'gap-2'}`}>
        {!isCompact && (
          <Image
            src={config.logo}
            alt={config.altText}
            width={16}
            height={16}
            className="w-4 h-4"
          />
        )}
        <span className={isCompact && hasCustomClass ? 'text-xs' : ''}>{children || config.text}</span>
      </div>
    </a>
  );
}
