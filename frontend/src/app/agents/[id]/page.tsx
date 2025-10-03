'use client'

import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { agentService } from '@/services/agents'
import type { Agent } from '@/types'
import { ArrowLeft, Star, Users, Settings, Play, Share2, Heart, MessageSquare } from 'lucide-react'

export default function AgentDetailPage() {
  const params = useParams()
  const router = useRouter()
  const [agent, setAgent] = useState<Agent | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const agentId = params.id as string

  useEffect(() => {
    if (agentId) {
      fetchAgent()
    }
  }, [agentId])

  const fetchAgent = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await agentService.getAgentById(parseInt(agentId))
      if (response.success && response.data) {
        setAgent(response.data)
      } else {
        setError(response.message || 'Failed to fetch agent details')
      }
    } catch (err) {
      setError('Failed to fetch agent details')
      console.error('Error fetching agent:', err)
    } finally {
      setLoading(false)
    }
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

  if (loading) {
    return (
      <div className="min-h-screen bg-background dark:bg-background-dark">
        <div className="container py-8">
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-accent dark:border-accent-dark"></div>
            <p className="mt-4 text-text-secondary dark:text-text-secondary-dark">正在加载 AI Agent 详情...</p>
          </div>
        </div>
      </div>
    )
  }

  if (error || !agent) {
    return (
      <div className="min-h-screen bg-background dark:bg-background-dark">
        <div className="container py-8">
          <div className="text-center py-12">
            <div className="text-red-500 dark:text-red-400 mb-4">
              <p>{error || 'AI Agent 未找到'}</p>
            </div>
            <Button onClick={() => router.back()} variant="outline">
              <ArrowLeft className="mr-2 h-4 w-4" />
              返回
            </Button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background dark:bg-background-dark">
      <div className="container py-8">
        {/* Back Button */}
        <Button
          variant="ghost"
          onClick={() => router.back()}
          className="mb-6"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          返回
        </Button>

        {/* Agent Header */}
        <div className="mb-8">
          <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between mb-6">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-4">
                <h1 className="text-3xl md:text-4xl font-bold text-text-primary dark:text-text-primary-dark">
                  {agent.name}
                </h1>
                <div className="flex flex-wrap gap-2">
                  <Badge
                    variant="secondary"
                    className={`text-sm ${getTypeColor(agent.type)}`}
                  >
                    {agent.type}
                  </Badge>
                  <Badge
                    variant="secondary"
                    className={`text-sm ${getStatusColor(agent.status)}`}
                  >
                    {agent.status}
                  </Badge>
                  <Badge
                    variant="secondary"
                    className={`text-sm ${getVisibilityColor(agent.visibility)}`}
                  >
                    {agent.visibility}
                  </Badge>
                </div>
              </div>

              <p className="text-lg text-text-secondary dark:text-text-secondary-dark mb-4">
                {agent.description}
              </p>

              <div className="flex items-center gap-6 text-sm text-text-secondary dark:text-text-secondary-dark">
                <div className="flex items-center space-x-1">
                  <Star className="h-4 w-4 text-yellow-500 fill-current" />
                  <span className="font-medium">{agent.statistics?.average_rating?.toFixed(1) || '0.0'}</span>
                  <span className="text-xs">({agent.statistics?.total_ratings || 0} 评价)</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Users className="h-4 w-4" />
                  <span className="font-medium">{agent.statistics?.total_conversations || 0}</span>
                  <span className="text-xs">对话</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Heart className="h-4 w-4 text-red-500" />
                  <span className="font-medium">{agent.statistics?.total_favorites || 0}</span>
                  <span className="text-xs">收藏</span>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-3 mt-6 lg:mt-0">
              <Button
                className="bg-accent dark:bg-accent-dark hover:bg-opacity-90 text-white"
                disabled={agent.status !== 'active'}
              >
                <Play className="mr-2 h-4 w-4" />
                开始对话
              </Button>
              <Button variant="outline">
                <Heart className="mr-2 h-4 w-4" />
                收藏
              </Button>
              <Button variant="outline">
                <Share2 className="mr-2 h-4 w-4" />
                分享
              </Button>
            </div>
          </div>
        </div>

        {/* Agent Details */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Detailed Description */}
            <Card>
              <CardHeader>
                <CardTitle>详细介绍</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="prose dark:prose-invert max-w-none">
                  <p className="text-text-secondary dark:text-text-secondary-dark leading-relaxed">
                    {agent.description}
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Model Configuration */}
            <Card>
              <CardHeader>
                <CardTitle>模型配置</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm font-medium text-text-primary dark:text-text-primary-dark mb-1">
                      模型名称
                    </p>
                    <p className="text-text-secondary dark:text-text-secondary-dark">
                      {agent.model_config?.model_name || (agent as any).model_name || '未知'}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-text-primary dark:text-text-primary-dark mb-1">
                      温度
                    </p>
                    <p className="text-text-secondary dark:text-text-secondary-dark">
                      {agent.model_config?.temperature ?? (agent as any).temperature ?? 0.7}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-text-primary dark:text-text-primary-dark mb-1">
                      最大令牌数
                    </p>
                    <p className="text-text-secondary dark:text-text-secondary-dark">
                      {agent.model_config?.max_tokens ?? (agent as any).max_tokens ?? 2048}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-text-primary dark:text-text-primary-dark mb-1">
                      系统提示
                    </p>
                    <p className="text-text-secondary dark:text-text-secondary-dark line-clamp-2">
                      {agent.model_config?.system_prompt || (agent as any).system_prompt || '未设置'}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Reviews */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  用户评价
                  <MessageSquare className="h-5 w-5 text-text-secondary dark:text-text-secondary-dark" />
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center py-8 text-text-secondary dark:text-text-secondary-dark">
                  <MessageSquare className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p>暂无用户评价</p>
                  <p className="text-sm mt-2">成为第一个评价这个 AI Agent 的用户</p>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Creator Info */}
            <Card>
              <CardHeader>
                <CardTitle>创建者</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-accent dark:bg-accent-dark rounded-full flex items-center justify-center">
                    <span className="text-white font-medium">
                      {agent.owner?.username?.charAt(0).toUpperCase() || 'U'}
                    </span>
                  </div>
                  <div>
                    <p className="font-medium text-text-primary dark:text-text-primary-dark">
                      {agent.owner?.username || '未知用户'}
                    </p>
                    <p className="text-sm text-text-secondary dark:text-text-secondary-dark">
                      {agent.owner?.full_name || ''}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Stats */}
            <Card>
              <CardHeader>
                <CardTitle>统计信息</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-text-secondary dark:text-text-secondary-dark">创建时间</span>
                  <span className="text-sm font-medium text-text-primary dark:text-text-primary-dark">
                    {new Date(agent.created_at).toLocaleDateString('zh-CN')}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-text-secondary dark:text-text-secondary-dark">更新时间</span>
                  <span className="text-sm font-medium text-text-primary dark:text-text-primary-dark">
                    {new Date(agent.updated_at).toLocaleDateString('zh-CN')}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-text-secondary dark:text-text-secondary-dark">版本</span>
                  <span className="text-sm font-medium text-text-primary dark:text-text-primary-dark">
                    {(agent as any).version || '1.0.0'}
                  </span>
                </div>
              </CardContent>
            </Card>

            {/* Tags */}
            <Card>
              <CardHeader>
                <CardTitle>标签</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {(agent as any).tags && (agent as any).tags.length > 0 ? (
                    (agent as any).tags.map((tag: string, index: number) => (
                      <Badge key={index} variant="secondary" className="text-xs">
                        {tag}
                      </Badge>
                    ))
                  ) : (
                    <p className="text-sm text-text-secondary dark:text-text-secondary-dark">
                      暂无标签
                    </p>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}