'use client';

import React from 'react';
import * as DialogPrimitive from '@radix-ui/react-dialog';
import { X } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ModalProps {
  open: boolean;
  onClose: () => void;
  title?: string;
  description?: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  closeOnOverlayClick?: boolean;
  closeOnEscape?: boolean;
  showCloseButton?: boolean;
  footer?: React.ReactNode;
  className?: string;
}

const sizeClasses = {
  sm: 'max-w-sm',
  md: 'max-w-md',
  lg: 'max-w-lg',
  xl: 'max-w-xl',
  full: 'max-w-4xl',
};

const Modal = React.forwardRef<HTMLDivElement, ModalProps>(
  ({ open, onClose, title, description, children, size = 'md', closeOnOverlayClick = true, showCloseButton = true, footer, className }, ref) => {
    return (
      <DialogPrimitive.Root open={open} onOpenChange={onClose}>
        <DialogPrimitive.Portal>
          <DialogPrimitive.Overlay
            className={cn(
              'fixed inset-0 z-50 bg-black/80 animate-in fade-in-0',
              'data-[state=closed]:animate-out data-[state=closed]:fade-out-0'
            )}
            onClick={closeOnOverlayClick ? onClose : undefined}
          />
          <DialogPrimitive.Content
            ref={ref}
            className={cn(
              'fixed z-50 w-full max-h-[85vh] overflow-y-auto rounded-xl bg-card border border-border shadow-xl',
              'animate-in fade-in-0 zoom-in-95 slide-in-from-bottom-4',
              'data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95 data-[state=closed]:slide-out-to-bottom-4',
              sizeClasses[size],
              className
            )}
            onOpenAutoFocus={(e) => e.preventDefault()}
            onCloseAutoFocus={(e) => e.preventDefault()}
          >
            {(title || showCloseButton) && (
              <div className="flex items-start justify-between gap-4 p-6 border-b border-border">
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
            <div className="p-6">
              {children}
            </div>
            {footer && (
              <div className="flex items-center justify-end gap-3 p-6 border-t border-border">
                {footer}
              </div>
            )}
          </DialogPrimitive.Content>
        </DialogPrimitive.Portal>
      </DialogPrimitive.Root>
    )
  }
)

Modal.displayName = 'Modal';

export { Modal };