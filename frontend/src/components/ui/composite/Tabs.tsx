'use client';

import React from 'react';
import * as TabsPrimitive from '@radix-ui/react-tabs';
import { cn } from '@/lib/utils';

interface Tab {
  id: string;
  label: string;
  icon?: React.ReactNode;
  disabled?: boolean;
  badge?: string | number;
  content: React.ReactNode;
}

interface TabsProps {
  tabs: Tab[];
  defaultTab?: string;
  onChange?: (tab: string) => void;
  variant?: 'line' | 'pills' | 'underline';
  fullWidth?: boolean;
  className?: string;
}

const Tabs = React.forwardRef<HTMLDivElement, TabsProps>(
  ({ tabs, defaultTab, onChange, variant = 'line', fullWidth = false, className, ...props }) => {
    const [activeTab, setActiveTab] = React.useState(defaultTab || tabs[0]?.id || '');

    const handleTabChange = (value: string) => {
      setActiveTab(value);
      onChange?.(value);
    };

    return (
      <TabsPrimitive.Root value={activeTab} onValueChange={handleTabChange} {...props}>
        <TabsPrimitive.List
          className={cn(
            'inline-flex h-10 items-center justify-center gap-1 bg-muted p-1 rounded-md',
            variant === 'line' && 'bg-transparent p-0',
            variant === 'pills' && '',
            variant === 'underline' && 'bg-transparent p-0',
            fullWidth && 'w-full',
            className
          )}
          aria-label="Tabs"
        >
          {tabs.map((tab) => (
            <TabsPrimitive.Trigger
              key={tab.id}
              value={tab.id}
              disabled={tab.disabled}
              className={cn(
                'inline-flex items-center justify-center gap-1.5 whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium transition-all duration-fast',
                'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
                'disabled:pointer-events-none disabled:opacity-50',
                variant === 'line' &&
                  'bg-transparent text-muted-foreground hover:text-foreground data-[state=active]:text-foreground data-[state=active]:shadow-sm',
                variant === 'pills' &&
                  'text-muted-foreground data-[state=active]:bg-card data-[state=active]:text-foreground data-[state=active]:shadow-sm',
                variant === 'underline' &&
                  'bg-transparent text-muted-foreground hover:text-foreground data-[state=active]:text-foreground data-[state=active]:border-b-2 data-[state=active]:border-primary',
                fullWidth && 'flex-1'
              )}
            >
              {tab.icon && <span aria-hidden="true">{tab.icon}</span>}
              {tab.label}
              {tab.badge && (
                <span className="px-1.5 py-0.5 text-xs rounded-full bg-primary/20 text-primary">
                  {tab.badge}
                </span>
              )}
            </TabsPrimitive.Trigger>
          ))}
        </TabsPrimitive.List>
        <div className="mt-4">
          {tabs.map((tab) => (
            <TabsPrimitive.Content
              key={tab.id}
              value={tab.id}
              className={cn(
                'animate-in fade-in-0 zoom-in-95',
                'data-[state=active]:animate-in data-[state=active]:fade-in-0 data-[state=active]:zoom-in-95',
                'data-[state=inactive]:animate-out data-[state=inactive]:fade-out-0 data-[state=inactive]:zoom-out-95'
              )}
            >
              {tab.content}
            </TabsPrimitive.Content>
          ))}
        </div>
      </TabsPrimitive.Root>
    )
  }
)

Tabs.displayName = 'Tabs';

export { Tabs };