import React from 'react';

interface AffiliateButtonProps {
  store: 'thomann' | 'gear4music' | 'generic';
  href: string;
  className?: string;
  storeName?: string;
  isAvailable?: boolean;
  variant?: 'default' | 'compact' | 'inline';
}

export default function AffiliateButton({ 
  store, 
  href, 
  className = '', 
  storeName, 
  isAvailable = true,
  variant = 'default'
}: AffiliateButtonProps) {
  const storeConfig = {
    thomann: {
      cssClass: 'fp-table__button--thomann',
      logo: '/thomann-100.png',
      logoAlt: 'th•mann',
      defaultName: 'Thomann'
    },
    gear4music: {
      cssClass: 'fp-table__button--gear4music',
      logo: '/gear-100.png',
      logoAlt: 'Gear4music',
      defaultName: 'Gear4music'
    },
    generic: {
      cssClass: '',
      logo: null,
      logoAlt: '',
      defaultName: storeName || 'Store'
    }
  };

  const config = storeConfig[store];
  const displayName = storeName || config.defaultName;

  // Build CSS classes
  let buttonClasses = `fp-table__button ${config.cssClass}`;
  if (!isAvailable) {
    buttonClasses += ' opacity-50 cursor-not-allowed';
  }
  if (className) {
    buttonClasses += ` ${className}`;
  }
  


  return (
    <a
      href={isAvailable ? href : undefined}
      target={isAvailable ? "_blank" : undefined}
      rel={isAvailable ? "noopener noreferrer" : undefined}
      className={buttonClasses}
      aria-disabled={!isAvailable}
    >
      <span>View Price at</span>
      {config.logo ? (
        <img 
          src={config.logo} 
          alt={config.logoAlt} 
          className="w-16 h-8 object-contain" 
          style={{ backgroundColor: 'white' }}
        />
      ) : (
        <span className="font-medium">{displayName}</span>
      )}
    </a>
  );
}

// Helper component for common usage patterns
export function ThomannButton({ href, isAvailable = true, className = '' }: {
  href: string;
  isAvailable?: boolean;
  className?: string;
}) {
  return (
    <AffiliateButton
      store="thomann"
      href={href}
      isAvailable={isAvailable}
      className={className}
    />
  );
}

export function Gear4musicButton({ href, isAvailable = true, className = '' }: {
  href: string;
  isAvailable?: boolean;
  className?: string;
}) {
  return (
    <AffiliateButton
      store="gear4music"
      href={href}
      isAvailable={isAvailable}
      className={className}
    />
  );
}

export function GenericStoreButton({ 
  href, 
  storeName, 
  isAvailable = true, 
  className = '' 
}: {
  href: string;
  storeName: string;
  isAvailable?: boolean;
  className?: string;
}) {
  return (
    <AffiliateButton
      store="generic"
      href={href}
      storeName={storeName}
      isAvailable={isAvailable}
      className={className}
    />
  );
}
