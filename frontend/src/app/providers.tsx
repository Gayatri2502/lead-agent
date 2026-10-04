'use client';

import { ReactNode, useEffect } from 'react';
import { Toaster } from '@/components/ui/composite/Toast';
import { QueryProvider } from '@/services/query-client';
import { useAppStore } from '@/store';

interface ProvidersProps {
  children: ReactNode;
}

export function Providers({ children }: ProvidersProps) {
  const { theme, sidebarCollapsed } = useAppStore();

  useEffect(() => {
    const root = document.documentElement;
    root.classList.remove('light', 'dark');
    
    if (theme === 'system') {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      root.classList.add(prefersDark ? 'dark' : 'light');
    } else {
      root.classList.add(theme);
    }
  }, [theme]);

  useEffect(() => {
    const root = document.documentElement;
    if (sidebarCollapsed) {
      root.classList.add('sidebar-collapsed');
    } else {
      root.classList.remove('sidebar-collapsed');
    }
  }, [sidebarCollapsed]);

  return (
    <QueryProvider>
      {children}
      <Toaster />
    </QueryProvider>
  );
}