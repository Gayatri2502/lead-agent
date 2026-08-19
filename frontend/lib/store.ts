import { create } from "zustand";

interface User {
  id: number;
  email: string;
  username: string;
  role: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
}

interface Business {
  id: number;
  name: string;
  business_type: string;
  timezone: string;
  appointment_duration: number;
}

interface AppState {
  user: User | null;
  business: Business | null;
  isAuthenticated: boolean;
  setUser: (user: User | null) => void;
  setBusiness: (business: Business | null) => void;
  setAuthenticated: (authenticated: boolean) => void;
  logout: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  user: null,
  business: null,
  isAuthenticated: false,
  
  setUser: (user) => set({ user }),
  setBusiness: (business) => set({ business }),
  setAuthenticated: (authenticated) => set({ isAuthenticated: authenticated }),
  
  logout: () => set({
    user: null,
    business: null,
    isAuthenticated: false,
  }),
}));
