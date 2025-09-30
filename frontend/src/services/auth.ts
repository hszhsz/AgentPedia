import apiClient from './api';
import type { User, UserLogin, UserRegister, TokenResponse, ApiResponse } from '../types';

export class AuthService {
  // 用户登录
  async login(credentials: UserLogin): Promise<ApiResponse<TokenResponse>> {
    return apiClient.post('/users/login', credentials);
  }

  // 用户注册
  async register(userData: UserRegister): Promise<ApiResponse<User>> {
    return apiClient.post('/users/register', userData);
  }

  // 获取当前用户信息
  async getCurrentUser(): Promise<ApiResponse<User>> {
    return apiClient.get('/users/me');
  }

  // 更新用户信息
  async updateProfile(userData: Partial<User>): Promise<ApiResponse<User>> {
    return apiClient.patch('/users/me', userData);
  }

  // 修改密码
  async changePassword(data: {
    current_password: string;
    new_password: string;
    confirm_password: string;
  }): Promise<ApiResponse<void>> {
    return apiClient.post('/users/me/change-password', data);
  }

  // 请求密码重置
  async requestPasswordReset(email: string): Promise<ApiResponse<void>> {
    return apiClient.post('/users/password-reset', { email });
  }

  // 确认密码重置
  async confirmPasswordReset(data: {
    token: string;
    new_password: string;
    confirm_password: string;
  }): Promise<ApiResponse<void>> {
    return apiClient.post('/users/password-reset/confirm', data);
  }

  // 刷新token
  async refreshToken(refreshToken: string): Promise<ApiResponse<TokenResponse>> {
    return apiClient.post('/users/refresh-token', { refresh_token: refreshToken });
  }

  // 登出
  async logout(): Promise<void> {
    apiClient.clearAuth();
  }

  // 检查是否已认证
  isAuthenticated(): boolean {
    return apiClient.isAuthenticated();
  }
}

export const authService = new AuthService();
export default authService;