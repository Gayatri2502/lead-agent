'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useState, ReactNode } from 'react';

const QUERY_CLIENT_OPTIONS = {
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      gcTime: 1000 * 60 * 30, // 30 minutes
      retry: 1,
      refetchOnWindowFocus: false,
      refetchOnReconnect: true,
    },
    mutations: {
      retry: 0,
    },
  },
};

export function createQueryClient() {
  return new QueryClient(QUERY_CLIENT_OPTIONS);
}

interface QueryProviderProps {
  children: ReactNode;
}

export function QueryProvider({ children }: QueryProviderProps) {
  const [queryClient] = useState(() => createQueryClient());

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}

/**
 * Query keys for consistent caching
 */
export const queryKeys = {
  // Auth
  auth: ['auth'] as const,
  user: (id: number) => ['user', id] as const,
  business: (id: number) => ['business', id] as const,

  // Customers
  customers: (businessId: number, params?: any) =>
    ['customers', businessId, params] as const,
  customer: (id: number) => ['customer', id] as const,

  // Appointments
  appointments: (businessId: number, params?: any) =>
    ['appointments', businessId, params] as const,
  appointment: (id: number) => ['appointment', id] as const,

  // Calls
  calls: (businessId: number, params?: any) =>
    ['calls', businessId, params] as const,
  call: (id: number) => ['call', id] as const,
  callTranscript: (id: number) => ['call', id, 'transcript'] as const,
  callRecording: (id: number) => ['call', id, 'recording'] as const,

  // Analytics
  analyticsOverview: (businessId: number, params?: any) =>
    ['analytics', 'overview', businessId, params] as const,
  callAnalytics: (businessId: number, params?: any) =>
    ['analytics', 'calls', businessId, params] as const,
  appointmentAnalytics: (businessId: number, params?: any) =>
    ['analytics', 'appointments', businessId, params] as const,
  customerAnalytics: (businessId: number, params?: any) =>
    ['analytics', 'customers', businessId, params] as const,
  revenueAnalytics: (businessId: number, params?: any) =>
    ['analytics', 'revenue', businessId, params] as const,

  // Staff
  staff: (businessId: number, params?: any) =>
    ['staff', businessId, params] as const,
  staffMember: (id: number) => ['staff', id] as const,

  // Services
  services: (businessId: number, params?: any) =>
    ['services', businessId, params] as const,
  service: (id: number) => ['service', id] as const,

  // Integrations
  integrations: (businessId: number) =>
    ['integrations', businessId] as const,

  // Webhooks
  webhooks: (businessId: number) =>
    ['webhooks', businessId] as const,

  // Notifications
  notifications: (businessId: number, params?: any) =>
    ['notifications', businessId, params] as const,

  // API Keys
  apiKeys: (businessId: number) =>
    ['apiKeys', businessId] as const,

  // Audit Logs
  auditLogs: (businessId: number, params?: any) =>
    ['auditLogs', businessId, params] as const,
} as const;