'use client';

import React from 'react';
import { cn } from '@/lib/utils';
import { Card, CardHeader, CardTitle, CardContent } from '../composite';

interface ChartWrapperProps {
  title?: string;
  description?: string;
  children: React.ReactNode;
  className?: string;
  height?: number;
  action?: React.ReactNode;
}

export function ChartWrapper({
  title,
  description,
  children,
  className,
  height = 300,
  action,
}: ChartWrapperProps) {
  return (
    <Card className={cn('overflow-hidden', className)}>
      {(title || action) && (
        <CardHeader className="flex flex-row items-center justify-between">
          <div>
            {title && <CardTitle>{title}</CardTitle>}
            {description && <p className="text-sm text-muted-foreground mt-1">{description}</p>}
          </div>
          {action}
        </CardHeader>
      )}
      <CardContent className="p-0">
        <div style={{ height }} className="w-full">
          {children}
        </div>
      </CardContent>
    </Card>
  );
}