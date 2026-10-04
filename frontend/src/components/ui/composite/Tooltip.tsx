'use client';

import React from 'react';
import * as TooltipPrimitive from '@radix-ui/react-tooltip';
import { cn } from '@/lib/utils';

interface TooltipProps {
  content: React.ReactNode;
  children: React.ReactElement;
  side?: 'top' | 'right' | 'bottom' | 'left';
  align?: 'start' | 'center' | 'end';
  delayDuration?: number;
  skipDelayDuration?: number;
  className?: string;
}

const Tooltip = React.forwardRef<HTMLDivElement, TooltipProps>(
  ({ content, children, side = 'top', align = 'center', delayDuration = 200, skipDelayDuration = 50, className, ...props }, ref) => {
    if (!React.isValidElement(children)) {
      throw new Error('Tooltip children must be a single React element');
    }

    return (
      <TooltipPrimitive.Provider delayDuration={delayDuration} skipDelayDuration={skipDelayDuration}>
        <TooltipPrimitive.Root {...props}>
          <TooltipPrimitive.Trigger asChild>
            {React.cloneElement(children, { 'data-tooltip-trigger': '' } as React.HTMLAttributes<HTMLElement>)}
          </TooltipPrimitive.Trigger>
          <TooltipPrimitive.Portal>
            <TooltipPrimitive.Content
              ref={ref}
              side={side}
              align={align}
              className={cn(
                'z-50 rounded-md bg-card border border-border px-3 py-1.5 text-xs text-foreground shadow-md',
                'animate-in fade-in-0 zoom-in-95',
                'data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95',
                'data-[side=bottom]:slide-in-from-top-2',
                'data-[side=left]:slide-in-from-right-2',
                'data-[side=right]:slide-in-from-left-2',
                'data-[side=top]:slide-in-from-bottom-2',
                className
              )}
            >
              {content}
              <TooltipPrimitive.Arrow className="fill-card border-border" />
            </TooltipPrimitive.Content>
          </TooltipPrimitive.Portal>
        </TooltipPrimitive.Root>
      </TooltipPrimitive.Provider>
    )
  }
)

Tooltip.displayName = 'Tooltip';

export { Tooltip };