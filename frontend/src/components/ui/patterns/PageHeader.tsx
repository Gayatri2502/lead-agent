'use client';

import React from 'react';
import { cn } from '@/lib/utils';
import { Text } from '../primitives';

interface BreadcrumbItem {
  label: string;
  href?: string;
  current?: boolean;
}

interface PageHeaderProps {
  title: string;
  description?: string;
  action?: React.ReactNode;
  secondaryAction?: React.ReactNode;
  breadcrumbs?: BreadcrumbItem[];
  className?: string;
}

export function PageHeader({
  title,
  description,
  action,
  secondaryAction,
  breadcrumbs,
  className,
}: PageHeaderProps) {
  return (
    <div className={cn('space-y-4', className)}>
      {breadcrumbs && breadcrumbs.length > 0 && (
        <nav className="flex items-center gap-2 text-sm" aria-label="Breadcrumb">
          <ol className="flex items-center gap-2">
            {breadcrumbs.map((item, index) => (
              <li key={item.label} className="flex items-center gap-2">
                {index > 0 && (
                  <span className="text-muted-foreground" aria-hidden="true">/</span>
                )}
                {item.href ? (
                  <a
                    href={item.href}
                    className={cn(
                      'transition-colors',
                      item.current ? 'font-medium text-foreground' : 'text-muted-foreground hover:text-foreground'
                    )}
                    aria-current={item.current ? 'page' : undefined}
                  >
                    {item.label}
                  </a>
                ) : (
                  <span className={cn('font-medium', item.current && 'text-foreground')}>
                    {item.label}
                  </span>
                )}
              </li>
            ))}
          </ol>
        </nav>
      )}
      <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
        <div className="space-y-1">
          <h1 className="text-h2 font-semibold tracking-tight">{title}</h1>
          {description && (
            <Text variant="body" color="muted">
              {description}
            </Text>
          )}
        </div>
        <div className="flex items-center gap-2 w-full sm:w-auto">
          {secondaryAction && (
            <span className="hidden sm:inline-flex">{secondaryAction}</span>
          )}
          {action}
        </div>
      </div>
    </div>
  );
}