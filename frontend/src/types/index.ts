// 用户相关类型
export interface User {
  id: string;
  username: string;
  email: string;
  full_name?: string;
  bio?: string;
  avatar_url?: string;
  theme: 'light' | 'dark' | 'auto';
  language: string;
  timezone: string;
  is_active: boolean;
  is_verified: boolean;
  role: 'user' | 'admin' | 'moderator';
  created_at: string;
  updated_at: string;
  last_login?: string;
}

export interface UserLogin {
  username: string;
  password: string;
}

export interface UserRegister {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  full_name?: string;
  agree_to_terms: boolean;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

// Agent相关类型
export interface Agent {
  id: string;
  name: string;
  description: string;
  type: 'chat' | 'task' | 'code' | 'creative';
  visibility: 'public' | 'private' | 'unlisted';
  status: 'active' | 'inactive' | 'draft';
  owner_id: string;
  owner?: User;
  model_config: ModelConfig;
  functional_config: FunctionalConfig;
  rate_limits: RateLimit;
  statistics: AgentStats;
  created_at: string;
  updated_at: string;
  published_at?: string;
}

export interface ModelConfig {
  provider: string;
  model_name: string;
  temperature: number;
  max_tokens: number;
  top_p: number;
  frequency_penalty: number;
  presence_penalty: number;
}

export interface FunctionalConfig {
  system_prompt: string;
  welcome_message: string;
  max_conversation_length: number;
  enable_memory: boolean;
  enable_web_search: boolean;
  enable_code_execution: boolean;
  allowed_file_types: string[];
}

export interface RateLimit {
  requests_per_minute: number;
  requests_per_hour: number;
  requests_per_day: number;
}

export interface AgentStats {
  total_conversations: number;
  total_messages: number;
  average_rating: number;
  total_ratings: number;
  total_tokens_used: number;
  total_cost: number;
}

// 对话相关类型
export interface Conversation {
  id: string;
  title: string;
  agent_id: string;
  agent?: Agent;
  user_id: string;
  user?: User;
  status: 'active' | 'archived' | 'deleted';
  message_count: number;
  total_tokens: number;
  total_cost: number;
  created_at: string;
  updated_at: string;
  last_message_at?: string;
}

export interface Message {
  id: string;
  conversation_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  metadata?: Record<string, any>;
  tokens_used?: number;
  cost?: number;
  processing_time?: number;
  created_at: string;
  updated_at: string;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
  stream?: boolean;
}

export interface ChatResponse {
  message: Message;
  conversation: Conversation;
}

// API Key相关类型
export interface APIKey {
  id: string;
  name: string;
  description?: string;
  key_prefix: string;
  scopes: string[];
  rate_limits: RateLimit;
  status: 'active' | 'inactive' | 'revoked';
  usage: APIKeyUsage;
  expires_at?: string;
  created_at: string;
  updated_at: string;
  last_used_at?: string;
}

export interface APIKeyUsage {
  total_requests: number;
  requests_today: number;
  requests_this_month: number;
  last_request_at?: string;
}

// 通用类型
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  errors?: Record<string, string[]>;
}

// 表单相关类型
export interface FormErrors {
  [key: string]: string[];
}

// 主题相关类型
export type Theme = 'light' | 'dark' | 'auto';

// 语言相关类型
export type Language = 'zh-CN' | 'en-US' | 'ja-JP' | 'ko-KR';