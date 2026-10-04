'use client';

import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { User, Business } from '@/types';

interface AppState {
  user: User | null;
  business: Business | null;
  isAuthenticated: boolean;
  setUser: (user: User | null) => void;
  setBusiness: (business: Business | null) => void;
  setAuthenticated: (authenticated: boolean) => void;
  logout: () => void;

  sidebarCollapsed: boolean;
  toggleSidebar: () => void;
  setSidebarCollapsed: (collapsed: boolean) => void;

  theme: 'dark' | 'light' | 'system';
  setTheme: (theme: 'dark' | 'light' | 'system') => void;

  unreadCount: number;
  setUnreadCount: (count: number) => void;
  incrementUnreadCount: () => void;
  decrementUnreadCount: () => void;

  globalLoading: boolean;
  setGlobalLoading: (loading: boolean) => void;
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      user: null,
      business: null,
      isAuthenticated: false,
      setUser: (user) => set({ user }),
      setBusiness: (business) => set({ business }),
      setAuthenticated: (isAuthenticated) => set({ isAuthenticated }),
      logout: () => set({
        user: null,
        business: null,
        isAuthenticated: false,
        unreadCount: 0,
      }),

      sidebarCollapsed: false,
      toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
      setSidebarCollapsed: (sidebarCollapsed) => set({ sidebarCollapsed }),

      theme: 'dark',
      setTheme: (theme) => set({ theme }),

      unreadCount: 0,
      setUnreadCount: (unreadCount) => set({ unreadCount }),
      incrementUnreadCount: () => set((state) => ({ unreadCount: state.unreadCount + 1 })),
      decrementUnreadCount: () => set((state) => ({ unreadCount: Math.max(0, state.unreadCount - 1) })),

      globalLoading: false,
      setGlobalLoading: (globalLoading) => set({ globalLoading }),
    }),
    {
      name: 'app-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        sidebarCollapsed: state.sidebarCollapsed,
        theme: state.theme,
      }),
    }
  )
);