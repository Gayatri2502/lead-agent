'use client';

import { useEffect, useState } from 'react';

/**
 * Media query hook for responsive design
 */
export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    if (typeof window === 'undefined') return;

    const media = window.matchMedia(query);
    if (media.matches !== matches) {
      setMatches(media.matches);
    }

    const listener = (event: MediaQueryListEvent) => {
      setMatches(event.matches);
    };

    media.addEventListener('change', listener);
    return () => media.removeEventListener('change', listener);
  }, [matches, query]);

  return matches;
}

/**
 * Breakpoint hooks
 */
export function useIsMobile(): boolean {
  return useMediaQuery(`(max-width: ${767}px)`);
}

export function useIsTablet(): boolean {
  return useMediaQuery(`(min-width: ${768}px) and (max-width: ${1023}px)`);
}

export function useIsDesktop(): boolean {
  return useMediaQuery(`(min-width: ${1024}px)`);
}

export function useIsLargeDesktop(): boolean {
  return useMediaQuery(`(min-width: ${1440}px)`);
}

export function useReducedMotion(): boolean {
  return useMediaQuery('(prefers-reduced-motion: reduce)');
}

export function useDarkMode(): boolean {
  return useMediaQuery('(prefers-color-scheme: dark)');
}