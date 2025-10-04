import apiClient from './api';
import type { Agent, PaginatedResponse, ApiResponse } from '../types';

export interface AgentFilters {
  type?: string;
  visibility?: string;
  status?: string;
  owner_id?: string;
  search?: string;
  page?: number;
  size?: number;
}

export interface AgentCreateData {
  name: string;
  description: string;
  type: 'chat' | 'task' | 'code' | 'creative';
  visibility: 'public' | 'private' | 'unlisted';
  model_config: {
    provider: string;
    model_name: string;
    temperature: number;
    max_tokens: number;
    top_p: number;
    frequency_penalty: number;
    presence_penalty: number;
  };
  functional_config: {
    system_prompt: string;
    welcome_message: string;
    max_conversation_length: number;
    enable_memory: boolean;
    enable_web_search: boolean;
    enable_code_execution: boolean;
    allowed_file_types: string[];
  };
  rate_limits: {
    requests_per_minute: number;
    requests_per_hour: number;
    requests_per_day: number;
  };
}

export class AgentService {
  // 获取所有公开的Agent
  async getPublicAgents(filters?: AgentFilters): Promise<ApiResponse<PaginatedResponse<Agent>>> {
    return apiClient.get('/agents', filters);
  }

  // 获取当前用户的Agent
  async getMyAgents(filters?: AgentFilters): Promise<ApiResponse<PaginatedResponse<Agent>>> {
    return apiClient.get('/agents/my', filters);
  }

  // 获取Agent详情
  async getAgent(id: string): Promise<ApiResponse<Agent>> {
    return apiClient.get(`/agents/${id}`);
  }

  // 获取Agent详情 (by ID)
  async getAgentById(id: number): Promise<ApiResponse<Agent>> {
    return apiClient.get(`/agents/${id}`);
  }

  // 创建Agent
  async createAgent(data: AgentCreateData): Promise<ApiResponse<Agent>> {
    return apiClient.post('/agents', data);
  }

  // 更新Agent
  async updateAgent(id: string, data: Partial<AgentCreateData>): Promise<ApiResponse<Agent>> {
    return apiClient.patch(`/agents/${id}`, data);
  }

  // 删除Agent
  async deleteAgent(id: string): Promise<ApiResponse<void>> {
    return apiClient.delete(`/agents/${id}`);
  }

  // 克隆Agent
  async cloneAgent(id: string, data: { name: string; description?: string }): Promise<ApiResponse<Agent>> {
    return apiClient.post(`/agents/${id}/clone`, data);
  }

  // 发布Agent
  async publishAgent(id: string): Promise<ApiResponse<Agent>> {
    return apiClient.post(`/agents/${id}/publish`);
  }

  // 取消发布Agent
  async unpublishAgent(id: string): Promise<ApiResponse<Agent>> {
    return apiClient.post(`/agents/${id}/unpublish`);
  }

  // 获取Agent统计信息
  async getAgentStats(id: string): Promise<ApiResponse<any>> {
    return apiClient.get(`/agents/${id}/stats`);
  }

  // 导出Agent配置
  async exportAgent(id: string): Promise<ApiResponse<any>> {
    return apiClient.get(`/agents/${id}/export`);
  }

  // 导入Agent配置
  async importAgent(data: any): Promise<ApiResponse<Agent>> {
    return apiClient.post('/agents/import', data);
  }

  // 获取Agent扩展详情（包含评论、分析数据等）
  async getAgentDetailExtended(id: number): Promise<ApiResponse<any>> {
    return apiClient.get(`/agents/${id}/detail`);
  }

  // 创建Agent评论
  async createReview(agentId: number, data: {
    rating: number;
    title?: string;
    content?: string;
  }): Promise<ApiResponse<any>> {
    return apiClient.post(`/agents/${agentId}/reviews`, data);
  }

  // 获取Agent评论列表
  async getReviews(agentId: number, params?: {
    limit?: number;
    offset?: number;
  }): Promise<ApiResponse<any[]>> {
    return apiClient.get(`/agents/${agentId}/reviews`, params);
  }

  // 切换Agent收藏状态
  async toggleFavorite(agentId: number, isFavorite: boolean): Promise<ApiResponse<any>> {
    return apiClient.post(`/agents/${agentId}/favorite`, { is_favorite: isFavorite });
  }

  // 获取Agent分析数据
  async getAnalytics(agentId: number, params?: {
    period_type?: string;
    limit?: number;
  }): Promise<ApiResponse<any[]>> {
    return apiClient.get(`/agents/${agentId}/analytics`, params);
  }

  // 获取Agent流量数据
  async getTraffic(agentId: number, params?: {
    days?: number;
  }): Promise<ApiResponse<any[]>> {
    return apiClient.get(`/agents/${agentId}/traffic`, params);
  }
}

export const agentService = new AgentService();
export default agentService;