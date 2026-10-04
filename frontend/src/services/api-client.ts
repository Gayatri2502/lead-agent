import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios';
import Cookies from 'js-cookie';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000,
    });

    // Request interceptor - add auth token
    this.client.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        const token = Cookies.get('access_token');
        if (token && config.headers) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor - handle errors
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Token expired or invalid
          Cookies.remove('access_token');
          Cookies.remove('user_id');
          Cookies.remove('business_id');

          // Redirect to login if not already there
          if (typeof window !== 'undefined' && !window.location.pathname.startsWith('/auth')) {
            window.location.href = '/auth/login';
          }
        }
        return Promise.reject(error);
      }
    );
  }

  // ===== Auth =====
  async login(email: string, password: string) {
    return this.client.post('/auth/login', { email, password });
  }

  async register(data: any) {
    return this.client.post('/auth/register', data);
  }

  async refreshToken() {
    return this.client.post('/auth/refresh');
  }

  async forgotPassword(email: string) {
    return this.client.post('/auth/forgot-password', { email });
  }

  async resetPassword(token: string, password: string) {
    return this.client.post('/auth/reset-password', { token, password });
  }

  // ===== Business =====
  async getBusiness(id: number) {
    return this.client.get(`/businesses/${id}`);
  }

  async updateBusiness(id: number, data: any) {
    return this.client.put(`/businesses/${id}`, data);
  }

  async getBusinessSettings(businessId: number) {
    return this.client.get(`/businesses/${businessId}/settings`);
  }

  async updateBusinessSettings(businessId: number, data: any) {
    return this.client.put(`/businesses/${businessId}/settings`, data);
  }

  async getBusinessHours(businessId: number) {
    return this.client.get(`/businesses/${businessId}/hours`);
  }

  async updateBusinessHours(businessId: number, hours: any) {
    return this.client.put(`/businesses/${businessId}/hours`, hours);
  }

  // ===== Users/Staff =====
  async getUsers(businessId: number, params?: any) {
    return this.client.get(`/users`, { params: { business_id: businessId, ...params } });
  }

  async getUser(id: number) {
    return this.client.get(`/users/${id}`);
  }

  async createUser(data: any) {
    return this.client.post('/users', data);
  }

  async updateUser(id: number, data: any) {
    return this.client.put(`/users/${id}`, data);
  }

  async deleteUser(id: number) {
    return this.client.delete(`/users/${id}`);
  }

  async getStaff(businessId: number, params?: any) {
    return this.client.get('/staff', { params: { business_id: businessId, ...params } });
  }

  async getStaffMember(id: number) {
    return this.client.get(`/staff/${id}`);
  }

  async createStaff(data: any) {
    return this.client.post('/staff', data);
  }

  async updateStaff(id: number, data: any) {
    return this.client.put(`/staff/${id}`, data);
  }

  async deleteStaff(id: number) {
    return this.client.delete(`/staff/${id}`);
  }

  // ===== Customers =====
  async getCustomers(businessId: number, params?: any) {
    return this.client.get('/customers', { params: { business_id: businessId, ...params } });
  }

  async getCustomer(id: number) {
    return this.client.get(`/customers/${id}`);
  }

  async createCustomer(businessId: number, data: any) {
    return this.client.post('/customers', { ...data, business_id: businessId });
  }

  async updateCustomer(id: number, data: any) {
    return this.client.put(`/customers/${id}`, data);
  }

  async deleteCustomer(id: number) {
    return this.client.delete(`/customers/${id}`);
  }

  async importCustomers(businessId: number, file: File) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('business_id', businessId.toString());
    return this.client.post('/customers/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  }

  async exportCustomers(businessId: number, params?: any) {
    return this.client.get('/customers/export', {
      params: { business_id: businessId, ...params },
      responseType: 'blob',
    });
  }

  // ===== Appointments =====
  async getAppointments(businessId: number, params?: any) {
    return this.client.get('/appointments', { params: { business_id: businessId, ...params } });
  }

  async getAppointment(id: number) {
    return this.client.get(`/appointments/${id}`);
  }

  async createAppointment(businessId: number, data: any) {
    return this.client.post('/appointments', { ...data, business_id: businessId });
  }

  async updateAppointment(id: number, data: any) {
    return this.client.put(`/appointments/${id}`, data);
  }

  async deleteAppointment(id: number) {
    return this.client.delete(`/appointments/${id}`);
  }

  async cancelAppointment(id: number, reason?: string) {
    return this.client.post(`/appointments/${id}/cancel`, { reason });
  }

  async confirmAppointment(id: number) {
    return this.client.post(`/appointments/${id}/confirm`);
  }

  async completeAppointment(id: number) {
    return this.client.post(`/appointments/${id}/complete`);
  }

  async rescheduleAppointment(id: number, startTime: string, endTime: string) {
    return this.client.post(`/appointments/${id}/reschedule`, { start_time: startTime, end_time: endTime });
  }

  // ===== Services =====
  async getServices(businessId: number, params?: any) {
    return this.client.get('/services', { params: { business_id: businessId, ...params } });
  }

  async getService(id: number) {
    return this.client.get(`/services/${id}`);
  }

  async createService(businessId: number, data: any) {
    return this.client.post('/services', { ...data, business_id: businessId });
  }

  async updateService(id: number, data: any) {
    return this.client.put(`/services/${id}`, data);
  }

  async deleteService(id: number) {
    return this.client.delete(`/services/${id}`);
  }

  // ===== Calls =====
  async getCalls(businessId: number, params?: any) {
    return this.client.get('/calls', { params: { business_id: businessId, ...params } });
  }

  async getCall(id: number) {
    return this.client.get(`/calls/${id}`);
  }

  async getCallRecording(id: number) {
    return this.client.get(`/calls/${id}/recording`, { responseType: 'blob' });
  }

  async getCallTranscript(id: number) {
    return this.client.get(`/calls/${id}/transcript`);
  }

  async updateCallTranscript(id: number, transcript: string) {
    return this.client.put(`/calls/${id}/transcript`, { transcript });
  }

  async exportCalls(businessId: number, params?: any) {
    return this.client.get('/calls/export', {
      params: { business_id: businessId, ...params },
      responseType: 'blob',
    });
  }

  // ===== Analytics =====
  async getAnalyticsOverview(businessId: number, params?: any) {
    return this.client.get('/analytics/overview', { params: { business_id: businessId, ...params } });
  }

  async getCallAnalytics(businessId: number, params?: any) {
    return this.client.get('/analytics/calls', { params: { business_id: businessId, ...params } });
  }

  async getAppointmentAnalytics(businessId: number, params?: any) {
    return this.client.get('/analytics/appointments', { params: { business_id: businessId, ...params } });
  }

  async getCustomerAnalytics(businessId: number, params?: any) {
    return this.client.get('/analytics/customers', { params: { business_id: businessId, ...params } });
  }

  async getRevenueAnalytics(businessId: number, params?: any) {
    return this.client.get('/analytics/revenue', { params: { business_id: businessId, ...params } });
  }

  async exportAnalytics(businessId: number, type: string, params?: any) {
    return this.client.get(`/analytics/export/${type}`, {
      params: { business_id: businessId, ...params },
      responseType: 'blob',
    });
  }

  // ===== Webhooks =====
  async getWebhooks(businessId: number) {
    return this.client.get('/webhooks', { params: { business_id: businessId } });
  }

  async createWebhook(businessId: number, data: any) {
    return this.client.post('/webhooks', { ...data, business_id: businessId });
  }

  async updateWebhook(id: number, data: any) {
    return this.client.put(`/webhooks/${id}`, data);
  }

  async deleteWebhook(id: number) {
    return this.client.delete(`/webhooks/${id}`);
  }

  async testWebhook(id: number) {
    return this.client.post(`/webhooks/${id}/test`);
  }

  // ===== Integrations =====
  async getIntegrations(businessId: number) {
    return this.client.get('/integrations', { params: { business_id: businessId } });
  }

  async connectIntegration(businessId: number, type: string, data: any) {
    return this.client.post('/integrations', { ...data, business_id: businessId, type });
  }

  async disconnectIntegration(id: number) {
    return this.client.delete(`/integrations/${id}`);
  }

  async syncIntegration(id: number) {
    return this.client.post(`/integrations/${id}/sync`);
  }

  // ===== Notifications =====
  async getNotifications(businessId: number, params?: any) {
    return this.client.get('/notifications', { params: { business_id: businessId, ...params } });
  }

  async markNotificationRead(id: number) {
    return this.client.post(`/notifications/${id}/read`);
  }

  async markAllNotificationsRead(businessId: number) {
    return this.client.post('/notifications/read-all', { business_id: businessId });
  }

  // ===== API Keys =====
  async getApiKeys(businessId: number) {
    return this.client.get('/api-keys', { params: { business_id: businessId } });
  }

  async createApiKey(businessId: number, data: any) {
    return this.client.post('/api-keys', { ...data, business_id: businessId });
  }

  async revokeApiKey(id: number) {
    return this.client.delete(`/api-keys/${id}`);
  }

  // ===== Audit Logs =====
  async getAuditLogs(businessId: number, params?: any) {
    return this.client.get('/audit-logs', { params: { business_id: businessId, ...params } });
  }

  // ===== Health =====
  async healthCheck() {
    return this.client.get('/health');
  }
}

export const apiClient = new APIClient();