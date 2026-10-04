'use client';

import React from 'react';
import * as DialogPrimitive from '@radix-ui/react-dialog';
import { X } from 'lucide-react';
import { cn } from '@/lib/utils';

interface DrawerProps {
  open: boolean;
  onClose: () => void;
  children: React.ReactNode;
  side?: 'left' | 'right';
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  title?: string;
  description?: string;
  showCloseButton?: boolean;
  className?: string;
}

const sideClasses = {
  left: 'left-0',
  right: 'right-0',
};

const sizeClasses = {
  sm: 'w-64',
  md: 'w-80',
  lg: 'w-96',
  xl: 'w-[32rem]',
  full: 'w-full max-w-4xl',
};

const Drawer = React.forwardRef<HTMLDivElement, DrawerProps>(
  ({ open, onClose, children, side = 'right', size = 'md', title, description, showCloseButton = true, className }, ref) => {
    return (
      <DialogPrimitive.Root open={open} onOpenChange={onClose}>
        <DialogPrimitive.Portal>
          <DialogPrimitive.Overlay
            className={cn(
              'fixed inset-0 z-50 bg-black/80 animate-in fade-in-0',
              'data-[state=closed]:animate-out data-[state=closed]:fade-out-0'
            )}
            onClick={onClose}
          />
          <DialogPrimitive.Content
            ref={ref}
            className={cn(
              'fixed z-50 h-full flex flex-col overflow-y-auto bg-card border border-border shadow-xl',
              'animate-in slide-in-from-right-full',
              'data-[state=closed]:animate-out data-[state=closed]:slide-out-to-right-full',
              sideClasses[side],
              sizeClasses[size],
              className
            )}
            onOpenAutoFocus={(e) => e.preventDefault()}
            onCloseAutoFocus={(e) => e.preventDefault()}
          >
            {(title || showCloseButton) && (
              <div className="flex items-start justify-between gap-4 p-6 border-b border-border flex-shrink-0">
                <div className="flex-1">
                  {title && (
                    <DialogPrimitive.Title className="text-h4 font-semibold">
                      {title}
                    </DialogPrimitive.Title>
                  )}
                  {description && (
                    <DialogPrimitive.Description className="mt-1 text-sm text-muted-foreground">
                      {description}
                    </DialogPrimitive.Description>
                  )}
                </div>
                {showCloseButton && (
                  <DialogPrimitive.Close asChild>
                    <button
                      className="rounded-md p-1 text-muted-foreground hover:text-foreground hover:bg-muted transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                      aria-label="Close"
                    >
                      <X className="h-4 w-4" aria-hidden="true" />
                    </button>
                  </DialogPrimitive.Close>
                )}
              </div>
            )}
            <div className="flex-1 p-6 overflow-y-auto">
              {children}
            </div>
          </DialogPrimitive.Content>
        </DialogPrimitive.Portal>
      </DialogPrimitive.Root>
    )
  }
)

Drawer.displayName = 'Drawer';

export { Drawer };