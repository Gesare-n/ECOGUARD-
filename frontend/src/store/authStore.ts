// Authentication store using zustand for EcoGuard frontend
// This replaces the mock implementation with a real authentication system

import { create } from 'zustand';
import { User } from '../types/user';
import authService from '../services/authService';

interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  loading: boolean;
  error: string | null;
}

interface AuthActions {
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => Promise<boolean>;
  checkAuthStatus: () => Promise<void>;
  clearError: () => void;
}

const useAuthStore = create<AuthState & AuthActions>((set, get) => ({
  isAuthenticated: false,
  user: null,
  loading: false,
  error: null,
  
  login: async (username, password) => {
    set({ loading: true, error: null });
    try {
      const success = await authService.login(username, password);
      if (success) {
        const state = authService.getState();
        set({ 
          isAuthenticated: state.isAuthenticated, 
          user: state.user, 
          loading: false 
        });
        return true;
      } else {
        set({ 
          loading: false, 
          error: authService.getState().error || 'Login failed' 
        });
        return false;
      }
    } catch (error) {
      set({ 
        loading: false, 
        error: 'Network error. Please try again.' 
      });
      return false;
    }
  },
  
  logout: async () => {
    set({ loading: true });
    try {
      const success = await authService.logout();
      if (success) {
        set({ 
          isAuthenticated: false, 
          user: null, 
          loading: false 
        });
        return true;
      } else {
        set({ loading: false, error: 'Logout failed' });
        return false;
      }
    } catch (error) {
      set({ 
        loading: false, 
        error: 'Network error. Please try again.' 
      });
      return false;
    }
  },
  
  checkAuthStatus: async () => {
    set({ loading: true });
    try {
      const user = await authService.getCurrentUser();
      if (user) {
        set({ 
          isAuthenticated: true, 
          user, 
          loading: false 
        });
      } else {
        set({ loading: false });
      }
    } catch (error) {
      set({ 
        loading: false, 
        error: 'Failed to check authentication status' 
      });
    }
  },
  
  clearError: () => set({ error: null })
}));

export default useAuthStore;