"""
Frontend Documentation

Guide to the Next.js dashboard application.
"""

## Frontend Architecture

### Directory Structure

```
frontend/
├── app/                      # Next.js 15 App Router
│   ├── (auth)/              # Auth group layout
│   ├── dashboard/           # Dashboard pages
│   ├── bookings/            # Appointments management
│   ├── customers/           # Customer management
│   ├── calls/               # Call history
│   ├── analytics/           # Analytics dashboard
│   ├── staff/               # Staff management
│   ├── settings/            # Business settings
│   ├── profile/             # User profile
│   ├── billing/             # Billing/subscription
│   ├── api-settings/        # API keys and webhooks
│   ├── layout.tsx           # Root layout
│   └── page.tsx             # Home page
│
├── components/              # Reusable React components
│   ├── ui/                 # Base UI components
│   ├── charts/             # Chart components
│   ├── forms/              # Form components
│   └── layouts/            # Layout components
│
├── hooks/                   # Custom React hooks
│   └── useApi.ts           # API data fetching hooks
│
├── lib/                     # Utilities and helpers
│   ├── api-client.ts       # Axios API client
│   ├── store.ts            # Zustand state management
│   └── utils.ts            # Helper functions
│
├── styles/                  # Global styles
│   └── globals.css         # Tailwind + custom CSS
│
├── public/                  # Static assets
│
├── next.config.ts          # Next.js configuration
├── tsconfig.json           # TypeScript configuration
├── tailwind.config.ts      # Tailwind CSS configuration
├── postcss.config.js       # PostCSS configuration
└── package.json            # Dependencies
```

## Key Technologies

- **Framework**: Next.js 15 (React 18, TypeScript)
- **Styling**: Tailwind CSS + custom CSS
- **UI Components**: Radix UI
- **API Client**: Axios
- **State Management**: Zustand
- **Data Fetching**: React Query / SWR
- **Form Handling**: React Hook Form
- **Validation**: Zod

## Pages Overview

### Unauthenticated
- `/auth/login` - Login page
- `/auth/register` - Registration page

### Authenticated
- `/` - Home/welcome
- `/dashboard` - Main dashboard with metrics
- `/bookings` - Appointment management
- `/customers` - Customer management
- `/calls` - Call history and analytics
- `/analytics` - Detailed analytics
- `/staff` - Staff/provider management
- `/settings` - Business settings
- `/profile` - User profile management
- `/billing` - Subscription and billing
- `/api-settings` - API keys and webhooks

## Development

### Setup

```bash
cd frontend
npm install
npm run dev
```

### Build

```bash
npm run build
npm start
```

### Type Checking

```bash
npm run type-check
```

### Linting

```bash
npm run lint
```

## API Integration

### Making Requests

```typescript
import { apiClient } from '@/lib/api-client';

// Fetch data
const response = await apiClient.getAppointments(businessId);

// Create data
await apiClient.createAppointment(businessId, appointmentData);

// Update data
await apiClient.updateAppointment(appointmentId, updates);

// Delete data
await apiClient.deleteAppointment(appointmentId);
```

### Using Hooks

```typescript
import { useAppointments } from '@/hooks/useApi';

export function MyComponent() {
  const { appointments, isLoading, error, fetchAppointments } = useAppointments(businessId);
  
  useEffect(() => {
    fetchAppointments();
  }, []);
  
  return (
    <>
      {isLoading && <div>Loading...</div>}
      {error && <div>Error: {error}</div>}
      {appointments.map(apt => <div>{apt.id}</div>)}
    </>
  );
}
```

## State Management

### Using Zustand Store

```typescript
import { useAppStore } from '@/lib/store';

export function MyComponent() {
  const user = useAppStore((state) => state.user);
  const setUser = useAppStore((state) => state.setUser);
  
  return <div>Hello {user?.first_name}</div>;
}
```

## Styling

### Tailwind CSS Classes

```tsx
// Dark theme (default)
<div className="bg-background text-foreground">
  <div className="bg-card border border-border p-6 rounded-lg">
    <h1 className="text-3xl font-bold text-primary">Title</h1>
    <p className="text-muted">Subtitle</p>
  </div>
</div>
```

### Custom CSS

```css
/* In styles/globals.css */
@layer components {
  .btn-primary {
    @apply px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90;
  }
}
```

## Forms

### Using React Hook Form

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const schema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
});

export function MyForm() {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema),
  });
  
  const onSubmit = (data) => console.log(data);
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('name')} />
      {errors.name && <span>{errors.name.message}</span>}
      <button type="submit">Submit</button>
    </form>
  );
}
```

## Environment Variables

Create `.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_NAME=AI Voice Receptionist
```

## Performance Tips

1. **Code Splitting**: Pages automatically code-split
2. **Image Optimization**: Use `<Image>` component from Next.js
3. **Dynamic Imports**: Use `dynamic()` for heavy components
4. **CSS Optimization**: Tailwind purges unused styles
5. **API Caching**: Implement with React Query

## Common Tasks

### Add a New Page

```bash
# Create page file
touch app/new-page/page.tsx
```

```typescript
export default function NewPage() {
  return <div>New Page</div>;
}
```

### Add a New API Call

1. Add method to `lib/api-client.ts`
2. Create hook in `hooks/useApi.ts`
3. Use hook in component

### Add New Component

```typescript
// components/MyComponent.tsx
interface MyComponentProps {
  title: string;
}

export function MyComponent({ title }: MyComponentProps) {
  return <div>{title}</div>;
}
```

## Debugging

### Browser DevTools

- React DevTools for component inspection
- Next.js DevTools for performance
- Network tab for API debugging

### Error Boundaries

```typescript
'use client';

interface Props {
  children: React.ReactNode;
}

export function ErrorBoundary({ children }: Props) {
  const [hasError, setHasError] = useState(false);
  
  useEffect(() => {
    // Error handling
  }, []);
  
  if (hasError) return <div>Something went wrong</div>;
  
  return children;
}
```

## Testing

### Setup Jest

```bash
npm install --save-dev jest @testing-library/react
```

### Write Tests

```typescript
import { render, screen } from '@testing-library/react';
import { MyComponent } from './MyComponent';

test('renders correctly', () => {
  render(<MyComponent />);
  expect(screen.getByText('text')).toBeInTheDocument();
});
```

## Deployment

### Build for Production

```bash
npm run build
npm start
```

### Environment Variables

Set in production environment:
- `NEXT_PUBLIC_API_URL`: Production API URL
- Any other needed secrets

### Docker

```dockerfile
# See docker/Dockerfile.frontend
```

## Troubleshooting

**Build fails**
- Clear `.next` folder: `rm -rf .next`
- Reinstall dependencies: `rm -rf node_modules && npm install`
- Check TypeScript errors: `npm run type-check`

**API errors**
- Check browser console
- Verify `NEXT_PUBLIC_API_URL`
- Check backend is running
- Verify CORS settings

**Performance issues**
- Use React DevTools Profiler
- Check Network tab for slow requests
- Analyze bundle with `npm run analyze`
