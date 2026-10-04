'use client';

import React from 'react';
import * as DropdownMenuPrimitive from '@radix-ui/react-dropdown-menu';
import { Check, ChevronRight } from 'lucide-react';
import { cn } from '@/lib/utils';

export interface DropdownMenuItem {
  label?: string;
  onClick?: () => void;
  href?: string;
  icon?: React.ReactNode;
  shortcut?: string;
  disabled?: boolean;
  destructive?: boolean;
  divider?: boolean;
  subItems?: DropdownMenuItem[];
  checked?: boolean;
}

interface DropdownMenuProps {
  trigger: React.ReactNode;
  items: DropdownMenuItem[];
  align?: 'start' | 'end' | 'center';
  sideOffset?: number;
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
}

const DropdownMenu = React.forwardRef<HTMLDivElement, DropdownMenuProps>(
  ({ trigger, items, align = 'end', sideOffset = 4, open, onOpenChange, ...props }, ref) => {
    return (
      <DropdownMenuPrimitive.Root open={open} onOpenChange={onOpenChange} {...props}>
        <DropdownMenuPrimitive.Trigger asChild>
          {trigger}
        </DropdownMenuPrimitive.Trigger>
        <DropdownMenuPrimitive.Portal>
          <DropdownMenuPrimitive.Content
            ref={ref}
            className={cn(
              'z-50 min-w-[8rem] overflow-hidden rounded-md border border-border bg-card p-1',
              'shadow-md',
              'animate-in fade-in-0 zoom-in-95',
              'data-[side=bottom]:slide-in-from-top-2',
              'data-[side=left]:slide-in-from-right-2',
              'data-[side=right]:slide-in-from-left-2',
              'data-[side=top]:slide-in-from-bottom-2'
            )}
            align={align}
            sideOffset={sideOffset}
          >
            {items.map((item, index) => {
              if (item.divider) {
                return (
                  <DropdownMenuPrimitive.Separator key={index} className="h-px bg-border my-1" />
                );
              }

              if (item.subItems && item.subItems.length > 0) {
                return (
                  <DropdownMenuPrimitive.Sub key={index}>
                    <DropdownMenuPrimitive.SubTrigger
                      className={cn(
                        'flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm',
                        'outline-none focus:bg-accent focus:text-accent-foreground',
                        'data-[state=open]:bg-accent data-[state=open]:text-accent-foreground',
                        item.disabled && 'opacity-50 pointer-events-none'
                      )}
                      disabled={item.disabled}
                    >
                      {item.icon && <span className="mr-2 h-4 w-4" aria-hidden="true">{item.icon}</span>}
                      {item.label}
                      <ChevronRight className="ml-auto h-4 w-4" aria-hidden="true" />
                    </DropdownMenuPrimitive.SubTrigger>
                    <DropdownMenuPrimitive.SubContent className="z-50 min-w-[8rem] overflow-hidden rounded-md border border-border bg-card p-1 shadow-md">
                      {item.subItems.map((subItem, subIndex) => (
                        <DropdownMenuItemComponent
                          key={subIndex}
                          item={subItem}
                        />
                      ))}
                    </DropdownMenuPrimitive.SubContent>
                  </DropdownMenuPrimitive.Sub>
                );
              }

              return <DropdownMenuItemComponent key={index} item={item} />;
            })}
          </DropdownMenuPrimitive.Content>
        </DropdownMenuPrimitive.Portal>
      </DropdownMenuPrimitive.Root>
    )
  }
)

DropdownMenu.displayName = 'DropdownMenu';

function DropdownMenuItemComponent({ item }: { item: DropdownMenuItem }) {
  const { label, onClick, href, icon, shortcut, disabled, destructive, checked } = item;

  const content = (
    <>
      {icon && <span className="mr-2 h-4 w-4" aria-hidden="true">{icon}</span>}
      {label}
      {shortcut && <span className="ml-auto text-xs text-muted-foreground" aria-hidden="true">{shortcut}</span>}
      {checked && <Check className="ml-auto h-4 w-4 text-primary" aria-hidden="true" />}
    </>
  );

  if (href) {
    return (
      <DropdownMenuPrimitive.Item asChild>
        <a
          href={href}
          className={cn(
            'flex cursor-pointer select-none items-center rounded-sm px-2 py-1.5 text-sm',
            'outline-none focus:bg-accent focus:text-accent-foreground',
            'data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
            destructive && 'text-destructive focus:text-destructive'
          )}
        >
          {content}
        </a>
      </DropdownMenuPrimitive.Item>
    );
  }

  return (
    <DropdownMenuPrimitive.Item
      onSelect={onClick}
      disabled={disabled}
      className={cn(
        'flex cursor-pointer select-none items-center rounded-sm px-2 py-1.5 text-sm',
        'outline-none focus:bg-accent focus:text-accent-foreground',
        'data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
        destructive && 'text-destructive focus:text-destructive'
      )}
    >
      {content}
    </DropdownMenuPrimitive.Item>
  );
}

export { DropdownMenu };