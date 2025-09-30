import { apiClient } from './api';
import type { User, ApiResponse } from '../types';

interface UpdateProfileData {
  username: string;
  email: string;
  bio?: string;
  avatar_url?: string;
}

export const userService = {
  // 获取当前用户信息
  getCurrentUser: async (): Promise<ApiResponse<User>> => {
    try {
      const response = await apiClient.get('/users/me');
      return {
        success: true,
        data: response.data,
        message: 'User fetched successfully'
      };
    } catch (error: any) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Failed to fetch user'
      };
    }
  },

  // 更新用户资料
  updateProfile: async (data: UpdateProfileData): Promise<ApiResponse<User>> => {
    try {
      const response = await apiClient.put('/users/me', data);
      return {
        success: true,
        data: response.data,
        message: 'Profile updated successfully'
      };
    } catch (error: any) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Failed to update profile'
      };
    }
  },

  // 更改密码
  changePassword: async (currentPassword: string, newPassword: string): Promise<ApiResponse<void>> => {
    try {
      await apiClient.put('/users/me/password', {
        current_password: currentPassword,
        new_password: newPassword
      });
      return {
        success: true,
        message: 'Password changed successfully'
      };
    } catch (error: any) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Failed to change password'
      };
    }
  },

  // 删除账户
  deleteAccount: async (): Promise<ApiResponse<void>> => {
    try {
      await apiClient.delete('/users/me');
      return {
        success: true,
        message: 'Account deleted successfully'
      };
    } catch (error: any) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Failed to delete account'
      };
    }
  }
};