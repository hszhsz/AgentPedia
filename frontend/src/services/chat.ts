import apiClient from './api';
import type { Conversation, Message, ChatRequest, ChatResponse, PaginatedResponse, ApiResponse } from '../types';

export interface ConversationFilters {
  agent_id?: string;
  status?: string;
  page?: number;
  size?: number;
}

export interface MessageFilters {
  conversation_id: string;
  page?: number;
  size?: number;
}

export class ChatService {
  // 获取用户的对话列表
  async getConversations(filters?: ConversationFilters): Promise<ApiResponse<PaginatedResponse<Conversation>>> {
    return apiClient.get('/conversations', filters);
  }

  // 获取特定对话
  async getConversation(id: string): Promise<ApiResponse<Conversation>> {
    return apiClient.get(`/conversations/${id}`);
  }

  // 创建新对话
  async createConversation(agentId: string, title?: string): Promise<ApiResponse<Conversation>> {
    return apiClient.post('/conversations', {
      agent_id: agentId,
      title: title || '新对话',
    });
  }

  // 更新对话标题
  async updateConversation(id: string, data: { title?: string; status?: string }): Promise<ApiResponse<Conversation>> {
    return apiClient.patch(`/conversations/${id}`, data);
  }

  // 删除对话
  async deleteConversation(id: string): Promise<ApiResponse<void>> {
    return apiClient.delete(`/conversations/${id}`);
  }

  // 获取对话中的消息
  async getMessages(filters: MessageFilters): Promise<ApiResponse<PaginatedResponse<Message>>> {
    return apiClient.get(`/conversations/${filters.conversation_id}/messages`, {
      page: filters.page,
      size: filters.size,
    });
  }

  // 发送消息
  async sendMessage(request: ChatRequest): Promise<ApiResponse<ChatResponse>> {
    return apiClient.post('/chat', request);
  }

  // 流式发送消息
  async sendMessageStream(request: ChatRequest): Promise<ReadableStream<Uint8Array>> {
    const response = await fetch(`${apiClient.getBaseURL()}/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiClient.getToken()}`,
      },
      body: JSON.stringify({ ...request, stream: true }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    if (!response.body) {
      throw new Error('Response body is null');
    }

    return response.body;
  }

  // 获取消息详情
  async getMessage(conversationId: string, messageId: string): Promise<ApiResponse<Message>> {
    return apiClient.get(`/conversations/${conversationId}/messages/${messageId}`);
  }

  // 删除消息
  async deleteMessage(conversationId: string, messageId: string): Promise<ApiResponse<void>> {
    return apiClient.delete(`/conversations/${conversationId}/messages/${messageId}`);
  }

  // 重新生成消息
  async regenerateMessage(conversationId: string, messageId: string): Promise<ApiResponse<ChatResponse>> {
    return apiClient.post(`/conversations/${conversationId}/messages/${messageId}/regenerate`);
  }

  // 评价消息
  async rateMessage(conversationId: string, messageId: string, rating: number): Promise<ApiResponse<void>> {
    return apiClient.post(`/conversations/${conversationId}/messages/${messageId}/rate`, { rating });
  }
}

export const chatService = new ChatService();
export default chatService;