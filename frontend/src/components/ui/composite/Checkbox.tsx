'use client';

import React from 'react';
import * as CheckboxPrimitive from '@radix-ui/react-checkbox';
import { cn } from '@/lib/utils';

export interface CheckboxProps extends React.ComponentPropsWithoutRef<typeof CheckboxPrimitive.Root> {
  label: string;
  description?: string;
  error?: string;
  indeterminate?: boolean;
}

const Checkbox = React.forwardRef<
  React.ElementRef<typeof CheckboxPrimitive.Root>,
  CheckboxProps
>(({ className, label, description, error, disabled, required, id, indeterminate, ...props }, ref) => {
  const checkboxId = id || `checkbox-${Math.random().toString(36).substring(2, 9)}`;
  const descriptionId = description ? `${checkboxId}-description` : undefined;
  const errorId = error ? `${checkboxId}-error` : undefined;

  return (
    <div className="flex items-start gap-3">
      <CheckboxPrimitive.Root
        ref={ref}
        id={checkboxId}
        required={required}
        disabled={disabled}
        checked={indeterminate ? 'indeterminate' : props.checked}
        aria-describedby={descriptionId}
        aria-errormessage={errorId}
        className={cn(
          'peer h-4 w-4 shrink-0 rounded-sm border border-input',
          'bg-background text-primary',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
          'disabled:cursor-not-allowed disabled:opacity-50',
          'data-[state=checked]:bg-primary data-[state=checked]:border-primary',
          'transition-colors duration-fast',
          error && 'border-destructive data-[state=checked]:border-destructive data-[state=checked]:bg-destructive',
          className
        )}
      >
        <CheckboxPrimitive.Indicator className={cn(
          'flex items-center justify-center text-primary-foreground',
          'data-[state=checked]:animate-in data-[state=checked]:zoom-in-95 data-[state=checked]:fade-in',
          'data-[state=unchecked]:animate-out data-[state=unchecked]:zoom-out-95 data-[state=unchecked]:fade-out'
        )}>
          <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3">
            <polyline points="20 6 9 17 4 12" />
          </svg>
        </CheckboxPrimitive.Indicator>
      </CheckboxPrimitive.Root>
      <div className="min-w-0 flex-1">
        <label htmlFor={checkboxId} className="block text-label peer-disabled:opacity-50">
          {label}
          {required && <span className="text-destructive ml-1" aria-hidden="true">*</span>}
        </label>
        {description && (
          <p id={descriptionId} className="mt-0.5 text-sm text-muted-foreground">
            {description}
          </p>
        )}
        {error && (
          <p id={errorId} className="mt-1.5 text-sm text-destructive" role="alert">
            {error}
          </p>
        )}
      </div>
    </div>
  )
})

Checkbox.displayName = 'Checkbox';

export { Checkbox };