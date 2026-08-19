import { useState, useCallback } from "react";
import Cookies from "js-cookie";
import { useRouter } from "next/navigation";
import { apiClient } from "@/lib/api-client";

export function useAuth() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const login = useCallback(
    async (email: string, password: string) => {
      setIsLoading(true);
      setError(null);

      try {
        const response = await apiClient.login(email, password);
        const { access_token, user } = response.data;

        // Store token
        Cookies.set("access_token", access_token, { expires: 7 });
        Cookies.set("user_id", user.id, { expires: 7 });
        Cookies.set("business_id", user.business_id, { expires: 7 });

        router.push("/dashboard");
      } catch (err: any) {
        setError(err.response?.data?.detail || "Login failed");
      } finally {
        setIsLoading(false);
      }
    },
    [router]
  );

  const logout = useCallback(() => {
    Cookies.remove("access_token");
    Cookies.remove("user_id");
    Cookies.remove("business_id");
    router.push("/auth/login");
  }, [router]);

  const isAuthenticated = !!Cookies.get("access_token");

  return { login, logout, isAuthenticated, isLoading, error };
}

export function useAppointments(businessId: number) {
  const [appointments, setAppointments] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchAppointments = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await apiClient.getAppointments(businessId);
      setAppointments(response.data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }, [businessId]);

  return { appointments, isLoading, error, fetchAppointments };
}

export function useCustomers(businessId: number) {
  const [customers, setCustomers] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchCustomers = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await apiClient.getCustomers(businessId);
      setCustomers(response.data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }, [businessId]);

  return { customers, isLoading, error, fetchCustomers };
}

export function useAnalytics(businessId: number) {
  const [analytics, setAnalytics] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchAnalytics = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await apiClient.getAnalytics(businessId);
      setAnalytics(response.data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }, [businessId]);

  return { analytics, isLoading, error, fetchAnalytics };
}
