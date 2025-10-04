'use client'

import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { GlassCard } from '@/components/ui/glass-card'
import { GlassButton } from '@/components/ui/glass-button'
import { GlassBadge } from '@/components/ui/glass-badge'
import { MetricCard } from '@/components/ui/metric-card'
import { MetricSparkline } from '@/components/ui/charts/metric-sparkline'
import { agentService } from '@/services/agents'
import type { Agent } from '@/types'
import {
  ArrowLeft,
  Star,
  Users,
  Heart,
  MessageSquare,
  TrendingUp,
  DollarSign,
  Globe,
  Calendar,
  Tag,
  Zap,
} from 'lucide-react'

export default function AgentDetailPage() {
  const params = useParams()
  const router = useRouter()
  const [agent, setAgent] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isFavorite, setIsFavorite] = useState(false)

  const agentId = params.id as string

  useEffect(() => {
    if (agentId) {
      fetchAgentDetail()
    }
  }, [agentId])

  const fetchAgentDetail = async () => {
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

  const handleFavorite = async () => {
    try {
      const newFavorite = !isFavorite
      await agentService.toggleFavorite(parseInt(agentId), newFavorite)
      setIsFavorite(newFavorite)
    } catch (err) {
      console.error('Error toggling favorite:', err)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-500/20 border-green-400/30 text-green-100'
      case 'inactive': return 'bg-gray-500/20 border-gray-400/30 text-gray-100'
      case 'draft': return 'bg-yellow-500/20 border-yellow-400/30 text-yellow-100'
      default: return 'bg-gray-500/20 border-gray-400/30 text-gray-100'
    }
  }

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'chat': return 'bg-blue-500/20 border-blue-400/30 text-blue-100'
      case 'task': return 'bg-green-500/20 border-green-400/30 text-green-100'
      case 'code': return 'bg-orange-500/20 border-orange-400/30 text-orange-100'
      case 'creative': return 'bg-purple-500/20 border-purple-400/30 text-purple-100'
      default: return 'bg-gray-500/20 border-gray-400/30 text-gray-100'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-gray-50 to-slate-100">
        <div className="container py-8">
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-slate-400"></div>
            <p className="mt-4 text-slate-600">正在加载 AI Agent 详情...</p>
          </div>
        </div>
      </div>
    )
  }

  const agentData = agent

  // Generate mock data for charts and reviews (since we don't have extended data from basic API)
  const revenueData = Array.from({ length: 12 }, (_, i) => ({
    value: Math.floor(Math.random() * 100000) + 50000,
    label: new Date(Date.now() - (11 - i) * 30 * 24 * 60 * 60 * 1000).toLocaleDateString('zh-CN', { month: 'short' })
  }))

  const userGrowthData = Array.from({ length: 12 }, (_, i) => ({
    value: Math.floor(Math.random() * 1000) + 500,
    label: new Date(Date.now() - (11 - i) * 30 * 24 * 60 * 60 * 1000).toLocaleDateString('zh-CN', { month: 'short' })
  }))

  // Mock reviews data
  const reviews = [
    {
      id: 1,
      rating: 5,
      title: "非常好用",
      content: "这个AI助手真的很棒，帮我解决了很多问题。",
      created_at: "2024-01-15",
      user: { name: "张三" }
    },
    {
      id: 2,
      rating: 4,
      title: "体验不错",
      content: "整体体验很好，希望能继续优化。",
      created_at: "2024-01-10",
      user: { name: "李四" }
    }
  ]

  // Use tags and pricing_plans from agent data
  const tags = agentData.tags || []
  const pricing_plans = agentData.pricing_plans || []

  if (error || !agent) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-gray-50 to-slate-100">
        <div className="container py-8">
          <div className="text-center py-12">
            <div className="text-slate-600 mb-4">
              <p>{error || 'AI Agent 未找到'}</p>
            </div>
            <GlassButton onClick={() => router.back()} variant="outline">
              <ArrowLeft className="mr-2 h-4 w-4" />
              返回
            </GlassButton>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-gray-50 to-slate-100">
      <div className="container py-8">
        {/* Back Button */}
        <GlassButton
          variant="ghost"
          onClick={() => router.back()}
          className="mb-6"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          返回
        </GlassButton>

        {/* Agent Header */}
        <div className="mb-8">
          <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between mb-6">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-4">
                <h1 className="text-3xl md:text-4xl font-bold text-slate-800">
                  {agentData.name}
                </h1>
                <div className="flex flex-wrap gap-2">
                  <GlassBadge variant={agentData.type === 'chat' ? 'primary' : 'secondary'}>
                    {agentData.type}
                  </GlassBadge>
                  <GlassBadge className={getStatusColor(agentData.status)}>
                    {agentData.status}
                  </GlassBadge>
                </div>
              </div>

              <p className="text-lg text-slate-600 mb-4">
                {agentData.one_liner || agentData.description}
              </p>

              <div className="flex items-center gap-6 text-slate-500">
                <div className="flex items-center space-x-1">
                  <Star className="h-4 w-4 text-yellow-400 fill-current" />
                  <span className="font-medium">{agentData.average_rating?.toFixed(1) || '0.0'}</span>
                  <span className="text-xs">({agentData.total_ratings || 0})</span>
                </div>
                <div className="flex items-center space-x-1">
                  <MessageSquare className="h-4 w-4" />
                  <span className="font-medium">{agentData.total_reviews || 0}</span>
                  <span className="text-xs">评论</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Heart className="h-4 w-4 text-red-400" />
                  <span className="font-medium">{agentData.total_favorites || 0}</span>
                  <span className="text-xs">收藏</span>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-3 mt-6 lg:mt-0">
              <GlassButton
                variant="primary"
                glow
                disabled={agentData.status !== 'active'}
              >
                <Zap className="mr-2 h-4 w-4" />
                开始对话
              </GlassButton>
              <GlassButton
                variant="outline"
                onClick={handleFavorite}
              >
                <Heart className={`mr-2 h-4 w-4 ${isFavorite ? 'fill-current text-red-400' : ''}`} />
                {isFavorite ? '已收藏' : '收藏'}
              </GlassButton>
            </div>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <MetricCard
            title="月活用户"
            value={agentData.monthly_active_users || 0}
            icon={<Users className="h-5 w-5" />}
            trend={{
              value: agentData.growth_rate || 0,
              direction: agentData.growth_rate > 0 ? 'up' : 'down'
            }}
          />
          <MetricCard
            title="年度经常性收入"
            value={`$${((agentData.annual_recurring_revenue || 0) / 1000000).toFixed(1)}M`}
            icon={<DollarSign className="h-5 w-5" />}
          />
          <MetricCard
            title="月度经常性收入"
            value={`$${((agentData.monthly_recurring_revenue || 0) / 1000000).toFixed(1)}M`}
            icon={<TrendingUp className="h-5 w-5" />}
          />
          <MetricCard
            title="流量排名"
            value={`#${agentData.traffic_rank || 'N/A'}`}
            icon={<TrendingUp className="h-5 w-5" />}
          />
        </div>

        {/* Performance & Analytics */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Performance Metrics */}
          <GlassCard variant="subtle" className="p-6">
            <h3 className="text-xl font-semibold text-slate-800 mb-6">性能指标</h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-slate-600">响应时间</span>
                <span className="text-slate-800 font-medium">
                  {(agentData.average_response_time || 0).toFixed(1)}s
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-600">成功率</span>
                <span className="text-slate-800 font-medium">
                  {(agentData.success_rate || 0).toFixed(1)}%
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-600">准确率</span>
                <span className="text-slate-800 font-medium">94.7%</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-600">正常运行时间</span>
                <span className="text-slate-800 font-medium">99.9%</span>
              </div>
            </div>
          </GlassCard>

          {/* Revenue Analytics */}
          <GlassCard variant="subtle" className="p-6">
            <h3 className="text-xl font-semibold text-slate-800 mb-6">收入分析</h3>
            <div className="h-32">
              <MetricSparkline
                title="月度收入趋势"
                current={agentData.monthly_recurring_revenue || 0}
                data={revenueData}
                format="currency"
                color="green"
              />
            </div>
          </GlassCard>
        </div>

        {/* Comprehensive Overview */}
        <GlassCard variant="subtle" className="p-8 mb-8">
          <h3 className="text-2xl font-semibold text-slate-800 mb-6">综合概述</h3>
          <div className="prose max-w-none">
            <div className="text-slate-700 leading-relaxed whitespace-pre-line">
              {agentData.detailed_description || agentData.description || '暂无详细介绍'}
            </div>
          </div>
        </GlassCard>

        {/* User Reviews & Tags */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* User Reviews */}
          <GlassCard variant="subtle" className="p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-semibold text-slate-800">用户评价</h3>
              <MessageSquare className="h-5 w-5 text-slate-500" />
            </div>

            {reviews && reviews.length > 0 ? (
              <div className="space-y-4">
                {reviews.slice(0, 3).map((review: any) => (
                  <div key={review.id} className="border-b border-slate-200 pb-4 last:border-0">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center space-x-2">
                        <div className="flex text-yellow-400">
                          {'★'.repeat(Math.floor(review.rating))}
                          {'☆'.repeat(5 - Math.floor(review.rating))}
                        </div>
                        <span className="text-slate-600 text-sm">
                          {review.user_username || '匿名用户'}
                        </span>
                      </div>
                      <span className="text-slate-500 text-xs">
                        {new Date(review.created_at).toLocaleDateString()}
                      </span>
                    </div>
                    {review.title && (
                      <h4 className="text-slate-800 font-medium mb-1">{review.title}</h4>
                    )}
                    {review.content && (
                      <p className="text-slate-700 text-sm">{review.content}</p>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-slate-500">
                <MessageSquare className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>暂无用户评价</p>
                <p className="text-sm mt-2">成为第一个评价这个 AI Agent 的用户</p>
              </div>
            )}
          </GlassCard>

          {/* Tags & Pricing */}
          <div className="space-y-6">
            {/* Tags */}
            <GlassCard variant="subtle" className="p-6">
              <h3 className="text-xl font-semibold text-slate-800 mb-4">标签</h3>
              <div className="flex flex-wrap gap-2">
                {tags && tags.length > 0 ? (
                  tags.map((tag: string, index: number) => (
                    <GlassBadge key={index} variant="secondary">
                      <Tag className="w-3 h-3 mr-1" />
                      {tag}
                    </GlassBadge>
                  ))
                ) : (
                  <p className="text-slate-600 text-sm">暂无标签</p>
                )}
              </div>
            </GlassCard>

            {/* Pricing Plans */}
            <GlassCard variant="subtle" className="p-6">
              <h3 className="text-xl font-semibold text-slate-800 mb-4">价格方案</h3>
              <div className="space-y-3">
                {pricing_plans && pricing_plans.length > 0 ? (
                  pricing_plans.map((plan: any, index: number) => (
                    <div
                      key={index}
                      className="flex justify-between items-center p-3 bg-slate-50 rounded-lg"
                    >
                      <div>
                        <div className="text-slate-800 font-medium">{plan.name}</div>
                        <div className="text-slate-600 text-sm">{plan.description}</div>
                      </div>
                      <div className="text-slate-800 font-bold">
                        ${plan.price}/{plan.interval}
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="text-slate-600 text-sm">暂无价格信息</p>
                )}
              </div>
            </GlassCard>
          </div>
        </div>

        {/* Additional Info */}
        <GlassCard variant="subtle" className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="flex items-center space-x-3">
              <Globe className="h-5 w-5 text-slate-500" />
              <div>
                <div className="text-slate-600 text-sm">官方网站</div>
                <div className="text-slate-800">
                  {agentData.website_url ? (
                    <a
                      href={agentData.website_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="hover:text-blue-600 transition-colors"
                    >
                      {agentData.website_url}
                    </a>
                  ) : (
                    '未提供'
                  )}
                </div>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <Calendar className="h-5 w-5 text-slate-500" />
              <div>
                <div className="text-slate-600 text-sm">上线日期</div>
                <div className="text-slate-800">
                  {agentData.published_at
                    ? new Date(agentData.published_at).toLocaleDateString('zh-CN')
                    : '未发布'}
                </div>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <Users className="h-5 w-5 text-slate-500" />
              <div>
                <div className="text-slate-600 text-sm">创建者</div>
                <div className="text-slate-800">
                  {agentData.owner?.username || '未知用户'}
                </div>
              </div>
            </div>
          </div>
        </GlassCard>
      </div>
    </div>
  )
}