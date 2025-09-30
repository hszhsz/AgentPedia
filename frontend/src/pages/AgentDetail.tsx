import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { agentService } from '../services/agents';
import type { Agent } from '../types';
import Button from '../components/ui/Button';

const AgentDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();
  const [agent, setAgent] = useState<Agent | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) {
      setError('Agent ID not found');
      setLoading(false);
      return;
    }

    const fetchAgent = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await agentService.getAgent(id);
        if (response.success && response.data) {
          setAgent(response.data);
        } else {
          setError(response.message || 'Failed to fetch agent');
        }
      } catch (err) {
        setError('获取Agent详情失败');
        console.error('Error fetching agent:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchAgent();
  }, [id]);

  const handleStartChat = () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    navigate(`/chat/${agent?.id}`);
  };

  const handleClone = async () => {
    if (!agent || !isAuthenticated) return;
    
    try {
      const response = await agentService.cloneAgent(agent.id, {
        name: `${agent.name} (副本)`,
        description: agent.description,
      });
      if (response.success && response.data) {
        navigate(`/agents/${response.data.id}/edit`);
      }
    } catch (err) {
      console.error('Error cloning agent:', err);
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-center items-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
      </div>
    );
  }

  if (error || !agent) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const isOwner = user?.id === agent.owner_id;

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <div className="flex items-center space-x-3 mb-2">
              <h1 className="text-3xl font-bold text-gray-900">{agent.name}</h1>
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                agent.visibility === 'public' 
                  ? 'bg-green-100 text-green-800' 
                  : agent.visibility === 'private'
                  ? 'bg-red-100 text-red-800'
                  : 'bg-yellow-100 text-yellow-800'
              }`}>
                {agent.visibility === 'public' ? '公开' : agent.visibility === 'private' ? '私有' : '未列出'}
              </span>
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                agent.status === 'active' 
                  ? 'bg-green-100 text-green-800' 
                  : agent.status === 'inactive'
                  ? 'bg-gray-100 text-gray-800'
                  : 'bg-yellow-100 text-yellow-800'
              }`}>
                {agent.status === 'active' ? '活跃' : agent.status === 'inactive' ? '非活跃' : '草稿'}
              </span>
            </div>
            <p className="text-gray-600 mb-4">{agent.description}</p>
            <div className="flex items-center space-x-6 text-sm text-gray-500">
              <span>创建者: {agent.owner?.username || 'Unknown'}</span>
              <span>类型: {agent.type}</span>
              <span>创建时间: {new Date(agent.created_at).toLocaleDateString()}</span>
            </div>
          </div>
        </div>

        {/* Action buttons */}
        <div className="flex items-center space-x-4">
          <Button onClick={handleStartChat} size="lg">
            开始对话
          </Button>
          
          {isAuthenticated && !isOwner && (
            <Button variant="outline" onClick={handleClone}>
              克隆Agent
            </Button>
          )}
          
          {isOwner && (
            <Link to={`/agents/${agent.id}/edit`}>
              <Button variant="outline">
                编辑Agent
              </Button>
            </Link>
          )}
        </div>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white rounded-lg shadow-sm p-4">
          <div className="text-2xl font-bold text-primary-600">{agent.statistics.total_conversations}</div>
          <div className="text-sm text-gray-500">总对话数</div>
        </div>
        <div className="bg-white rounded-lg shadow-sm p-4">
          <div className="text-2xl font-bold text-primary-600">{agent.statistics.total_messages}</div>
          <div className="text-sm text-gray-500">总消息数</div>
        </div>
        <div className="bg-white rounded-lg shadow-sm p-4">
          <div className="text-2xl font-bold text-primary-600">{agent.statistics.average_rating.toFixed(1)}</div>
          <div className="text-sm text-gray-500">平均评分</div>
        </div>
        <div className="bg-white rounded-lg shadow-sm p-4">
          <div className="text-2xl font-bold text-primary-600">{agent.statistics.total_ratings}</div>
          <div className="text-sm text-gray-500">评分数量</div>
        </div>
      </div>

      {/* Configuration Details */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Model Configuration */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">模型配置</h2>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">提供商:</span>
              <span className="font-medium">{agent.model_config.provider}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">模型:</span>
              <span className="font-medium">{agent.model_config.model_name}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">温度:</span>
              <span className="font-medium">{agent.model_config.temperature}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">最大令牌:</span>
              <span className="font-medium">{agent.model_config.max_tokens}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Top P:</span>
              <span className="font-medium">{agent.model_config.top_p}</span>
            </div>
          </div>
        </div>

        {/* Functional Configuration */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">功能配置</h2>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">最大对话长度:</span>
              <span className="font-medium">{agent.functional_config.max_conversation_length}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">启用记忆:</span>
              <span className={`font-medium ${agent.functional_config.enable_memory ? 'text-green-600' : 'text-red-600'}`}>
                {agent.functional_config.enable_memory ? '是' : '否'}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">启用网络搜索:</span>
              <span className={`font-medium ${agent.functional_config.enable_web_search ? 'text-green-600' : 'text-red-600'}`}>
                {agent.functional_config.enable_web_search ? '是' : '否'}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">启用代码执行:</span>
              <span className={`font-medium ${agent.functional_config.enable_code_execution ? 'text-green-600' : 'text-red-600'}`}>
                {agent.functional_config.enable_code_execution ? '是' : '否'}
              </span>
            </div>
          </div>
        </div>

        {/* System Prompt */}
        <div className="bg-white rounded-lg shadow-sm p-6 lg:col-span-2">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">系统提示词</h2>
          <div className="bg-gray-50 rounded-md p-4">
            <pre className="text-sm text-gray-700 whitespace-pre-wrap font-mono">
              {agent.functional_config.system_prompt}
            </pre>
          </div>
        </div>

        {/* Welcome Message */}
        <div className="bg-white rounded-lg shadow-sm p-6 lg:col-span-2">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">欢迎消息</h2>
          <div className="bg-gray-50 rounded-md p-4">
            <p className="text-sm text-gray-700">
              {agent.functional_config.welcome_message}
            </p>
          </div>
        </div>

        {/* Rate Limits */}
        <div className="bg-white rounded-lg shadow-sm p-6 lg:col-span-2">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">速率限制</h2>
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-primary-600">{agent.rate_limits.requests_per_minute}</div>
              <div className="text-sm text-gray-500">每分钟请求数</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-primary-600">{agent.rate_limits.requests_per_hour}</div>
              <div className="text-sm text-gray-500">每小时请求数</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-primary-600">{agent.rate_limits.requests_per_day}</div>
              <div className="text-sm text-gray-500">每天请求数</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgentDetail;