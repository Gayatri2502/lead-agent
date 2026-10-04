'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from './api-client';
import { queryKeys } from './query-client';
import type { Customer, BusinessSettings } from '@/types';

// ===== Business =====
export function useBusiness(businessId: number, enabled = true) {
  return useQuery({
    queryKey: queryKeys.business(businessId),
    queryFn: () => apiClient.getBusiness(businessId).then((res) => res.data),
    enabled: enabled && !!businessId,
  });
}

export function useBusinessSettings(businessId: number, enabled = true) {
  return useQuery({
    queryKey: ['businessSettings', businessId],
    queryFn: () => apiClient.getBusinessSettings(businessId).then((res) => res.data),
    enabled: enabled && !!businessId,
  });
}

export function useUpdateBusinessSettings(businessId: number) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<BusinessSettings>) => apiClient.updateBusinessSettings(businessId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['businessSettings', businessId] });
    },
  });
}

// ===== Customers =====
export function useCustomers(businessId: number, params: any = {}, enabled = true) {
  return useQuery({
    queryKey: queryKeys.customers(businessId, params),
    queryFn: () => apiClient.getCustomers(businessId, params).then((res) => res.data),
    enabled: enabled && !!businessId && typeof window !== 'undefined',
    placeholderData: (previousData) => previousData,
  });
}

export function useCustomer(id: number, enabled = true) {
  return useQuery({
    queryKey: queryKeys.customer(id),
    queryFn: () => apiClient.getCustomer(id).then((res) => res.data),
    enabled: enabled && !!id,
  });
}

export function useCreateCustomer(businessId: number) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<Customer>) => apiClient.createCustomer(businessId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['customers', businessId] });
    },
  });
}

export function useUpdateCustomer() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Customer> }) =>
      apiClient.updateCustomer(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['customer', id] });
      queryClient.invalidateQueries({ queryKey: ['customers'] });
    },
  });
}

export function useDeleteCustomer() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => apiClient.deleteCustomer(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['customers'] });
    },
  });
}

export function useImportCustomers(businessId: number) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (file: File) => apiClient.importCustomers(businessId, file),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['customers', businessId] });
    },
  });
}

export function useExportCustomers(businessId: number) {
  return useMutation({
    mutationFn: (params?: any) => apiClient.exportCustomers(businessId, params),
  });
}

// ===== Appointments =====
export function useAppointments(businessId: number, params: any = {}, enabled = true) {
  return useQuery({
    queryKey: queryKeys.appointments(businessId, params),
    queryFn: () => apiClient.getAppointments(businessId, params).then((res) => res.data),
    enabled: enabled && !!businessId && typeof window !== 'undefined',
    placeholderData: (previousData) => previousData,
  });
}

export function useAppointment(id: number, enabled = true) {
  return useQuery({
    queryKey: queryKeys.appointment(id),
    queryFn: () => apiClient.getAppointment(id).then((res) => res.data),
    enabled: enabled && !!id,
  });
}

export function useCreateAppointment(businessId: number) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: any) => apiClient.createAppointment(businessId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['appointments', businessId] });
    },
  });
}

export function useUpdateAppointment() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => apiClient.updateAppointment(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['appointment', id] });
      queryClient.invalidateQueries({ queryKey: ['appointments'] });
    },
  });
}

export function useDeleteAppointment() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => apiClient.deleteAppointment(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['appointments'] });
    },
  });
}

export function useCancelAppointment() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, reason }: { id: number; reason?: string }) => apiClient.cancelAppointment(id, reason),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['appointment', id] });
      queryClient.invalidateQueries({ queryKey: ['appointments'] });
    },
  });
}

export function useConfirmAppointment() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => apiClient.confirmAppointment(id),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ['appointment', id] });
      queryClient.invalidateQueries({ queryKey: ['appointments'] });
    },
  });
}

export function useCompleteAppointment() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => apiClient.completeAppointment(id),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ['appointment', id] });
      queryClient.invalidateQueries({ queryKey: ['appointments'] });
    },
  });
}

export function useRescheduleAppointment() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, startTime, endTime }: { id: number; startTime: string; endTime: string }) =>
      apiClient.rescheduleAppointment(id, startTime, endTime),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['appointment', id] });
      queryClient.invalidateQueries({ queryKey: ['appointments'] });
    },
  });
}

// ===== Calls =====
export function useCalls(businessId: number, params: any = {}, enabled = true) {
  return useQuery({
    queryKey: queryKeys.calls(businessId, params),
    queryFn: () => apiClient.getCalls(businessId, params).then((res) => res.data),
    enabled: enabled && !!businessId && typeof window !== 'undefined',
    placeholderData: (previousData) => previousData,
  });
}

export function useCall(id: number, enabled = true) {
  return useQuery({
    queryKey: queryKeys.call(id),
    queryFn: () => apiClient.getCall(id).then((res) => res.data),
    enabled: enabled && !!id,
  });
}

export function useCallTranscript(id: number, enabled = true) {
  return useQuery({
    queryKey: queryKeys.callTranscript(id),
    queryFn: () => apiClient.getCallTranscript(id).then((res) => res.data),
    enabled: enabled && !!id,
  });
}

export function useUpdateCallTranscript() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, transcript }: { id: number; transcript: string }) =>
      apiClient.updateCallTranscript(id, transcript),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['call', id] });
      queryClient.invalidateQueries({ queryKey: ['call', id, 'transcript'] });
    },
  });
}

export function useExportCalls(businessId: number) {
  return useMutation({
    mutationFn: (params?: any) => apiClient.exportCalls(businessId, params),
  });
}

// ===== Analytics =====
export function useAnalyticsOverview(businessId: number, params: any = {}, enabled = true) {
  return useQuery({
    queryKey: queryKeys.analyticsOverview(businessId, params),
    queryFn: () => apiClient.getAnalyticsOverview(businessId, params).then((res) => res.data),
    enabled: enabled && !!businessId && typeof window !== 'undefined',
    staleTime: 1000 * 60 * 2, // 2 minutes
  });
}

export function useCallAnalytics(businessId: number, params: any = {}, enabled = true) {
  return useQuery({
    queryKey: queryKeys.callAnalytics(businessId, params),
    queryFn: () => apiClient.getCallAnalytics(businessId, params).then((res) => res.data),
    enabled: enabled && !!businessId && typeof window !== 'undefined',
  });
}

export function useAppointmentAnalytics(businessId: number, params: any = {}, enabled = true) {
  return useQuery({
    queryKey: queryKeys.appointmentAnalytics(businessId, params),
    queryFn: () => apiClient.getAppointmentAnalytics(businessId, params).then((res) => res.data),
    enabled: enabled && !!businessId && typeof window !== 'undefined',
  });
}

export function useCustomerAnalytics(businessId: number, params: any = {}, enabled = true) {
  return useQuery({
    queryKey: queryKeys.customerAnalytics(businessId, params),
    queryFn: () => apiClient.getCustomerAnalytics(businessId, params).then((res) => res.data),
    enabled: enabled && !!businessId && typeof window !== 'undefined',
  });
}

export function useRevenueAnalytics(businessId: number, params: any = {}, enabled = true) {
  return useQuery({
    queryKey: queryKeys.revenueAnalytics(businessId, params),
    queryFn: () => apiClient.getRevenueAnalytics(businessId, params).then((res) => res.data),
    enabled: enabled && !!businessId && typeof window !== 'undefined',
  });
}

// ===== Staff =====
export function useStaff(businessId: number, params: any = {}, enabled = true) {
  return useQuery({
    queryKey: queryKeys.staff(businessId, params),
    queryFn: () => apiClient.getStaff(businessId, params).then((res) => res.data),
    enabled: enabled && !!businessId && typeof window !== 'undefined',
  });
}

export function useStaffMember(id: number, enabled = true) {
  return useQuery({
    queryKey: queryKeys.staffMember(id),
    queryFn: () => apiClient.getStaffMember(id).then((res) => res.data),
    enabled: enabled && !!id && typeof window !== 'undefined',
  });
}

export function useCreateStaff() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: any) => apiClient.createStaff(data),
    onSuccess: (_, __, businessId) => {
      queryClient.invalidateQueries({ queryKey: ['staff', businessId] });
    },
  });
}

export function useUpdateStaff() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => apiClient.updateStaff(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['staff', id] });
      queryClient.invalidateQueries({ queryKey: ['staff'] });
    },
  });
}

export function useDeleteStaff() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => apiClient.deleteStaff(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['staff'] });
    },
  });
}

// ===== Services =====
export function useServices(businessId: number, params: any = {}, enabled = true) {
  return useQuery({
    queryKey: queryKeys.services(businessId, params),
    queryFn: () => apiClient.getServices(businessId, params).then((res) => res.data),
    enabled: enabled && !!businessId && typeof window !== 'undefined',
  });
}

export function useCreateService(businessId: number) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: any) => apiClient.createService(businessId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['services', businessId] });
    },
  });
}

// ===== Integrations =====
export function useIntegrations(businessId: number, enabled = true) {
  return useQuery({
    queryKey: queryKeys.integrations(businessId),
    queryFn: () => apiClient.getIntegrations(businessId).then((res) => res.data),
    enabled: enabled && !!businessId && typeof window !== 'undefined',
  });
}

export function useConnectIntegration() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ businessId, type, data }: { businessId: number; type: string; data: any }) =>
      apiClient.connectIntegration(businessId, type, data),
    onSuccess: (_, { businessId }) => {
      queryClient.invalidateQueries({ queryKey: ['integrations', businessId] });
    },
  });
}

export function useSyncIntegration() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => apiClient.syncIntegration(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['integrations'] });
    },
  });
}

// ===== Webhooks =====
export function useWebhooks(businessId: number, enabled = true) {
  return useQuery({
    queryKey: queryKeys.webhooks(businessId),
    queryFn: () => apiClient.getWebhooks(businessId).then((res) => res.data),
    enabled: enabled && !!businessId && typeof window !== 'undefined',
  });
}

export function useCreateWebhook(businessId: number) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: any) => apiClient.createWebhook(businessId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['webhooks', businessId] });
    },
  });
}

// ===== Notifications =====
export function useNotifications(businessId: number, params: any = {}, enabled = true) {
  return useQuery({
    queryKey: queryKeys.notifications(businessId, params),
    queryFn: () => apiClient.getNotifications(businessId, params).then((res) => res.data),
    enabled: enabled && !!businessId && typeof window !== 'undefined',
  });
}

// ===== API Keys =====
export function useApiKeys(businessId: number, enabled = true) {
  return useQuery({
    queryKey: queryKeys.apiKeys(businessId),
    queryFn: () => apiClient.getApiKeys(businessId).then((res) => res.data),
    enabled: enabled && !!businessId && typeof window !== 'undefined',
  });
}

export function useCreateApiKey(businessId: number) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: any) => apiClient.createApiKey(businessId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['apiKeys', businessId] });
    },
  });
}

export function useRevokeApiKey() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => apiClient.revokeApiKey(id),
    onSuccess: (_, __, businessId) => {
      queryClient.invalidateQueries({ queryKey: ['apiKeys', businessId] });
    },
  });
}

// ===== Audit Logs =====
export function useAuditLogs(businessId: number, params: any = {}, enabled = true) {
  return useQuery({
    queryKey: queryKeys.auditLogs(businessId, params),
    queryFn: () => apiClient.getAuditLogs(businessId, params).then((res) => res.data),
    enabled: enabled && !!businessId && typeof window !== 'undefined',
  });
}