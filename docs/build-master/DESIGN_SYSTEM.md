# Design System: AI Voice Receptionist Dashboard

## Design Tokens

### Colors (CSS Custom Properties)

```css
:root {
  /* ===== SEMANTIC COLORS ===== */
  /* Backgrounds */
  --color-bg-primary: #000000;
  --color-bg-secondary: #0a0a0a;
  --color-bg-tertiary: #111111;
  --color-bg-card: #111111;
  --color-bg-card-hover: #1a1a1a;
  --color-bg-overlay: rgba(0, 0, 0, 0.8);
  --color-bg-modal: #111111;
  --color-bg-toast: #1a1a1a;
  --color-bg-input: #1a1a1a;
  --color-bg-input-hover: #222222;
  --color-bg-input-focus: #222222;

  /* Foregrounds */
  --color-fg-primary: #ffffff;
  --color-fg-secondary: #e5e5e5;
  --color-fg-tertiary: #a3a3a3;
  --color-fg-muted: #737373;
  --color-fg-inverse: #000000;
  --color-fg-disabled: #525252;

  /* Primary - Actions, Links, Focus */
  --color-primary: #3b82f6;
  --color-primary-hover: #2563eb;
  --color-primary-active: #1d4ed8;
  --color-primary-muted: rgba(59, 130, 246, 0.12);
  --color-primary-fg: #ffffff;

  /* Success - Positive, Confirmed, Complete */
  --color-success: #22c55e;
  --color-success-hover: #16a34a;
  --color-success-muted: rgba(34, 197, 94, 0.12);
  --color-success-fg: #ffffff;

  /* Warning - Attention, Pending */
  --color-warning: #f59e0b;
  --color-warning-hover: #d97706;
  --color-warning-muted: rgba(245, 158, 11, 0.12);
  --color-warning-fg: #000000;

  /* Destructive - Errors, Delete, Critical */
  --color-destructive: #ef4444;
  --color-destructive-hover: #dc2626;
  --color-destructive-muted: rgba(239, 68, 68, 0.12);
  --color-destructive-fg: #ffffff;

  /* Borders */
  --color-border-primary: #222222;
  --color-border-secondary: #2a2a2a;
  --color-border-focus: #3b82f6;
  --color-border-error: #ef4444;
  --color-border-success: #22c55e;

  /* Rings/Focus */
  --color-ring: #3b82f6;
  --color-ring-offset: #000000;
  --color-ring-error: #ef4444;
  --color-ring-success: #22c55e;

  /* ===== CHART COLORS (Categorical) ===== */
  --chart-1: #3b82f6;
  --chart-2: #22c55e;
  --chart-3: #f59e0b;
  --chart-4: #ef4444;
  --chart-5: #8b5cf6;
  --chart-6: #06b6d4;
  --chart-7: #f97316;
  --chart-8: #ec4899;

  /* ===== LIGHT MODE (Future) ===== */
  /* [data-theme="light"] { ... } */
}
```

### Typography Scale (Fluid, Clamp-Based)

```css
:root {
  /* Base */
  --font-sans: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', 'SF Mono', 'Fira Code', monospace;

  /* Fluid Type Scale (clamp: min, preferred, max) */
  --text-xs: clamp(0.7rem, 0.68rem + 0.1vw, 0.75rem);     /* 11-12px */
  --text-sm: clamp(0.8125rem, 0.78rem + 0.16vw, 0.875rem); /* 13-14px */
  --text-base: clamp(0.9375rem, 0.89rem + 0.24vw, 1rem);   /* 15-16px */
  --text-lg: clamp(1.0625rem, 1.0rem + 0.32vw, 1.125rem);  /* 17-18px */
  --text-xl: clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem);      /* 20-24px */
  --text-2xl: clamp(1.5rem, 1.35rem + 0.75vw, 1.875rem);   /* 24-30px */
  --text-3xl: clamp(1.875rem, 1.65rem + 1.12vw, 2.25rem);  /* 30-36px */
  --text-4xl: clamp(2.25rem, 1.95rem + 1.5vw, 3rem);       /* 36-48px */

  /* Line Heights */
  --leading-tight: 1.1;
  --leading-snug: 1.375;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
  --leading-loose: 2;

  /* Font Weights */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;

  /* Letter Spacing */
  --tracking-tight: -0.02em;
  --tracking-normal: 0;
  --tracking-wide: 0.02em;
  --tracking-wider: 0.04em;
  --tracking-widest: 0.1em;
}
```

### Typography Semantic Tokens

```css
:root {
  /* Display */
  --text-display-xl: var(--text-4xl) / var(--leading-tight) var(--font-bold) var(--tracking-tight);
  --text-display-lg: var(--text-3xl) / var(--leading-tight) var(--font-bold) var(--tracking-tight);
  --text-display-md: var(--text-2xl) / var(--leading-snug) var(--font-semibold) var(--tracking-tight);
  --text-display-sm: var(--text-xl) / var(--leading-snug) var(--font-semibold) var(--tracking-tight);

  /* Headings */
  --text-h1: var(--text-3xl) / var(--leading-tight) var(--font-bold) var(--tracking-tight);
  --text-h2: var(--text-2xl) / var(--leading-snug) var(--font-semibold) var(--tracking-tight);
  --text-h3: var(--text-xl) / var(--leading-snug) var(--font-semibold) var(--tracking-tight);
  --text-h4: var(--text-lg) / var(--leading-normal) var(--font-semibold) var(--tracking-normal);
  --text-h5: var(--text-base) / var(--leading-normal) var(--font-semibold) var(--tracking-normal);
  --text-h6: var(--text-sm) / var(--leading-normal) var(--font-semibold) var(--tracking-wide);

  /* Body */
  --text-body-lg: var(--text-lg) / var(--leading-relaxed) var(--font-normal) var(--tracking-normal);
  --text-body: var(--text-base) / var(--leading-relaxed) var(--font-normal) var(--tracking-normal);
  --text-body-sm: var(--text-sm) / var(--leading-normal) var(--font-normal) var(--tracking-normal);
  --text-body-xs: var(--text-xs) / var(--leading-normal) var(--font-normal) var(--tracking-normal);

  /* Labels & UI */
  --text-label-lg: var(--text-base) / var(--leading-normal) var(--font-medium) var(--tracking-wide);
  --text-label: var(--text-sm) / var(--leading-normal) var(--font-medium) var(--tracking-wide);
  --text-label-sm: var(--text-xs) / var(--leading-normal) var(--font-medium) var(--tracking-wider);

  /* Data */
  --text-data-lg: var(--text-xl) / var(--leading-tight) var(--font-semibold) var(--tracking-tight) var(--font-mono);
  --text-data: var(--text-base) / var(--leading-normal) var(--font-medium) var(--tracking-normal) var(--font-mono);
  --text-data-sm: var(--text-sm) / var(--leading-normal) var(--font-medium) var(--tracking-normal) var(--font-mono);
  --text-data-xs: var(--text-xs) / var(--leading-normal) var(--font-normal) var(--tracking-normal) var(--font-mono);

  /* Code */
  --text-code: var(--text-sm) / var(--leading-normal) var(--font-normal) var(--font-mono);
}
```

### Spacing Scale

```css
:root {
  --space-0: 0;
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-7: 1.75rem;   /* 28px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
  --space-20: 5rem;     /* 80px */
  --space-24: 6rem;     /* 96px */

  /* Semantic Spacing */
  --space-component-xs: var(--space-2);
  --space-component-sm: var(--space-3);
  --space-component-md: var(--space-4);
  --space-component-lg: var(--space-6);
  --space-component-xl: var(--space-8);

  --space-layout-xs: var(--space-4);
  --space-layout-sm: var(--space-6);
  --space-layout-md: var(--space-8);
  --space-layout-lg: var(--space-12);
  --space-layout-xl: var(--space-16);
}
```

### Border Radius

```css
:root {
  --radius-none: 0;
  --radius-sm: 0.25rem;   /* 4px */
  --radius-md: 0.375rem;  /* 6px */
  --radius-lg: 0.5rem;    /* 8px */
  --radius-xl: 0.75rem;   /* 12px */
  --radius-2xl: 1rem;     /* 16px */
  --radius-full: 9999px;

  /* Semantic */
  --radius-input: var(--radius-md);
  --radius-button: var(--radius-md);
  --radius-card: var(--radius-lg);
  --radius-modal: var(--radius-xl);
  --radius-badge: var(--radius-full);
}
```

### Shadows

```css
:root {
  --shadow-xs: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
  --shadow-2xl: 0 25px 50px -12px rgb(0 0 0 / 0.25);

  /* Semantic */
  --shadow-dropdown: var(--shadow-lg);
  --shadow-tooltip: var(--shadow-md);
  --shadow-modal: var(--shadow-xl);
  --shadow-toast: var(--shadow-xl);
  --shadow-card-hover: var(--shadow-md);
}
```

### Transitions & Motion

```css
:root {
  /* Durations */
  --duration-instant: 0ms;
  --duration-fast: 100ms;
  --duration-normal: 200ms;
  --duration-slow: 300ms;
  --duration-slower: 500ms;

  /* Easings */
  --ease-linear: linear;
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);

  /* Semantic */
  --transition-fast: var(--duration-fast) var(--ease-out);
  --transition-normal: var(--duration-normal) var(--ease-out);
  --transition-slow: var(--duration-slow) var(--ease-in-out);
  --transition-spring: var(--duration-slow) var(--ease-spring);
}
```

### Breakpoints

```css
:root {
  --bp-xs: 320px;
  --bp-sm: 375px;
  --bp-md: 768px;
  --bp-lg: 1024px;
  --bp-xl: 1440px;
  --bp-2xl: 1920px;

  /* Container Max Widths */
  --container-sm: 640px;
  --container-md: 768px;
  --container-lg: 1024px;
  --container-xl: 1280px;
  --container-2xl: 1536px;
}
```

### Z-Index Scale

```css
:root {
  --z-hide: -1;
  --z-base: 0;
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-fixed: 300;
  --z-modal-backdrop: 400;
  --z-modal: 500;
  --z-popover: 600;
  --z-tooltip: 700;
  --z-toast: 800;
  --z-tooltip-hover: 900;
}
```

---

## Component API Reference

### Primitive Components

#### Box
```tsx
interface BoxProps extends React.HTMLAttributes<HTMLDivElement> {
  as?: React.ElementType;
  p?: keyof typeof spacing;
  px?: keyof typeof spacing;
  py?: keyof typeof spacing;
  m?: keyof typeof spacing;
  mx?: keyof typeof spacing;
  my?: keyof typeof spacing;
  gap?: keyof typeof spacing;
  flex?: boolean | 'col' | 'row';
  wrap?: boolean;
  align?: 'start' | 'center' | 'end' | 'stretch';
  justify?: 'start' | 'center' | 'end' | 'between' | 'around';
}
```

#### Text
```tsx
interface TextProps extends React.HTMLAttributes<HTMLParagraphElement> {
  as?: 'p' | 'span' | 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6' | 'label' | 'dt' | 'dd';
  variant?: 'display-xl' | 'display-lg' | 'display-md' | 'display-sm' |
            'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6' |
            'body-lg' | 'body' | 'body-sm' | 'body-xs' |
            'label-lg' | 'label' | 'label-sm' |
            'data-lg' | 'data' | 'data-sm' | 'data-xs' |
            'code';
  weight?: 'normal' | 'medium' | 'semibold' | 'bold';
  color?: 'primary' | 'secondary' | 'tertiary' | 'muted' | 'inverse' | 'success' | 'warning' | 'destructive';
  truncate?: boolean;
  inline?: boolean;
}
```

#### Flex
```tsx
interface FlexProps extends BoxProps {
  direction?: 'row' | 'col' | 'row-reverse' | 'col-reverse';
  align?: 'start' | 'center' | 'end' | 'stretch' | 'baseline';
  justify?: 'start' | 'center' | 'end' | 'between' | 'around' | 'evenly';
  gap?: keyof typeof spacing;
  wrap?: boolean;
  flex?: number | string;
}
```

#### Grid
```tsx
interface GridProps extends BoxProps {
  columns?: number | string;
  gap?: keyof typeof spacing;
  rows?: number | string;
  autoFlow?: 'row' | 'col' | 'dense' | 'row-dense' | 'col-dense';
}
```

### Composite Components

#### Button
```tsx
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'destructive' | 'success';
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  loading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
  asChild?: boolean; // For Link wrapping
}
```

**Variants:**
| Variant | Background | Text | Border | Use Case |
|---------|-----------|------|--------|----------|
| primary | Primary | Primary-fg | None | Primary actions |
| secondary | Secondary-muted | Primary | None | Secondary actions |
| outline | Transparent | Primary | Primary | Tertiary actions |
| ghost | Transparent | Primary | None | Subtle actions |
| destructive | Destructive | Destructive-fg | None | Delete, remove |
| success | Success | Success-fg | None | Confirm, approve |

**Sizes:**
| Size | Padding | Font | Height |
|------|---------|------|--------|
| xs | 4px 8px | label-sm | 28px |
| sm | 6px 12px | label-sm | 32px |
| md | 8px 16px | label | 40px |
| lg | 10px 20px | label-lg | 44px |
| xl | 12px 24px | label-lg | 48px |

#### Input
```tsx
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  leftElement?: React.ReactNode;
  rightElement?: React.ReactNode;
}
```

#### Textarea
```tsx
interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  hint?: string;
  autoResize?: boolean;
  minRows?: number;
  maxRows?: number;
}
```

#### Select
```tsx
interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
  hint?: string;
  placeholder?: string;
  options: { value: string; label: string; disabled?: boolean }[];
}
```

#### Checkbox
```tsx
interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label: string;
  description?: string;
  error?: string;
  indeterminate?: boolean;
}
```

#### RadioGroup / Radio
```tsx
interface RadioGroupProps {
  label?: string;
  error?: string;
  hint?: string;
  options: { value: string; label: string; description?: string; disabled?: boolean }[];
  direction?: 'vertical' | 'horizontal';
}
```

#### Switch
```tsx
interface SwitchProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string;
  description?: string;
  error?: string;
}
```

#### Card
```tsx
interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'bordered' | 'elevated';
  padding?: keyof typeof spacing;
  hover?: boolean;
  as?: React.ElementType;
}

interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {}
interface CardTitleProps extends React.HTMLAttributes<HTMLHeadingElement> {}
interface CardDescriptionProps extends React.HTMLAttributes<HTMLParagraphElement> {}
interface CardContentProps extends React.HTMLAttributes<HTMLDivElement> {}
interface CardFooterProps extends React.HTMLAttributes<HTMLDivElement> {}
```

#### Badge
```tsx
interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'default' | 'success' | 'warning' | 'destructive' | 'info' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  dot?: boolean;
  icon?: React.ReactNode;
}
```

#### Avatar
```tsx
interface AvatarProps extends React.HTMLAttributes<HTMLDivElement> {
  src?: string;
  alt?: string;
  fallback?: string; // Initials
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl';
  shape?: 'circle' | 'square';
}
```

**Sizes:** xs=24, sm=32, md=40, lg=48, xl=56, 2xl=72

#### DropdownMenu
```tsx
interface DropdownMenuProps {
  trigger: React.ReactNode;
  items: DropdownMenuItem[];
  align?: 'start' | 'end';
  sideOffset?: number;
}

interface DropdownMenuItem {
  label: string;
  onClick?: () => void;
  href?: string;
  icon?: React.ReactNode;
  shortcut?: string;
  disabled?: boolean;
  destructive?: boolean;
  divider?: boolean;
  subItems?: DropdownMenuItem[];
}
```

#### Tabs
```tsx
interface TabsProps {
  tabs: Tab[];
  defaultTab?: string;
  onChange?: (tab: string) => void;
  variant?: 'line' | 'pills' | 'underline';
  fullWidth?: boolean;
}

interface Tab {
  id: string;
  label: string;
  icon?: React.ReactNode;
  disabled?: boolean;
  badge?: string | number;
  content: React.ReactNode;
}
```

#### Table
```tsx
interface TableProps<T> {
  columns: Column<T>[];
  data: T[];
  keyAccessor: (item: T) => string | number;
  rowKey?: string;
  sortable?: boolean;
  filterable?: boolean;
  pagination?: PaginationConfig;
  selection?: SelectionConfig<T>;
  emptyState?: React.ReactNode;
  loading?: boolean;
  rowClassName?: (item: T) => string;
  onRowClick?: (item: T) => void;
}

interface Column<T> {
  key: string;
  header: string;
  accessor: keyof T | ((item: T) => React.ReactNode);
  width?: string;
  minWidth?: string;
  align?: 'left' | 'center' | 'right';
  sortable?: boolean;
  filterable?: boolean;
  render?: (value: any, item: T) => React.ReactNode;
  cellClassName?: string;
  headerClassName?: string;
}
```

#### Modal / Dialog
```tsx
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
}
```

#### Drawer
```tsx
interface DrawerProps {
  open: boolean;
  onClose: () => void;
  children: React.ReactNode;
  side?: 'left' | 'right';
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  title?: string;
  description?: string;
}
```

#### Toast / Sonner Integration
```tsx
interface ToastOptions {
  title: string;
  description?: string;
  action?: { label: string; onClick: () => void };
  duration?: number;
  dismissible?: boolean;
  closeButton?: boolean;
  icon?: React.ReactNode;
}

// Usage via toast() from sonner
toast.success('Saved', { description: 'Changes saved successfully' });
toast.error('Failed', { description: 'Something went wrong' });
toast.loading('Saving...');
toast.promise(promise, { loading: 'Saving...', success: 'Saved', error: 'Failed' });
```

#### Tooltip
```tsx
interface TooltipProps {
  content: React.ReactNode;
  children: React.ReactElement;
  side?: 'top' | 'right' | 'bottom' | 'left';
  align?: 'start' | 'center' | 'end';
  delayDuration?: number;
  skipDelayDuration?: number;
}
```

#### Popover
```tsx
interface PopoverProps {
  trigger: React.ReactNode;
  content: React.ReactNode;
  side?: 'top' | 'right' | 'bottom' | 'left';
  align?: 'start' | 'center' | 'end';
  sideOffset?: number;
}
```

### Pattern Components

#### PageHeader
```tsx
interface PageHeaderProps {
  title: string;
  description?: string;
  action?: React.ReactNode; // Primary action button
  secondaryAction?: React.ReactNode;
  breadcrumbs?: BreadcrumbItem[];
}

interface BreadcrumbItem {
  label: string;
  href?: string;
  current?: boolean;
}
```

#### StatCard
```tsx
interface StatCardProps {
  label: string;
  value: string | number;
  change?: {
    value: number;
    label: string;
    trend: 'up' | 'down' | 'neutral';
  };
  icon?: React.ReactNode;
  iconBg?: 'primary' | 'success' | 'warning' | 'destructive';
  loading?: boolean;
}
```

#### EmptyState
```tsx
interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description?: string;
  action?: React.ReactNode;
  secondaryAction?: React.ReactNode;
  illustration?: 'default' | 'search' | 'filter' | 'offline';
}
```

#### LoadingState
```tsx
interface LoadingStateProps {
  variant?: 'spinner' | 'skeleton' | 'dots' | 'pulse';
  size?: 'sm' | 'md' | 'lg';
  text?: string;
  overlay?: boolean;
}
```

#### ErrorState
```tsx
interface ErrorStateProps {
  title?: string;
  message: string;
  code?: string | number;
  onRetry?: () => void;
  onDismiss?: () => void;
  illustration?: 'default' | 'not-found' | 'server' | 'network';
}
```

#### DataTable (Advanced Table)
```tsx
interface DataTableProps<T> extends TableProps<T> {
  toolbar?: React.ReactNode; // Search, filters, export
  bulkActions?: BulkAction<T>[];
  rowActions?: RowAction<T>[];
  detailPanel?: (item: T) => React.ReactNode;
  virtualized?: boolean;
  stickyHeader?: boolean;
  resizableColumns?: boolean;
  reorderableColumns?: boolean;
}

interface BulkAction<T> {
  label: string;
  icon?: React.ReactNode;
  onClick: (items: T[]) => void;
  disabled?: (items: T[]) => boolean;
  variant?: 'primary' | 'destructive';
}

interface RowAction<T> {
  label: string;
  icon?: React.ReactNode;
  onClick: (item: T) => void;
  disabled?: (item: T) => boolean;
  variant?: 'default' | 'destructive';
}
```

#### FormField (Wrapper)
```tsx
interface FormFieldProps {
  label: string;
  error?: string;
  hint?: string;
  required?: boolean;
  children: React.ReactNode;
  htmlFor?: string;
}
```

---

## Component Architecture Rules

### 1. Composition Over Configuration
- Prefer compound components (`Card.Header`, `Card.Content`, `Card.Footer`)
- Use `asChild` pattern for polymorphic components
- Slots over props for complex content

### 2. Variant System
- Use `cva` (class-variance-authority) for variant management
- Define base, variants, compound variants, default variants
- Type-safe variant props

### 3. Forward Refs
- All components forward refs to underlying DOM element
- Use `React.forwardRef` consistently

### 4. Accessibility First
- Every interactive component has:
  - Proper ARIA attributes
  - Keyboard navigation
  - Focus management
  - Screen reader support

### 5. Theme Support
- All components support light/dark via CSS variables
- No hardcoded colors in component styles
- Use semantic color tokens

### 6. Responsive by Default
- Mobile-first breakpoints
- Container queries where appropriate
- Fluid typography via clamp()

---

## Implementation Structure

```
src/components/ui/
├── primitives/
│   ├── Box.tsx
│   ├── Text.tsx
│   ├── Flex.tsx
│   ├── Grid.tsx
│   └── index.ts
├── composite/
│   ├── Button.tsx
│   ├── Input.tsx
│   ├── Textarea.tsx
│   ├── Select.tsx
│   ├── Checkbox.tsx
│   ├── RadioGroup.tsx
│   ├── Switch.tsx
│   ├── Card.tsx
│   ├── Badge.tsx
│   ├── Avatar.tsx
│   ├── DropdownMenu.tsx
│   ├── Tabs.tsx
│   ├── Table.tsx
│   ├── Modal.tsx
│   ├── Drawer.tsx
│   ├── Toast.tsx
│   ├── Tooltip.tsx
│   ├── Popover.tsx
│   └── index.ts
├── patterns/
│   ├── PageHeader.tsx
│   ├── StatCard.tsx
│   ├── EmptyState.tsx
│   ├── LoadingState.tsx
│   ├── ErrorState.tsx
│   ├── DataTable.tsx
│   ├── FormField.tsx
│   └── index.ts
├── charts/
│   ├── ChartWrapper.tsx
│   ├── LineChart.tsx
│   ├── BarChart.tsx
│   ├── PieChart.tsx
│   ├── AreaChart.tsx
│   └── index.ts
└── index.ts
```

---

## Tailwind Config Integration

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Semantic colors mapped to CSS variables
        background: 'var(--color-bg-primary)',
        foreground: 'var(--color-fg-primary)',
        card: 'var(--color-bg-card)',
        'card-foreground': 'var(--color-fg-primary)',
        primary: 'var(--color-primary)',
        'primary-foreground': 'var(--color-primary-fg)',
        secondary: 'var(--color-fg-tertiary)',
        'secondary-foreground': 'var(--color-fg-primary)',
        destructive: 'var(--color-destructive)',
        'destructive-foreground': 'var(--color-destructive-fg)',
        muted: 'var(--color-fg-muted)',
        'muted-foreground': 'var(--color-fg-tertiary)',
        accent: 'var(--color-primary)',
        'accent-foreground': 'var(--color-primary-fg)',
        success: 'var(--color-success)',
        warning: 'var(--color-warning)',
        border: 'var(--color-border-primary)',
        input: 'var(--color-bg-input)',
        ring: 'var(--color-ring)',
        // Chart colors
        'chart-1': 'var(--chart-1)',
        'chart-2': 'var(--chart-2)',
        'chart-3': 'var(--chart-3)',
        'chart-4': 'var(--chart-4)',
        'chart-5': 'var(--chart-5)',
      },
      fontFamily: {
        sans: ['var(--font-sans)'],
        mono: ['var(--font-mono)'],
      },
      fontSize: {
        'display-xl': ['var(--text-4xl)', { lineHeight: 'var(--leading-tight)', letterSpacing: 'var(--tracking-tight)', fontWeight: 'var(--font-bold)' }],
        'display-lg': ['var(--text-3xl)', { lineHeight: 'var(--leading-tight)', letterSpacing: 'var(--tracking-tight)', fontWeight: 'var(--font-bold)' }],
        'display-md': ['var(--text-2xl)', { lineHeight: 'var(--leading-snug)', letterSpacing: 'var(--tracking-tight)', fontWeight: 'var(--font-semibold)' }],
        'display-sm': ['var(--text-xl)', { lineHeight: 'var(--leading-snug)', letterSpacing: 'var(--tracking-tight)', fontWeight: 'var(--font-semibold)' }],
        h1: ['var(--text-3xl)', { lineHeight: 'var(--leading-tight)', letterSpacing: 'var(--tracking-tight)', fontWeight: 'var(--font-bold)' }],
        h2: ['var(--text-2xl)', { lineHeight: 'var(--leading-snug)', letterSpacing: 'var(--tracking-tight)', fontWeight: 'var(--font-semibold)' }],
        h3: ['var(--text-xl)', { lineHeight: 'var(--leading-snug)', letterSpacing: 'var(--tracking-tight)', fontWeight: 'var(--font-semibold)' }],
        h4: ['var(--text-lg)', { lineHeight: 'var(--leading-normal)', letterSpacing: 'var(--tracking-normal)', fontWeight: 'var(--font-semibold)' }],
        h5: ['var(--text-base)', { lineHeight: 'var(--leading-normal)', letterSpacing: 'var(--tracking-normal)', fontWeight: 'var(--font-semibold)' }],
        h6: ['var(--text-sm)', { lineHeight: 'var(--leading-normal)', letterSpacing: 'var(--tracking-wide)', fontWeight: 'var(--font-semibold)' }],
        'body-lg': ['var(--text-lg)', { lineHeight: 'var(--leading-relaxed)' }],
        body: ['var(--text-base)', { lineHeight: 'var(--leading-relaxed)' }],
        'body-sm': ['var(--text-sm)', { lineHeight: 'var(--leading-normal)' }],
        'body-xs': ['var(--text-xs)', { lineHeight: 'var(--leading-normal)' }],
        'label-lg': ['var(--text-base)', { lineHeight: 'var(--leading-normal)', letterSpacing: 'var(--tracking-wide)', fontWeight: 'var(--font-medium)' }],
        label: ['var(--text-sm)', { lineHeight: 'var(--leading-normal)', letterSpacing: 'var(--tracking-wide)', fontWeight: 'var(--font-medium)' }],
        'label-sm': ['var(--text-xs)', { lineHeight: 'var(--leading-normal)', letterSpacing: 'var(--tracking-wider)', fontWeight: 'var(--font-medium)' }],
        'data-lg': ['var(--text-xl)', { lineHeight: 'var(--leading-tight)', letterSpacing: 'var(--tracking-tight)', fontWeight: 'var(--font-semibold)', fontFamily: 'var(--font-mono)' }],
        data: ['var(--text-base)', { lineHeight: 'var(--leading-normal)', letterSpacing: 'var(--tracking-normal)', fontWeight: 'var(--font-medium)', fontFamily: 'var(--font-mono)' }],
        'data-sm': ['var(--text-sm)', { lineHeight: 'var(--leading-normal)', letterSpacing: 'var(--tracking-normal)', fontWeight: 'var(--font-medium)', fontFamily: 'var(--font-mono)' }],
        'data-xs': ['var(--text-xs)', { lineHeight: 'var(--leading-normal)', letterSpacing: 'var(--tracking-normal)', fontFamily: 'var(--font-mono)' }],
        code: ['var(--text-sm)', { lineHeight: 'var(--leading-normal)', fontFamily: 'var(--font-mono)' }],
      },
      spacing: {
        '0': 'var(--space-0)',
        '1': 'var(--space-1)',
        '2': 'var(--space-2)',
        '3': 'var(--space-3)',
        '4': 'var(--space-4)',
        '5': 'var(--space-5)',
        '6': 'var(--space-6)',
        '7': 'var(--space-7)',
        '8': 'var(--space-8)',
        '10': 'var(--space-10)',
        '12': 'var(--space-12)',
        '16': 'var(--space-16)',
        '20': 'var(--space-20)',
        '24': 'var(--space-24)',
      },
      borderRadius: {
        none: 'var(--radius-none)',
        sm: 'var(--radius-sm)',
        DEFAULT: 'var(--radius-md)',
        md: 'var(--radius-md)',
        lg: 'var(--radius-lg)',
        xl: 'var(--radius-xl)',
        '2xl': 'var(--radius-2xl)',
        full: 'var(--radius-full)',
      },
      boxShadow: {
        xs: 'var(--shadow-xs)',
        sm: 'var(--shadow-sm)',
        DEFAULT: 'var(--shadow-md)',
        md: 'var(--shadow-md)',
        lg: 'var(--shadow-lg)',
        xl: 'var(--shadow-xl)',
        '2xl': 'var(--shadow-2xl)',
        dropdown: 'var(--shadow-dropdown)',
        tooltip: 'var(--shadow-tooltip)',
        modal: 'var(--shadow-modal)',
        toast: 'var(--shadow-toast)',
      },
      transitionDuration: {
        instant: 'var(--duration-instant)',
        fast: 'var(--duration-fast)',
        normal: 'var(--duration-normal)',
        slow: 'var(--duration-slow)',
        slower: 'var(--duration-slower)',
      },
      transitionTimingFunction: {
        linear: 'var(--ease-linear)',
        in: 'var(--ease-in)',
        out: 'var(--ease-out)',
        'in-out': 'var(--ease-in-out)',
        spring: 'var(--ease-spring)',
      },
      zIndex: {
        hide: 'var(--z-hide)',
        base: 'var(--z-base)',
        dropdown: 'var(--z-dropdown)',
        sticky: 'var(--z-sticky)',
        fixed: 'var(--z-fixed)',
        'modal-backdrop': 'var(--z-modal-backdrop)',
        modal: 'var(--z-modal)',
        popover: 'var(--z-popover)',
        tooltip: 'var(--z-tooltip)',
        toast: 'var(--z-toast)',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
};

export default config;
```

---

## CSS Variables Implementation

```css
/* src/styles/tokens.css */
@layer base {
  :root {
    /* All tokens from above */
  }

  [data-theme="light"] {
    /* Light mode overrides */
    --color-bg-primary: #ffffff;
    --color-bg-secondary: #fafafa;
    --color-bg-tertiary: #f5f5f5;
    --color-bg-card: #ffffff;
    --color-bg-card-hover: #fafafa;
    --color-bg-overlay: rgba(0, 0, 0, 0.5);
    --color-bg-modal: #ffffff;
    --color-bg-toast: #fafafa;
    --color-bg-input: #fafafa;
    --color-bg-input-hover: #f5f5f5;
    --color-bg-input-focus: #ffffff;

    --color-fg-primary: #0a0a0a;
    --color-fg-secondary: #1a1a1a;
    --color-fg-tertiary: #525252;
    --color-fg-muted: #737373;
    --color-fg-inverse: #ffffff;
    --color-fg-disabled: #a3a3a3;

    --color-primary: #2563eb;
    --color-primary-hover: #1d4ed8;
    --color-primary-active: #1e40af;
    --color-primary-muted: rgba(37, 99, 235, 0.12);

    --color-success: #16a34a;
    --color-success-hover: #15803d;
    --color-success-muted: rgba(22, 163, 74, 0.12);

    --color-warning: #d97706;
    --color-warning-hover: #b45309;
    --color-warning-muted: rgba(217, 119, 6, 0.12);

    --color-destructive: #dc2626;
    --color-destructive-hover: #b91c1c;
    --color-destructive-muted: rgba(220, 38, 38, 0.12);

    --color-border-primary: #e5e5e5;
    --color-border-secondary: #d4d4d4;
    --color-border-focus: #2563eb;
    --color-border-error: #dc2626;
    --color-border-success: #16a34a;

    --color-ring: #2563eb;
    --color-ring-offset: #ffffff;
  }
}
```

---

## Usage Guidelines

### Do's
- ✅ Use semantic tokens (`bg-card`, `text-primary`, `border-border`)
- ✅ Compose with primitives (`Box`, `Flex`, `Grid`, `Text`)
- ✅ Use compound components for complex UI
- ✅ Extend via `className` prop, not style prop
- ✅ Test in both light and dark modes

### Don'ts
- ❌ Hardcode hex colors in components
- ❌ Use arbitrary values in Tailwind (`w-[347px]`)
- ❌ Create one-off styled components
- ❌ Bypass the design system for "quick fixes"
- ❌ Mix spacing scales (use tokens only)

---

## Migration Checklist

- [ ] Create `tokens.css` with all design tokens
- [ ] Update `tailwind.config.ts` to use CSS variables
- [ ] Build primitive components (`Box`, `Text`, `Flex`, `Grid`)
- [ ] Build composite components (`Button`, `Input`, `Card`, etc.)
- [ ] Build pattern components (`PageHeader`, `StatCard`, `DataTable`, etc.)
- [ ] Migrate existing pages to use design system
- [ ] Add Storybook stories for all components
- [ ] Document component APIs
- [ ] Add visual regression tests