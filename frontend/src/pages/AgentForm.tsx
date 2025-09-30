import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { agentService, type AgentCreateData } from '../services/agents';
import type { Agent } from '../types';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';

const AgentForm: React.FC = () => {
  const { id } = useParams<{ id?: string }>();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const isEditing = !!id;

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState<AgentCreateData>({
    name: '',
    description: '',
    type: 'chat',
    visibility: 'private',
    model_config: {
      provider: 'openai',
      model_name: 'gpt-3.5-turbo',
      temperature: 0.7,
      max_tokens: 2048,
      top_p: 1.0,
      frequency_penalty: 0.0,
      presence_penalty: 0.0,
    },
    functional_config: {
      system_prompt: '',
      welcome_message: '',
      max_conversation_length: 100,
      enable_memory: true,
      enable_web_search: false,
      enable_code_execution: false,
      allowed_file_types: [],
    },
    rate_limits: {
      requests_per_minute: 10,
      requests_per_hour: 100,
      requests_per_day: 1000,
    },
  });

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    if (isEditing && id) {
      loadAgent();
    }
  }, [isAuthenticated, isEditing, id, navigate]);

  const loadAgent = async () => {
    if (!id) return;

    try {
      setLoading(true);
      setError(null);
      
      const response = await agentService.getAgent(id);
      if (response.success && response.data) {
        const agent = response.data;
        setFormData({
          name: agent.name,
          description: agent.description,
          type: agent.type,
          visibility: agent.visibility,
          model_config: agent.model_config,
          functional_config: agent.functional_config,
          rate_limits: agent.rate_limits,
        });
      } else {
        setError('加载Agent失败');
      }
    } catch (err) {
      setError('加载Agent失败');
      console.error('Error loading agent:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.name.trim()) {
      setError('请输入Agent名称');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      let response;
      if (isEditing && id) {
        response = await agentService.updateAgent(id, formData);
      } else {
        response = await agentService.createAgent(formData);
      }

      if (response.success && response.data) {
        navigate(`/agents/${response.data.id}`);
      } else {
        setError(response.message || `${isEditing ? '更新' : '创建'}Agent失败`);
      }
    } catch (err) {
      setError(`${isEditing ? '更新' : '创建'}Agent失败`);
      console.error('Error saving agent:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field: string, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleNestedInputChange = (section: keyof AgentCreateData, field: string, value: any) => {
    setFormData(prev => ({
      ...prev,
      [section]: {
        ...(prev[section] as any),
        [field]: value,
      },
    }));
  };

  if (!isAuthenticated) {
    return null;
  }

  if (loading && isEditing) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900">
            {isEditing ? '编辑Agent' : '创建新Agent'}
          </h1>
          <p className="text-gray-600 mt-2">
            {isEditing ? '修改Agent的配置和设置' : '配置您的AI助手'}
          </p>
        </div>

        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-md p-4">
            <p className="text-red-800">{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* 基本信息 */}
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-4">基本信息</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <Input
                  label="Agent名称"
                  value={formData.name}
                  onChange={(e) => handleInputChange('name', e.target.value)}
                  placeholder="输入Agent名称"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  类型
                </label>
                <select
                  value={formData.type}
                  onChange={(e) => handleInputChange('type', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                >
                  <option value="assistant">助手</option>
                  <option value="chatbot">聊天机器人</option>
                  <option value="analyzer">分析师</option>
                  <option value="generator">生成器</option>
                  <option value="other">其他</option>
                </select>
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  描述
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) => handleInputChange('description', e.target.value)}
                  placeholder="描述Agent的功能和用途"
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  可见性
                </label>
                <select
                  value={formData.visibility}
                  onChange={(e) => handleInputChange('visibility', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                >
                  <option value="private">私有</option>
                  <option value="public">公开</option>
                </select>
              </div>
            </div>
          </div>

          {/* 模型配置 */}
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-4">模型配置</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  模型
                </label>
                <select
                  value={formData.model_config.model_name}
                  onChange={(e) => handleNestedInputChange('model_config', 'model_name', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                >
                  <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                  <option value="gpt-4">GPT-4</option>
                  <option value="gpt-4-turbo">GPT-4 Turbo</option>
                </select>
              </div>
              <div>
                <Input
                  label="温度"
                  type="number"
                  min="0"
                  max="2"
                  step="0.1"
                  value={formData.model_config.temperature}
                  onChange={(e) => handleNestedInputChange('model_config', 'temperature', parseFloat(e.target.value))}
                />
              </div>
              <div>
                <Input
                  label="最大令牌数"
                  type="number"
                  min="1"
                  max="4096"
                  value={formData.model_config.max_tokens}
                  onChange={(e) => handleNestedInputChange('model_config', 'max_tokens', parseInt(e.target.value))}
                />
              </div>
              <div>
                <Input
                  label="Top P"
                  type="number"
                  min="0"
                  max="1"
                  step="0.1"
                  value={formData.model_config.top_p}
                  onChange={(e) => handleNestedInputChange('model_config', 'top_p', parseFloat(e.target.value))}
                />
              </div>
              <div>
                <Input
                  label="频率惩罚"
                  type="number"
                  min="-2"
                  max="2"
                  step="0.1"
                  value={formData.model_config.frequency_penalty}
                  onChange={(e) => handleNestedInputChange('model_config', 'frequency_penalty', parseFloat(e.target.value))}
                />
              </div>
              <div>
                <Input
                  label="存在惩罚"
                  type="number"
                  min="-2"
                  max="2"
                  step="0.1"
                  value={formData.model_config.presence_penalty}
                  onChange={(e) => handleNestedInputChange('model_config', 'presence_penalty', parseFloat(e.target.value))}
                />
              </div>
            </div>
          </div>

          {/* 功能配置 */}
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-4">功能配置</h2>
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="enable_memory"
                    checked={formData.functional_config.enable_memory}
                    onChange={(e) => handleNestedInputChange('functional_config', 'enable_memory', e.target.checked)}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label htmlFor="enable_memory" className="ml-2 block text-sm text-gray-900">
                    启用记忆功能
                  </label>
                </div>
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="enable_web_search"
                    checked={formData.functional_config.enable_web_search}
                    onChange={(e) => handleNestedInputChange('functional_config', 'enable_web_search', e.target.checked)}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label htmlFor="enable_web_search" className="ml-2 block text-sm text-gray-900">
                    启用网络搜索
                  </label>
                </div>
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="enable_code_execution"
                    checked={formData.functional_config.enable_code_execution}
                    onChange={(e) => handleNestedInputChange('functional_config', 'enable_code_execution', e.target.checked)}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label htmlFor="enable_code_execution" className="ml-2 block text-sm text-gray-900">
                    启用代码执行
                  </label>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  系统提示词
                </label>
                <textarea
                  value={formData.functional_config.system_prompt}
                  onChange={(e) => handleNestedInputChange('functional_config', 'system_prompt', e.target.value)}
                  placeholder="定义Agent的角色和行为..."
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  欢迎消息
                </label>
                <textarea
                  value={formData.functional_config.welcome_message}
                  onChange={(e) => handleNestedInputChange('functional_config', 'welcome_message', e.target.value)}
                  placeholder="Agent的欢迎消息..."
                  rows={2}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
              </div>
            </div>
          </div>

          {/* 速率限制 */}
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-4">速率限制</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <Input
                  label="每分钟请求数"
                  type="number"
                  min="1"
                  value={formData.rate_limits.requests_per_minute}
                  onChange={(e) => handleNestedInputChange('rate_limits', 'requests_per_minute', parseInt(e.target.value))}
                />
              </div>
              <div>
                <Input
                  label="每小时请求数"
                  type="number"
                  min="1"
                  value={formData.rate_limits.requests_per_hour}
                  onChange={(e) => handleNestedInputChange('rate_limits', 'requests_per_hour', parseInt(e.target.value))}
                />
              </div>
              <div>
                <Input
                  label="每天请求数"
                  type="number"
                  min="1"
                  value={formData.rate_limits.requests_per_day}
                  onChange={(e) => handleNestedInputChange('rate_limits', 'requests_per_day', parseInt(e.target.value))}
                />
              </div>
            </div>
          </div>

          {/* 提交按钮 */}
          <div className="flex justify-end space-x-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => navigate(-1)}
            >
              取消
            </Button>
            <Button
              type="submit"
              loading={loading}
              disabled={loading}
            >
              {isEditing ? '更新Agent' : '创建Agent'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AgentForm;