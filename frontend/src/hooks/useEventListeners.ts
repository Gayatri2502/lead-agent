'use client';

import { useEffect, useRef } from 'react';

/**
 * Detect clicks outside an element
 */
export function useOnClickOutside<T extends HTMLElement>(
  handler: (event: MouseEvent | TouchEvent) => void
): React.RefObject<T> {
  const ref = useRef<T>(null);

  useEffect(() => {
    const listener = (event: MouseEvent | TouchEvent) => {
      if (!ref.current || ref.current.contains(event.target as Node)) {
        return;
      }
      handler(event);
    };

    document.addEventListener('mousedown', listener);
    document.addEventListener('touchstart', listener);

    return () => {
      document.removeEventListener('mousedown', listener);
      document.removeEventListener('touchstart', listener);
    };
  }, [handler]);

  return ref;
}

/**
 * Detect key press
 */
export function useKeyPress(targetKey: string, handler: (event: KeyboardEvent) => void): void {
  useEffect(() => {
    const listener = (event: KeyboardEvent) => {
      if (event.key === targetKey) {
        handler(event);
      }
    };

    document.addEventListener('keydown', listener);
    return () => document.removeEventListener('keydown', listener);
  }, [targetKey, handler]);
}

/**
 * Detect escape key
 */
export function useEscapeKey(handler: () => void): void {
  useKeyPress('Escape', (event) => {
    event.preventDefault();
    handler();
  });
}

/**
 * Detect enter key
 */
export function useEnterKey(handler: () => void): void {
  useKeyPress('Enter', (event) => {
    event.preventDefault();
    handler();
  });
}