'use client';

import React from 'react';
import * as SwitchPrimitive from '@radix-ui/react-switch';
import { cn } from '@/lib/utils';

export interface SwitchProps extends React.ComponentPropsWithoutRef<typeof SwitchPrimitive.Root> {
  label?: string;
  description?: string;
  error?: string;
}

const Switch = React.forwardRef<
  React.ElementRef<typeof SwitchPrimitive.Root>,
  SwitchProps
>(({ className, label, description, error, disabled, required, id, ...props }, ref) => {
  const switchId = id || `switch-${Math.random().toString(36).substring(2, 9)}`;
  const descriptionId = description ? `${switchId}-description` : undefined;
  const errorId = error ? `${switchId}-error` : undefined;

  return (
    <div className="flex items-center gap-3">
      <SwitchPrimitive.Root
        ref={ref}
        id={switchId}
        required={required}
        disabled={disabled}
        aria-describedby={descriptionId}
        aria-errormessage={errorId}
        className={cn(
          'peer relative inline-flex h-6 w-11 shrink-0 cursor-pointer items-center rounded-full',
          'border-2 border-input bg-background',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
          'disabled:cursor-not-allowed disabled:opacity-50',
          'data-[state=checked]:bg-primary data-[state=checked]:border-primary',
          'transition-colors duration-fast',
          error && 'border-destructive data-[state=checked]:border-destructive data-[state=checked]:bg-destructive',
          className
        )}
        {...props}
      >
        <SwitchPrimitive.Thumb
          className={cn(
            'pointer-events-none block h-5 w-5 rounded-full bg-foreground shadow-lg ring-0',
            'data-[state=checked]:translate-x-5',
            'transition-transform duration-fast ease-spring'
          )}
        />
      </SwitchPrimitive.Root>
      {(label || description) && (
        <div className="min-w-0 flex-1">
          {label && (
            <label htmlFor={switchId} className="block text-label peer-disabled:opacity-50">
              {label}
              {required && <span className="text-destructive ml-1" aria-hidden="true">*</span>}
            </label>
          )}
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
      )}
    </div>
  )
})

Switch.displayName = 'Switch';

export { Switch };