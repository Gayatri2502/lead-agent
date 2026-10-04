'use client';

import React from 'react';
import { cn } from '@/lib/utils';
import { Card, CardContent } from '../composite';
import { Text } from '../primitives';
import { Flex } from '../primitives';

interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description?: string;
  action?: React.ReactNode;
  secondaryAction?: React.ReactNode;
  illustration?: 'default' | 'search' | 'filter' | 'offline';
  className?: string;
}

const illustrations = {
  default: (
    <svg className="h-16 w-16 text-muted-foreground/50" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  ),
  search: (
    <svg className="h-16 w-16 text-muted-foreground/50" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
    </svg>
  ),
  filter: (
    <svg className="h-16 w-16 text-muted-foreground/50" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
    </svg>
  ),
  offline: (
    <svg className="h-16 w-16 text-muted-foreground/50" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z" />
    </svg>
  ),
};

export function EmptyState({
  icon,
  title,
  description,
  action,
  secondaryAction,
  illustration = 'default',
  className,
}: EmptyStateProps) {
  return (
    <Card className={cn('text-center py-12', className)}>
      <CardContent className="p-6">
        <Flex direction="col" align="center" gap={4} className="w-full">
          {icon || illustrations[illustration]}
          <div className="space-y-2">
            <Text variant="h4" className="text-foreground">
              {title}
            </Text>
            {description && (
              <Text variant="body" color="muted" className="max-w-sm mx-auto">
                {description}
              </Text>
            )}
          </div>
          {(action || secondaryAction) && (
            <Flex align="center" gap={2} className="pt-2">
              {secondaryAction && <span>{secondaryAction}</span>}
              {action}
            </Flex>
          )}
        </Flex>
      </CardContent>
    </Card>
  );
}