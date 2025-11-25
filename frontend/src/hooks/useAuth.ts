// React hook for authentication
// This hook provides authentication state and functions to components

import useAuthStore from '../store/authStore';
import { User } from '../types/user';

interface UseAuthReturn {
  isAuthenticated: boolean;
  user: User | null;
  loading: boolean;
  error: string | null;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => Promise<boolean>;
  hasRole: (role: string) => boolean;
  hasAnyRole: (roles: string[]) => boolean;
  clearError: () => void;
  checkAuthStatus: () => Promise<void>;
}

export const useAuth = (): UseAuthReturn => {
  const { isAuthenticated, user, loading, error, login, logout, clearError, checkAuthStatus } = useAuthStore();
  
  const hasRole = (role: string): boolean => {
    if (!isAuthenticated || !user) {
      return false;
    }
    return user.role === role;
  };

  const hasAnyRole = (roles: string[]): boolean => {
    if (!isAuthenticated || !user) {
      return false;
    }
    return roles.includes(user.role);
  };

  return {
    isAuthenticated,
    user,
    loading,
    error,
    login,
    logout,
    hasRole,
    hasAnyRole,
    clearError,
    checkAuthStatus
  };
};