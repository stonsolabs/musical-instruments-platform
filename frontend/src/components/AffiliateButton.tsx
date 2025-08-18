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

  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      onClick={onClick}
      className={`block w-full text-center py-3 px-4 rounded-xl transition-colors text-sm font-medium text-white ${config.bgColor} ${config.hoverColor} ${className}`}
    >
      <div className="flex items-center justify-center gap-2">
        <Image
          src={config.logo}
          alt={config.altText}
          width={20}
          height={20}
          className="w-5 h-5"
        />
        <span>{children || config.text}</span>
      </div>
    </a>
  );
}
