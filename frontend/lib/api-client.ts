import axios, { AxiosInstance, AxiosError } from "axios";
import Cookies from "js-cookie";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        "Content-Type": "application/json",
      },
    });

    // Add interceptor to include JWT token
    this.client.interceptors.request.use((config) => {
      const token = Cookies.get("access_token");
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Add interceptor to handle errors
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Token expired, redirect to login
          Cookies.remove("access_token");
          window.location.href = "/auth/login";
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  login(email: string, password: string) {
    return this.client.post("/auth/login", { email, password });
  }

  register(data: any) {
    return this.client.post("/auth/register", data);
  }

  // Appointments
  getAppointments(businessId: number, params?: any) {
    return this.client.get(`/appointments?business_id=${businessId}`, { params });
  }

  createAppointment(businessId: number, data: any) {
    return this.client.post(`/appointments?business_id=${businessId}`, data);
  }

  getAppointment(id: number) {
    return this.client.get(`/appointments/${id}`);
  }

  updateAppointment(id: number, data: any) {
    return this.client.put(`/appointments/${id}`, data);
  }

  deleteAppointment(id: number) {
    return this.client.delete(`/appointments/${id}`);
  }

  // Customers
  getCustomers(businessId: number, params?: any) {
    return this.client.get(`/customers?business_id=${businessId}`, { params });
  }

  createCustomer(businessId: number, data: any) {
    return this.client.post(`/customers?business_id=${businessId}`, data);
  }

  getCustomer(id: number) {
    return this.client.get(`/customers/${id}`);
  }

  updateCustomer(id: number, data: any) {
    return this.client.put(`/customers/${id}`, data);
  }

  // Calls
  getCalls(businessId: number, params?: any) {
    return this.client.get(`/calls?business_id=${businessId}`, { params });
  }

  getCall(id: number) {
    return this.client.get(`/calls/${id}`);
  }

  // Analytics
  getAnalytics(businessId: number, params?: any) {
    return this.client.get(`/analytics/business/${businessId}`, { params });
  }

  // Business
  getBusiness(id: number) {
    return this.client.get(`/businesses/${id}`);
  }

  updateBusiness(id: number, data: any) {
    return this.client.put(`/businesses/${id}`, data);
  }

  getBusinessSettings(businessId: number) {
    return this.client.get(`/businesses/${businessId}/settings`);
  }

  updateBusinessSettings(businessId: number, data: any) {
    return this.client.put(`/businesses/${businessId}/settings`, data);
  }

  // Health check
  healthCheck() {
    return this.client.get("/health");
  }
}

export const apiClient = new APIClient();
