'use client';

import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const badgeVariants = cva(
  'inline-flex items-center gap-1.5 font-medium transition-colors duration-fast',
  {
    variants: {
      variant: {
        default: 'bg-secondary/20 text-secondary-foreground',
        success: 'bg-success-muted text-success',
        warning: 'bg-warning-muted text-warning',
        destructive: 'bg-destructive-muted text-destructive',
        info: 'bg-primary-muted text-primary',
        outline: 'border border-border bg-transparent',
      },
      size: {
        sm: 'px-2 py-0.5 text-xs gap-1',
        md: 'px-2.5 py-1 text-xs gap-1.5',
        lg: 'px-3 py-1 text-sm gap-1.5',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'md',
    },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {
  dot?: boolean;
  icon?: React.ReactNode;
}

const Badge = React.forwardRef<HTMLSpanElement, BadgeProps>(
  ({ className, variant, size, dot, icon, children, ...props }, ref) => {
    return (
      <span
        ref={ref}
        className={cn(badgeVariants({ variant, size }), className)}
        {...props}
      >
        {dot && (
          <span
            className={cn(
              'h-1.5 w-1.5 rounded-full',
              variant === 'success' && 'bg-success',
              variant === 'warning' && 'bg-warning',
              variant === 'destructive' && 'bg-destructive',
              variant === 'info' && 'bg-primary',
              variant === 'default' && 'bg-muted-foreground',
              variant === 'outline' && 'bg-current'
            )}
            aria-hidden="true"
          />
        )}
        {icon && <span aria-hidden="true">{icon}</span>}
        {children}
      </span>
    )
  }
)

Badge.displayName = 'Badge';

export { Badge };