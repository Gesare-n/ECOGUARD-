// Authentication service for EcoGuard frontend
// This service handles API calls to the backend authentication endpoints

import { User } from '../types/user';

const API_BASE_URL = '/api';

interface LoginResponse {
  user: User;
  token: string;
}

interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
  loading: boolean;
  error: string | null;
}

class AuthService {
  private state: AuthState = {
    isAuthenticated: false,
    user: null,
    token: null,
    loading: false,
    error: null
  };

  private listeners: Array<(state: AuthState) => void> = [];

  // Subscribe to state changes
  subscribe(listener: (state: AuthState) => void) {
    this.listeners.push(listener);
    return () => {
      const index = this.listeners.indexOf(listener);
      if (index > -1) {
        this.listeners.splice(index, 1);
      }
    };
  }

  // Notify all subscribers of state changes
  private notify() {
    this.listeners.forEach(listener => listener(this.state));
  }

  // Get current auth state
  getState() {
    return this.state;
  }

  // Login user
  async login(username: string, password: string): Promise<boolean> {
    try {
      this.state.loading = true;
      this.state.error = null;
      this.notify();

      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
      });

      if (response.ok) {
        const data: LoginResponse = await response.json();
        this.state.isAuthenticated = true;
        this.state.user = data.user;
        this.state.token = data.token;
        // Store token in localStorage for persistence
        localStorage.setItem('authToken', data.token);
        this.notify();
        return true;
      } else {
        const errorData = await response.json();
        this.state.error = errorData.error || 'Login failed';
        this.notify();
        return false;
      }
    } catch (error) {
      this.state.error = 'Network error. Please try again.';
      this.state.loading = false;
      this.notify();
      return false;
    } finally {
      this.state.loading = false;
      this.notify();
    }
  }

  // Logout user
  async logout(): Promise<boolean> {
    try {
      this.state.loading = true;
      this.notify();

      const response = await fetch(`${API_BASE_URL}/auth/logout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.state.token}`
        }
      });

      this.state.isAuthenticated = false;
      this.state.user = null;
      this.state.token = null;
      // Remove token from localStorage
      localStorage.removeItem('authToken');
      this.notify();
      return response.ok;
    } catch (error) {
      this.state.error = 'Logout failed. Please try again.';
      this.state.loading = false;
      this.notify();
      return false;
    } finally {
      this.state.loading = false;
      this.notify();
    }
  }

  // Get current user info
  async getCurrentUser(): Promise<User | null> {
    try {
      // Check if we have a token in state or localStorage
      const token = this.state.token || localStorage.getItem('authToken');
      if (!token) {
        return null;
      }

      const response = await fetch(`${API_BASE_URL}/auth/user`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        return data.user;
      }
      return null;
    } catch (error) {
      return null;
    }
  }

  // Check if user has required role
  hasRole(requiredRole: string): boolean {
    if (!this.state.isAuthenticated || !this.state.user) {
      return false;
    }
    return this.state.user.role === requiredRole;
  }

  // Check if user has any of the required roles
  hasAnyRole(requiredRoles: string[]): boolean {
    if (!this.state.isAuthenticated || !this.state.user) {
      return false;
    }
    return requiredRoles.includes(this.state.user.role);
  }
}

// Create singleton instance
const authService = new AuthService();

export default authService;