'use client';

import React, { useState, useEffect } from 'react';

interface HydrationSafeProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
  ssr?: boolean; // Whether to render on server-side
}

/**
 * HydrationSafe component prevents hydration mismatches by ensuring
 * consistent rendering between server and client
 */
export default function HydrationSafe({ 
  children, 
  fallback = null, 
  ssr = false 
}: HydrationSafeProps) {
  const [isHydrated, setIsHydrated] = useState(ssr);

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  // If not hydrated yet and SSR is disabled, show fallback
  if (!isHydrated && !ssr) {
    return <>{fallback}</>;
  }

  // If hydrated or SSR is enabled, show children
  return <>{children}</>;
}

/**
 * Hook to check if component is hydrated
 */
export function useHydration() {
  const [isHydrated, setIsHydrated] = useState(false);

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  return isHydrated;
}

/**
 * Hook to safely access browser-only APIs
 */
export function useBrowserOnly<T>(value: T, fallback: T): T {
  const isHydrated = useHydration();
  return isHydrated ? value : fallback;
}
