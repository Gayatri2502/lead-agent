'use client';

import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const textVariants = cva('', {
  variants: {
    as: {
      p: '',
      span: '',
      h1: '',
      h2: '',
      h3: '',
      h4: '',
      h5: '',
      h6: '',
      dt: '',
      dd: '',
      small: '',
      code: '',
      div: '',
    },
    variant: {
      'display-xl': 'text-display-xl font-bold tracking-tight',
      'display-lg': 'text-display-lg font-bold tracking-tight',
      'display-md': 'text-display-md font-semibold tracking-tight',
      'display-sm': 'text-display-sm font-semibold tracking-tight',
      h1: 'text-h1',
      h2: 'text-h2',
      h3: 'text-h3',
      h4: 'text-h4',
      h5: 'text-h5',
      h6: 'text-h6',
      'body-lg': 'text-body-lg',
      body: 'text-body',
      'body-sm': 'text-body-sm',
      'body-xs': 'text-body-xs',
      'label-lg': 'text-label-lg',
      label: 'text-label',
      'label-sm': 'text-label-sm',
      'data-lg': 'text-data-lg font-mono',
      data: 'text-data font-mono',
      'data-sm': 'text-data-sm font-mono',
      'data-xs': 'text-data-xs font-mono',
      code: 'text-code font-mono',
    },
    weight: {
      normal: 'font-normal',
      medium: 'font-medium',
      semibold: 'font-semibold',
      bold: 'font-bold',
    },
    textColor: {
      primary: 'text-primary',
      secondary: 'text-fg-secondary',
      tertiary: 'text-fg-tertiary',
      muted: 'text-muted-foreground',
      inverse: 'text-fg-inverse',
      success: 'text-success',
      warning: 'text-warning',
      destructive: 'text-destructive',
    },
    align: {
      left: 'text-left',
      center: 'text-center',
      right: 'text-right',
      justify: 'text-justify',
    },
    decoration: {
      none: 'no-underline',
      underline: 'underline',
      'line-through': 'line-through',
    },
    transform: {
      none: 'normal-case',
      uppercase: 'uppercase',
      lowercase: 'lowercase',
      capitalize: 'capitalize',
    },
    truncate: {
      true: 'truncate',
      false: '',
    },
    inline: {
      true: 'inline',
      false: '',
    },
  },
  compoundVariants: [],
  defaultVariants: {
    as: 'p',
    variant: 'body',
    weight: 'normal',
    textColor: 'primary',
    align: 'left',
    decoration: 'none',
    transform: 'none',
    truncate: false,
    inline: false,
  },
});

export interface TextProps
  extends React.HTMLAttributes<HTMLParagraphElement>,
    VariantProps<typeof textVariants> {
  as?: 'p' | 'span' | 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6' | 'dt' | 'dd' | 'small' | 'code';
  textColor?: 'primary' | 'secondary' | 'tertiary' | 'muted' | 'inverse' | 'success' | 'warning' | 'destructive';
}

const Text = React.forwardRef<HTMLParagraphElement, TextProps>(
  ({ className, as: _as, children, ...props }, ref) => {
    const { variant, weight, textColor, align, decoration, transform, truncate, inline, ...rest } = props;

    return (
      <div
        ref={ref}
        className={cn(
          textVariants({
            as: 'div',
            variant,
            weight,
            textColor,
            align,
            decoration,
            transform,
            truncate,
            inline,
          }),
          className
        )}
        {...rest}
      >
        {children}
      </div>
    )
  }
)

Text.displayName = 'Text';

export { Text };