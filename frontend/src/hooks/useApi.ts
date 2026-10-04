'use client';

import { useCallback, useState } from 'react';
import Cookies from 'js-cookie';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api-client';
import type { Business, User } from '@/types';

interface AuthState {
  user: User | null;
  business: Business | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export function useAuth() {
  const router = useRouter();
  const [state, setState] = useState<AuthState>({
    user: null,
    business: null,
    isAuthenticated: !!Cookies.get('access_token'),
    isLoading: false,
    error: null,
  });

  const login = useCallback(
    async (email: string, password: string) => {
      setState((prev) => ({ ...prev, isLoading: true, error: null }));

      try {
        const response = await apiClient.login(email, password);
        const { access_token, user } = response.data;

        Cookies.set('access_token', access_token, { expires: 7 });
        Cookies.set('user_id', user.id.toString(), { expires: 7 });
        Cookies.set('business_id', user.business_id.toString(), { expires: 7 });

        setState({
          user,
          business: null, // Will be fetched separately
          isAuthenticated: true,
          isLoading: false,
          error: null,
        });

        router.push('/dashboard');
        return { success: true };
      } catch (err: any) {
        const error = err.response?.data?.detail || 'Login failed';
        setState((prev) => ({ ...prev, isLoading: false, error }));
        return { success: false, error };
      }
    },
    [router]
  );

  const register = useCallback(
    async (data: any) => {
      setState((prev) => ({ ...prev, isLoading: true, error: null }));

      try {
        const response = await apiClient.register(data);
        return { success: true, data: response.data };
      } catch (err: any) {
        const error = err.response?.data?.detail || 'Registration failed';
        setState((prev) => ({ ...prev, isLoading: false, error }));
        return { success: false, error };
      }
    },
    []
  );

  const logout = useCallback(() => {
    Cookies.remove('access_token');
    Cookies.remove('user_id');
    Cookies.remove('business_id');
    setState({
      user: null,
      business: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
    });
    router.push('/auth/login');
  }, [router]);

  return { ...state, login, register, logout };
}

export function useApi(fetchFn: (params: any) => Promise<{ data: any[]; total: number }>, initialParams: any = {}) {
  const [items, setItems] = useState<any[]>([]);
  const [total, setTotal] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [params, setParams] = useState(initialParams);

  const fetch = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetchFn(params);
      setItems(response.data);
      setTotal(response.total);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to fetch');
    } finally {
      setIsLoading(false);
    }
  }, [fetchFn, params]);

  const updateParams = useCallback((newParams: any) => {
    setParams((prev: any) => ({ ...prev, ...newParams, page: newParams.page || 1 }));
  }, []);

  return {
    items,
    total,
    isLoading,
    error,
    params,
    fetch,
    updateParams,
    setItems,
  };
}