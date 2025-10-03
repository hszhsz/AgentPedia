'use client'

import React, { createContext, useContext, useReducer, useEffect } from 'react';
import type { ReactNode } from 'react';
import type { User, TokenResponse } from '../types';
import { authService } from '../services/auth';
import apiClient from '../services/api';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

type AuthAction =
  | { type: 'AUTH_START' }
  | { type: 'AUTH_SUCCESS'; payload: User }
  | { type: 'AUTH_FAILURE'; payload: string }
  | { type: 'AUTH_LOGOUT' }
  | { type: 'AUTH_UPDATE_USER'; payload: User }
  | { type: 'AUTH_CLEAR_ERROR' };

interface AuthContextType extends AuthState {
  login: (credentials: { username: string; password: string }) => Promise<boolean>;
  register: (userData: any) => Promise<boolean>;
  logout: () => void;
  updateProfile: (userData: Partial<User>) => Promise<boolean>;
  updateUser: (user: User) => void;
  clearError: () => void;
}

const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,
};

function authReducer(state: AuthState, action: AuthAction): AuthState {
  switch (action.type) {
    case 'AUTH_START':
      return {
        ...state,
        isLoading: true,
        error: null,
      };
    case 'AUTH_SUCCESS':
      return {
        ...state,
        user: action.payload,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      };
    case 'AUTH_FAILURE':
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: action.payload,
      };
    case 'AUTH_LOGOUT':
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      };
    case 'AUTH_UPDATE_USER':
      return {
        ...state,
        user: action.payload,
      };
    case 'AUTH_CLEAR_ERROR':
      return {
        ...state,
        error: null,
      };
    default:
      return state;
  }
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // 初始化时检查用户认证状态
  useEffect(() => {
    const initAuth = async () => {
      if (authService.isAuthenticated()) {
        dispatch({ type: 'AUTH_START' });
        try {
          const response = await authService.getCurrentUser();
          if (response.success && response.data) {
            dispatch({ type: 'AUTH_SUCCESS', payload: response.data });
          } else {
            dispatch({ type: 'AUTH_FAILURE', payload: 'Failed to get user info' });
            authService.logout();
          }
        } catch (error) {
          dispatch({ type: 'AUTH_FAILURE', payload: 'Authentication failed' });
          authService.logout();
        }
      } else {
        dispatch({ type: 'AUTH_LOGOUT' });
      }
    };

    initAuth();
  }, []);

  const login = async (credentials: { username: string; password: string }): Promise<boolean> => {
    dispatch({ type: 'AUTH_START' });
    
    try {
      const response = await authService.login(credentials);
      if (response.success && response.data) {
        // 设置tokens
        apiClient.setAuthTokens(response.data);
        
        // 获取用户信息
        const userResponse = await authService.getCurrentUser();
        if (userResponse.success && userResponse.data) {
          dispatch({ type: 'AUTH_SUCCESS', payload: userResponse.data });
          return true;
        } else {
          dispatch({ type: 'AUTH_FAILURE', payload: 'Failed to get user info' });
          return false;
        }
      } else {
        dispatch({ type: 'AUTH_FAILURE', payload: response.message || 'Login failed' });
        return false;
      }
    } catch (error) {
      dispatch({ type: 'AUTH_FAILURE', payload: 'Login failed' });
      return false;
    }
  };

  const register = async (userData: any): Promise<boolean> => {
    dispatch({ type: 'AUTH_START' });
    
    try {
      const response = await authService.register(userData);
      if (response.success && response.data) {
        // 注册成功后自动登录
        const loginSuccess = await login({
          username: userData.username,
          password: userData.password,
        });
        return loginSuccess;
      } else {
        dispatch({ type: 'AUTH_FAILURE', payload: response.message || 'Registration failed' });
        return false;
      }
    } catch (error) {
      dispatch({ type: 'AUTH_FAILURE', payload: 'Registration failed' });
      return false;
    }
  };

  const logout = () => {
    authService.logout();
    dispatch({ type: 'AUTH_LOGOUT' });
  };

  const updateProfile = async (userData: Partial<User>): Promise<boolean> => {
    try {
      const response = await authService.updateProfile(userData);
      if (response.success && response.data) {
        dispatch({ type: 'AUTH_UPDATE_USER', payload: response.data });
        return true;
      } else {
        dispatch({ type: 'AUTH_FAILURE', payload: response.message || 'Update failed' });
        return false;
      }
    } catch (error) {
      dispatch({ type: 'AUTH_FAILURE', payload: 'Update failed' });
      return false;
    }
  };

  const updateUser = (user: User) => {
    dispatch({ type: 'AUTH_UPDATE_USER', payload: user });
  };

  const clearError = () => {
    dispatch({ type: 'AUTH_CLEAR_ERROR' });
  };

  const value: AuthContextType = {
    ...state,
    login,
    register,
    logout,
    updateProfile,
    updateUser,
    clearError,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

export default AuthContext;