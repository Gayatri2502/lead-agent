'use client';

import React from 'react';
import { cn } from '@/lib/utils';
import { Card, CardContent } from '../composite';
import { Text } from '../primitives';
import { Flex } from '../primitives';
import { Button } from '../composite';

interface ErrorStateProps {
  title?: string;
  message: string;
  code?: string | number;
  onRetry?: () => void;
  onDismiss?: () => void;
  illustration?: 'default' | 'not-found' | 'server' | 'network';
  className?: string;
}

const illustrations = {
  default: (
    <svg className="h-16 w-16 text-destructive/50" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
    </svg>
  ),
  'not-found': (
    <svg className="h-16 w-16 text-muted-foreground/50" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  ),
  server: (
    <svg className="h-16 w-16 text-destructive/50" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  ),
  network: (
    <svg className="h-16 w-16 text-warning/50" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
    </svg>
  ),
};

export function ErrorState({
  title,
  message,
  code,
  onRetry,
  onDismiss,
  illustration = 'default',
  className,
}: ErrorStateProps) {
  return (
    <Card className={cn('text-center', className)}>
      <CardContent className="p-8">
        <Flex direction="col" align="center" gap={4} className="w-full">
          {illustrations[illustration]}
          <div className="space-y-2">
            {title && <Text variant="h4" className="text-foreground">{title}</Text>}
            <Text variant="body" color="muted" className="max-w-sm mx-auto">
              {message}
            </Text>
            {code && (
              <Text variant="data-sm" color="muted" className="font-mono">
                Error code: {code}
              </Text>
            )}
          </div>
          <Flex align="center" gap={2} className="pt-2">
            {onDismiss && (
              <Button variant="ghost" size="sm" onClick={onDismiss}>
                Dismiss
              </Button>
            )}
            {onRetry && (
              <Button variant="primary" size="sm" onClick={onRetry}>
                Try Again
              </Button>
            )}
          </Flex>
        </Flex>
      </CardContent>
    </Card>
  );
}