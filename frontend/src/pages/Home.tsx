import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { agentService } from '../services/agents';
import Button from '../components/ui/Button';
import type { Agent, PaginatedResponse } from '../types';

const Home: React.FC = () => {
  const { user, isAuthenticated } = useAuth();
  const [agents, setAgents] = useState<Agent[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const response = await agentService.getPublicAgents({ page: 1, size: 12 });
        if (response.success && response.data) {
          setAgents(response.data.items);
        } else {
          setError(response.message || 'Failed to load agents');
        }
      } catch (err) {
        setError('Failed to load agents');
      } finally {
        setIsLoading(false);
      }
    };

    fetchAgents();
  }, []);

  const AgentCard: React.FC<{ agent: Agent }> = ({ agent }) => (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900 truncate">
          {agent.name}
        </h3>
        <span className={`px-2 py-1 text-xs rounded-full ${
          agent.type === 'chat' ? 'bg-blue-100 text-blue-800' :
          agent.type === 'task' ? 'bg-green-100 text-green-800' :
          agent.type === 'code' ? 'bg-purple-100 text-purple-800' :
          'bg-pink-100 text-pink-800'
        }`}>
          {agent.type}
        </span>
      </div>
      
      <p className="text-gray-600 text-sm mb-4 line-clamp-3">
        {agent.description}
      </p>
      
      <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
        <span>by {agent.owner?.username || 'Unknown'}</span>
        <span>{agent.statistics.total_conversations} 对话</span>
      </div>
      
      <div className="flex space-x-2">
        <Button
          size="sm"
          className="flex-1"
          onClick={() => {
            // TODO: 实现与Agent对话
            console.log('Chat with agent:', agent.id);
          }}
        >
          开始对话
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => {
            // TODO: 实现查看Agent详情
            console.log('View agent details:', agent.id);
          }}
        >
          详情
        </Button>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl">
              欢迎来到 <span className="text-primary-600">AgentPedia</span>
            </h1>
            <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
              发现、创建和分享智能AI助手。让AI为你的工作和生活带来更多可能。
            </p>
            <div className="mt-5 max-w-md mx-auto sm:flex sm:justify-center md:mt-8">
              {isAuthenticated ? (
                <div className="space-x-4">
                  <Link to="/agents/create">
                    <Button size="lg">
                      创建Agent
                    </Button>
                  </Link>
                  <Link to="/agents">
                    <Button variant="outline" size="lg">
                      浏览Agent
                    </Button>
                  </Link>
                </div>
              ) : (
                <div className="space-x-4">
                  <Link to="/register">
                    <Button size="lg">
                      立即注册
                    </Button>
                  </Link>
                  <Link to="/login">
                    <Button variant="outline" size="lg">
                      登录
                    </Button>
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Featured Agents Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900">
            热门 Agent
          </h2>
          <p className="mt-4 text-lg text-gray-600">
            探索社区中最受欢迎的AI助手
          </p>
        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {[...Array(8)].map((_, i) => (
              <div key={i} className="bg-white rounded-lg shadow-md p-6 animate-pulse">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
                <div className="h-3 bg-gray-200 rounded w-full mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-2/3 mb-4"></div>
                <div className="h-8 bg-gray-200 rounded w-full"></div>
              </div>
            ))}
          </div>
        ) : error ? (
          <div className="text-center py-12">
            <p className="text-red-600">{error}</p>
            <Button
              variant="outline"
              className="mt-4"
              onClick={() => window.location.reload()}
            >
              重试
            </Button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {agents.map((agent) => (
              <AgentCard key={agent.id} agent={agent} />
            ))}
          </div>
        )}

        {!isLoading && !error && agents.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500">暂无可用的Agent</p>
            {isAuthenticated && (
              <Link to="/agents/create">
                <Button className="mt-4">
                  创建第一个Agent
                </Button>
              </Link>
            )}
          </div>
        )}

        {!isLoading && !error && agents.length > 0 && (
          <div className="text-center mt-12">
            <Link to="/agents">
              <Button variant="outline" size="lg">
                查看更多Agent
              </Button>
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;