import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { chatService } from '../services/chat';
import { agentService } from '../services/agents';
import type { Conversation, Message, Agent } from '../types';
import Button from '../components/ui/Button';

const Chat: React.FC = () => {
  const { agentId, conversationId } = useParams<{ agentId?: string; conversationId?: string }>();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [agent, setAgent] = useState<Agent | null>(null);
  const [conversation, setConversation] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 滚动到消息底部
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    const initializeChat = async () => {
      try {
        setLoading(true);
        setError(null);

        // 如果有conversationId，加载现有对话
        if (conversationId) {
          const convResponse = await chatService.getConversation(conversationId);
          if (convResponse.success && convResponse.data) {
            setConversation(convResponse.data);
            
            // 获取Agent信息
            if (convResponse.data.agent_id) {
              const agentResponse = await agentService.getAgent(convResponse.data.agent_id);
              if (agentResponse.success && agentResponse.data) {
                setAgent(agentResponse.data);
              }
            }

            // 获取消息历史
            const messagesResponse = await chatService.getMessages({
              conversation_id: conversationId,
              size: 50,
            });
            if (messagesResponse.success && messagesResponse.data) {
              setMessages(messagesResponse.data.items);
            }
          }
        }
        // 如果有agentId但没有conversationId，创建新对话
        else if (agentId) {
          const agentResponse = await agentService.getAgent(agentId);
          if (agentResponse.success && agentResponse.data) {
            setAgent(agentResponse.data);
            
            // 创建新对话
            const convResponse = await chatService.createConversation(agentId);
            if (convResponse.success && convResponse.data) {
              setConversation(convResponse.data);
              navigate(`/chat/${agentId}/${convResponse.data.id}`, { replace: true });
              
              // 添加欢迎消息
              if (agentResponse.data.functional_config.welcome_message) {
                const welcomeMessage: Message = {
                  id: 'welcome',
                  conversation_id: convResponse.data.id,
                  role: 'assistant',
                  content: agentResponse.data.functional_config.welcome_message,
                  created_at: new Date().toISOString(),
                  updated_at: new Date().toISOString(),
                };
                setMessages([welcomeMessage]);
              }
            }
          }
        }
      } catch (err) {
        setError('初始化聊天失败');
        console.error('Error initializing chat:', err);
      } finally {
        setLoading(false);
      }
    };

    initializeChat();
  }, [agentId, conversationId, isAuthenticated, navigate]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || !conversation || loading) return;

    const userMessage: Message = {
      id: `temp-${Date.now()}`,
      conversation_id: conversation.id,
      role: 'user',
      content: inputMessage.trim(),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await chatService.sendMessage({
        message: inputMessage.trim(),
        conversation_id: conversation.id,
      });

      if (response.success && response.data) {
        // 更新用户消息ID
        setMessages(prev => 
          prev.map(msg => 
            msg.id === userMessage.id 
              ? { ...response.data!.message, role: 'user' as const, content: userMessage.content }
              : msg
          )
        );
        
        // 添加助手回复
        setMessages(prev => [...prev, response.data!.message]);
        
        // 更新对话信息
        if (response.data.conversation) {
          setConversation(response.data.conversation);
        }
      }
    } catch (err) {
      setError('发送消息失败');
      console.error('Error sending message:', err);
      // 移除失败的消息
      setMessages(prev => prev.filter(msg => msg.id !== userMessage.id));
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const MessageBubble: React.FC<{ message: Message }> = ({ message }) => (
    <div className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
        message.role === 'user'
          ? 'bg-primary-600 text-white'
          : 'bg-gray-200 text-gray-900'
      }`}>
        <div className="whitespace-pre-wrap">{message.content}</div>
        <div className={`text-xs mt-1 ${
          message.role === 'user' ? 'text-primary-100' : 'text-gray-500'
        }`}>
          {new Date(message.created_at).toLocaleTimeString()}
        </div>
      </div>
    </div>
  );

  if (!isAuthenticated) {
    return null;
  }

  if (loading && !conversation) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error && !conversation) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <p className="text-red-800">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      {agent && (
        <div className="bg-white border-b border-gray-200 px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-primary-600 rounded-full flex items-center justify-center">
                <span className="text-white font-medium">
                  {agent.name.charAt(0).toUpperCase()}
                </span>
              </div>
              <div>
                <h1 className="text-lg font-semibold text-gray-900">{agent.name}</h1>
                <p className="text-sm text-gray-500">{agent.type}</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => navigate(`/agents/${agent.id}`)}
              >
                查看详情
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-4xl mx-auto">
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
          {loading && (
            <div className="flex justify-start mb-4">
              <div className="bg-gray-200 rounded-lg px-4 py-2">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <div className="bg-white border-t border-gray-200 px-4 py-4">
        <div className="max-w-4xl mx-auto">
          <div className="flex space-x-4">
            <div className="flex-1">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="输入消息..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                rows={1}
                disabled={loading}
              />
            </div>
            <Button
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || loading}
              loading={loading}
            >
              发送
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;