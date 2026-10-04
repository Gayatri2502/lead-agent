'use client';

import React from 'react';
import { cn } from '@/lib/utils';
import { Text } from '../primitives';
import { Flex } from '../primitives';

interface LoadingStateProps {
  variant?: 'spinner' | 'skeleton' | 'dots' | 'pulse';
  size?: 'sm' | 'md' | 'lg';
  text?: string;
  overlay?: boolean;
  className?: string;
}

const spinnerSizes = {
  sm: 'h-4 w-4',
  md: 'h-8 w-8',
  lg: 'h-12 w-12',
};

const textSizes = {
  sm: 'text-sm',
  md: 'text-base',
  lg: 'text-lg',
};

export function LoadingState({ variant = 'spinner', size = 'md', text, overlay, className }: LoadingStateProps) {
  const baseStyles = cn(
    'flex items-center justify-center',
    overlay && 'fixed inset-0 z-50 bg-background/80 backdrop-blur-sm',
    className
  );

  const spinner = (
    <svg
      className={cn('animate-spin text-primary', spinnerSizes[size])}
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      aria-hidden="true"
    >
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      />
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      />
    </svg>
  );

  const dots = (
    <Flex style={{ gap: '0.375rem' }} aria-hidden="true">
      <span className={cn('h-2 w-2 rounded-full bg-primary animate-bounce', 'animation-delay-0', textSizes[size])} />
      <span className={cn('h-2 w-2 rounded-full bg-primary animate-bounce', 'animation-delay-100', textSizes[size])} />
      <span className={cn('h-2 w-2 rounded-full bg-primary animate-bounce', 'animation-delay-200', textSizes[size])} />
    </Flex>
  );

  const pulse = (
    <div
      className={cn('animate-pulse rounded', spinnerSizes[size])}
      style={{ background: 'linear-gradient(90deg, var(--color-bg-tertiary) 25%, var(--color-bg-secondary) 50%, var(--color-bg-tertiary) 75%)', backgroundSize: '200% 100%' }}
      aria-hidden="true"
    />
  );

  const skeleton = (
    <div className="space-y-3 w-full max-w-md" aria-hidden="true">
      <div className="h-4 bg-muted rounded animate-pulse" style={{ width: '60%' }} />
      <div className="h-4 bg-muted rounded animate-pulse" style={{ width: '40%' }} />
      <div className="h-4 bg-muted rounded animate-pulse" style={{ width: '80%' }} />
    </div>
  );

  return (
    <div className={baseStyles} role="status" aria-live="polite" aria-label={text || 'Loading'}>
      <Flex direction="col" align="center" gap={3}>
        {variant === 'spinner' && spinner}
        {variant === 'dots' && dots}
        {variant === 'pulse' && pulse}
        {variant === 'skeleton' && skeleton}
        {text && <Text variant="body" color="muted" className={textSizes[size]}>{text}</Text>}
      </Flex>
    </div>
  );
}