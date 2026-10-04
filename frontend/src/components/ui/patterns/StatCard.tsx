'use client';

import React from 'react';
import { cn } from '@/lib/utils';
import { Card, CardContent } from '../composite';
import { Text } from '../primitives';
import { Flex } from '../primitives';

interface StatCardProps {
  label: string;
  value: string | number;
  change?: {
    value: number;
    label: string;
    trend: 'up' | 'down' | 'neutral';
  };
  icon?: React.ReactNode;
  iconBg?: 'primary' | 'success' | 'warning' | 'destructive';
  loading?: boolean;
  className?: string;
}

const trendColors = {
  up: 'text-success',
  down: 'text-destructive',
  neutral: 'text-muted-foreground',
};

const iconBgClasses = {
  primary: 'bg-primary/20 text-primary',
  success: 'bg-success/20 text-success',
  warning: 'bg-warning/20 text-warning',
  destructive: 'bg-destructive/20 text-destructive',
};

export function StatCard({
  label,
  value,
  change,
  icon,
  iconBg = 'primary',
  loading,
  className,
}: StatCardProps) {
  if (loading) {
    return (
      <Card className={cn('animate-pulse', className)}>
        <CardContent className="p-6">
          <div className="h-4 w-3/4 bg-muted rounded mb-2" />
          <div className="h-8 w-1/2 bg-muted rounded mb-2" />
          {change && <div className="h-3 w-1/3 bg-muted rounded" />}
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={cn('hover:border-primary/50 transition-colors', className)}>
      <CardContent className="p-6">
        <Flex justify="between" align="start" className="mb-4">
          <Text variant="label" color="muted">
            {label}
          </Text>
          {icon && (
            <div className={cn('w-10 h-10 rounded-lg flex items-center justify-center', iconBgClasses[iconBg])}>
              {icon}
            </div>
          )}
        </Flex>
        <Text variant="data-lg" className="mb-2">
          {value}
        </Text>
{change && (
            <Flex style={{ gap: '0.375rem' }} align="center">
            <Text
              variant="label-sm"
              className={cn(trendColors[change.trend], 'flex items-center gap-1')}
            >
              {change.trend === 'up' && <span aria-hidden="true">↑</span>}
              {change.trend === 'down' && <span aria-hidden="true">↓</span>}
              {change.trend === 'neutral' && <span aria-hidden="true">→</span>}
              {Math.abs(change.value)}% {change.label}
            </Text>
          </Flex>
        )}
      </CardContent>
    </Card>
  );
}