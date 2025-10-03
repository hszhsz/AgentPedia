'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { agentService, type AgentFilters } from '@/services/agents'
import type { Agent, PaginatedResponse } from '@/types'
import { Search, Filter, Plus, Star, Users, ArrowRight } from 'lucide-react'

export default function AgentsPage() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [filters, setFilters] = useState<AgentFilters>({
    page: 1,
    size: 12,
    search: ''
  })
  const [pagination, setPagination] = useState({
    total: 0,
    page: 1,
    size: 12,
    pages: 0
  })

  useEffect(() => {
    fetchAgents()
  }, [filters])

  const fetchAgents = async () => {
    try {
      setLoading(true)
      const response = await agentService.getPublicAgents(filters)
      if (response.success && response.data) {
        setAgents(response.data.items)
        setPagination(response.data)
      } else {
        setError(response.message || 'Failed to fetch agents')
      }
    } catch (err) {
      setError('Failed to fetch agents')
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (search: string) => {
    setFilters(prev => ({ ...prev, search, page: 1 }))
  }

  const handleFilter = (newFilters: Partial<AgentFilters>) => {
    setFilters(prev => ({ ...prev, ...newFilters, page: 1 }))
  }

  const handlePageChange = (page: number) => {
    setFilters(prev => ({ ...prev, page }))
  }

  const getStatusColor = (status: Agent['status']) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
      case 'inactive': return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
      case 'draft': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
    }
  }

  const getVisibilityColor = (visibility: Agent['visibility']) => {
    switch (visibility) {
      case 'public': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
      case 'private': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
      case 'unlisted': return 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200'
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
    }
  }

  const getTypeColor = (type: Agent['type']) => {
    switch (type) {
      case 'chat': return 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-200'
      case 'task': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
      case 'code': return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200'
      case 'creative': return 'bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-200'
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
    }
  }

  return (
    <div className="min-h-screen bg-background dark:bg-background-dark">
      <div className="container py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-text-primary dark:text-text-primary-dark mb-4">
            AI Agents 探索
          </h1>
          <p className="text-lg text-text-secondary dark:text-text-secondary-dark max-w-3xl mx-auto mb-8">
            发现社区创建的各种 AI Agents，从对话助手到编程工具，找到适合您需求的智能助手
          </p>

          {/* Search and Filters */}
          <div className="flex flex-col md:flex-row gap-4 max-w-4xl mx-auto mb-8">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-text-secondary dark:text-text-secondary-dark" />
              <Input
                placeholder="搜索 AI Agents..."
                className="pl-10"
                value={filters.search || ''}
                onChange={(e) => handleSearch(e.target.value)}
              />
            </div>
            <div className="flex gap-2">
              <select
                className="px-4 py-2 border border-border dark:border-border-dark rounded-lg bg-white dark:bg-background-dark text-text-primary dark:text-text-primary-dark"
                value={filters.type || ''}
                onChange={(e) => handleFilter({ type: e.target.value || undefined })}
              >
                <option value="">所有类型</option>
                <option value="chat">对话</option>
                <option value="task">任务</option>
                <option value="code">编程</option>
                <option value="creative">创意</option>
              </select>
              <select
                className="px-4 py-2 border border-border dark:border-border-dark rounded-lg bg-white dark:bg-background-dark text-text-primary dark:text-text-primary-dark"
                value={filters.visibility || ''}
                onChange={(e) => handleFilter({ visibility: e.target.value || undefined })}
              >
                <option value="">所有可见性</option>
                <option value="public">公开</option>
                <option value="private">私有</option>
                <option value="unlisted">不公开</option>
              </select>
            </div>
          </div>

          {/* Create New Agent Button */}
          <div className="flex justify-center mb-8">
            <Button
              className="bg-accent dark:bg-accent-dark hover:bg-opacity-90 text-white px-6"
              onClick={() => window.location.href = '/agents/create'}
            >
              <Plus className="mr-2 h-4 w-4" />
              创建新的 AI Agent
            </Button>
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-accent dark:border-accent-dark"></div>
            <p className="mt-4 text-text-secondary dark:text-text-secondary-dark">正在加载 AI Agents...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="text-center py-12">
            <div className="text-red-500 dark:text-red-400 mb-4">
              <p>{error}</p>
            </div>
            <Button onClick={fetchAgents}>重试</Button>
          </div>
        )}

        {/* Agents Grid */}
        {!loading && !error && (
          <>
            {agents.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-text-secondary dark:text-text-secondary-dark mb-4">
                  没有找到匹配的 AI Agents
                </p>
                <Button onClick={() => window.location.href = '/agents/create'}>
                  创建第一个 AI Agent
                </Button>
              </div>
            ) : (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-8">
                  {agents.map((agent) => (
                    <Card
                      key={agent.id}
                      className="group hover:shadow-xl transition-all duration-300 border-border dark:border-border-dark hover:border-accent dark:hover:border-accent-dark cursor-pointer"
                      onClick={() => window.location.href = `/agents/${agent.id}`}
                    >
                      <CardHeader className="pb-4">
                        <div className="flex items-start justify-between mb-3">
                          <div className="flex-1">
                            <CardTitle className="text-lg group-hover:text-accent dark:group-hover:text-accent-dark transition-colors mb-2">
                              {agent.name}
                            </CardTitle>
                            <div className="flex flex-wrap gap-2 mb-2">
                              <Badge
                                variant="secondary"
                                className={`text-xs ${getTypeColor(agent.type)}`}
                              >
                                {agent.type}
                              </Badge>
                              <Badge
                                variant="secondary"
                                className={`text-xs ${getStatusColor(agent.status)}`}
                              >
                                {agent.status}
                              </Badge>
                              <Badge
                                variant="secondary"
                                className={`text-xs ${getVisibilityColor(agent.visibility)}`}
                              >
                                {agent.visibility}
                              </Badge>
                            </div>
                          </div>
                        </div>

                        <CardDescription className="text-sm leading-relaxed line-clamp-3">
                          {agent.description}
                        </CardDescription>
                      </CardHeader>

                      <CardContent className="space-y-4">
                        {/* Stats */}
                        <div className="flex items-center justify-between text-sm text-text-secondary dark:text-text-secondary-dark">
                          <div className="flex items-center space-x-1">
                            <Star className="h-4 w-4 text-yellow-500 fill-current" />
                            <span>{agent.statistics?.average_rating?.toFixed(1) || '0.0'}</span>
                            <span className="text-xs">({agent.statistics?.total_ratings || 0})</span>
                          </div>
                          <div className="flex items-center space-x-1">
                            <Users className="h-4 w-4" />
                            <span>{agent.statistics?.total_conversations || 0}</span>
                          </div>
                        </div>

                        {/* Model Info */}
                        <div className="text-xs text-text-secondary dark:text-text-secondary-dark">
                          <p>模型: {agent.model_config?.model_name || (agent as any).model_name || '未知'}</p>
                          <p>创建者: {agent.owner?.username || '未知'}</p>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>

                {/* Pagination */}
                {pagination.pages > 1 && (
                  <div className="flex justify-center items-center space-x-2">
                    <Button
                      variant="outline"
                      disabled={pagination.page <= 1}
                      onClick={() => handlePageChange(pagination.page - 1)}
                    >
                      上一页
                    </Button>
                    <span className="text-sm text-text-secondary dark:text-text-secondary-dark">
                      第 {pagination.page} 页，共 {pagination.pages} 页
                    </span>
                    <Button
                      variant="outline"
                      disabled={pagination.page >= pagination.pages}
                      onClick={() => handlePageChange(pagination.page + 1)}
                    >
                      下一页
                    </Button>
                  </div>
                )}
              </>
            )}
          </>
        )}
      </div>
    </div>
  )
}