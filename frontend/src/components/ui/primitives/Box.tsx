'use client';

import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const boxVariants = cva('', {
  variants: {
    as: {
      div: '',
      section: '',
      article: '',
      aside: '',
      main: '',
      header: '',
      footer: '',
      nav: '',
    },
    display: {
      block: 'block',
      flex: 'flex',
      inline: 'inline',
      'inline-flex': 'inline-flex',
      grid: 'grid',
      hidden: 'hidden',
    },
    flexDir: {
      row: 'flex-row',
      col: 'flex-col',
      'row-reverse': 'flex-row-reverse',
      'col-reverse': 'flex-col-reverse',
    },
    align: {
      start: 'items-start',
      center: 'items-center',
      end: 'items-end',
      stretch: 'items-stretch',
      baseline: 'items-baseline',
    },
    justify: {
      start: 'justify-start',
      center: 'justify-center',
      end: 'justify-end',
      between: 'justify-between',
      around: 'justify-around',
      evenly: 'justify-evenly',
    },
    gap: {
      0: 'gap-0',
      1: 'gap-1',
      2: 'gap-2',
      3: 'gap-3',
      4: 'gap-4',
      5: 'gap-5',
      6: 'gap-6',
      8: 'gap-8',
      10: 'gap-10',
      12: 'gap-12',
    },
    wrap: {
      true: 'flex-wrap',
      false: 'flex-nowrap',
    },
    flex: {
      1: 'flex-1',
      auto: 'flex-auto',
      initial: 'flex-initial',
      none: 'flex-none',
    },
    grow: {
      true: 'grow',
      false: 'grow-0',
    },
    shrink: {
      true: 'shrink',
      false: 'shrink-0',
    },
    basis: {
      full: 'basis-full',
      auto: 'basis-auto',
    },
    overflow: {
      auto: 'overflow-auto',
      hidden: 'overflow-hidden',
      scroll: 'overflow-scroll',
      visible: 'overflow-visible',
      'x-auto': 'overflow-x-auto',
      'y-auto': 'overflow-y-auto',
    },
    position: {
      static: 'static',
      relative: 'relative',
      absolute: 'absolute',
      fixed: 'fixed',
      sticky: 'sticky',
    },
    inset: {
      0: 'inset-0',
      x: 'inset-x-0',
      y: 'inset-y-0',
      start: 'inset-inline-start-0',
      end: 'inset-inline-end-0',
      top: 'top-0',
      right: 'right-0',
      bottom: 'bottom-0',
      left: 'left-0',
    },
  },
  compoundVariants: [],
  defaultVariants: {
    as: 'div',
    display: 'block',
  },
});

export interface BoxProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof boxVariants> {
  as?: 'article' | 'aside' | 'div' | 'footer' | 'header' | 'main' | 'nav' | 'section';
}

const Box = React.forwardRef<HTMLDivElement, BoxProps>(
  ({ className, as: Component = 'div', children, ...props }, ref) => {
    const { display, flexDir, align, justify, gap, wrap, flex, grow, shrink, basis, overflow, position, inset, ...rest } = props;

    return (
      <Component
        ref={ref}
        className={cn(
          boxVariants({
            display,
            flexDir,
            align,
            justify,
            gap,
            wrap,
            flex,
            grow,
            shrink,
            basis,
            overflow,
            position,
            inset,
          }),
          className
        )}
        {...rest}
      >
        {children}
      </Component>
    )
  }
)

Box.displayName = 'Box';

export { Box };