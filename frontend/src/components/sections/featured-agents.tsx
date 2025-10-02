'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { useIntl } from '@/components/providers/intl-provider'
import { Star, Users, ExternalLink, ArrowRight } from 'lucide-react'

interface Agent {
  id: string
  name: string
  description: string
  category: string
  status: 'released' | 'beta' | 'alpha' | 'concept'
  rating: number
  users: string
  tags: string[]
  icon: string
  website?: string
}

const featuredAgents: Agent[] = [
  {
    id: '1',
    name: 'ChatGPT',
    description: 'OpenAI 开发的强大对话式 AI 助手，支持自然语言理解和生成',
    category: 'communication',
    status: 'released',
    rating: 4.8,
    users: '100M+',
    tags: ['对话', '写作', '编程', '翻译'],
    icon: '🤖',
    website: 'https://chat.openai.com'
  },
  {
    id: '2',
    name: 'Claude',
    description: 'Anthropic 开发的 AI 助手，专注于有用、无害、诚实的交互',
    category: 'communication',
    status: 'released',
    rating: 4.7,
    users: '10M+',
    tags: ['对话', '分析', '写作'],
    icon: '🧠',
    website: 'https://claude.ai'
  },
  {
    id: '3',
    name: 'GitHub Copilot',
    description: 'GitHub 与 OpenAI 合作开发的 AI 代码助手，实时代码建议',
    category: 'development',
    status: 'released',
    rating: 4.6,
    users: '1M+',
    tags: ['编程', '代码补全', '多语言'],
    icon: '⚡',
    website: 'https://github.com/features/copilot'
  },
  {
    id: '4',
    name: 'Midjourney',
    description: '基于 AI 的图像生成工具，将文字描述转换为精美图像',
    category: 'entertainment',
    status: 'released',
    rating: 4.9,
    users: '15M+',
    tags: ['图像生成', '艺术创作', '设计'],
    icon: '🎨',
    website: 'https://midjourney.com'
  },
  {
    id: '5',
    name: 'Perplexity',
    description: 'AI 驱动的搜索引擎，提供准确的答案和信息来源',
    category: 'productivity',
    status: 'released',
    rating: 4.5,
    users: '2M+',
    tags: ['搜索', '研究', '问答'],
    icon: '🔍',
    website: 'https://perplexity.ai'
  },
  {
    id: '6',
    name: 'Notion AI',
    description: '集成在 Notion 中的 AI 写作助手，提升内容创作效率',
    category: 'productivity',
    status: 'released',
    rating: 4.4,
    users: '5M+',
    tags: ['写作', '笔记', '协作'],
    icon: '📝',
    website: 'https://notion.so'
  }
]

const getStatusColor = (status: Agent['status']) => {
  switch (status) {
    case 'released': return 'bg-success dark:bg-success-dark'
    case 'beta': return 'bg-warning dark:bg-warning-dark'
    case 'alpha': return 'bg-error dark:bg-error-dark'
    case 'concept': return 'bg-secondary dark:bg-secondary-dark'
    default: return 'bg-secondary dark:bg-secondary-dark'
  }
}

const getStatusText = (status: Agent['status']) => {
  switch (status) {
    case 'released': return '已发布'
    case 'beta': return '测试版'
    case 'alpha': return '内测版'
    case 'concept': return '概念版'
    default: return status
  }
}

export function FeaturedAgents() {
  const { t } = useIntl()

  return (
    <section className="py-20 bg-background dark:bg-background-dark">
      <div className="container">
        {/* Section Header */}
        <div className="text-center mb-16">
          <Badge variant="secondary" className="mb-4">
            ⭐ 精选推荐
          </Badge>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-text-primary dark:text-text-primary-dark mb-4">
            {t('featured.title')}
          </h2>
          <p className="text-lg md:text-xl text-text-secondary dark:text-text-secondary-dark max-w-3xl mx-auto">
            发现最受欢迎和最具创新性的 AI Agent 项目，助力您的工作和生活
          </p>
        </div>

        {/* Agents Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
          {featuredAgents.map((agent) => (
            <Card
              key={agent.id}
              className="group hover:shadow-xl transition-all duration-300 border-border dark:border-border-dark hover:border-accent dark:hover:border-accent-dark cursor-pointer"
              onClick={() => window.location.href = `/agents/${agent.id}`}
            >
              <CardHeader className="pb-4">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center space-x-3">
                    <div className="text-3xl">{agent.icon}</div>
                    <div>
                      <CardTitle className="text-xl group-hover:text-accent dark:group-hover:text-accent-dark transition-colors">
                        {agent.name}
                      </CardTitle>
                      <div className="flex items-center space-x-2 mt-1">
                        <Badge
                          variant="secondary"
                          className={`text-xs ${getStatusColor(agent.status)} text-white`}
                        >
                          {getStatusText(agent.status)}
                        </Badge>
                        <div className="flex items-center space-x-1">
                          <Star className="h-4 w-4 text-yellow-500 fill-current" />
                          <span className="text-sm text-text-secondary dark:text-text-secondary-dark">
                            {agent.rating}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <CardDescription className="text-sm leading-relaxed">
                  {agent.description}
                </CardDescription>
              </CardHeader>

              <CardContent className="space-y-4">
                {/* Tags */}
                <div className="flex flex-wrap gap-2">
                  {agent.tags.map((tag) => (
                    <Badge key={tag} variant="outline" className="text-xs">
                      {tag}
                    </Badge>
                  ))}
                </div>

                {/* Users Count */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2 text-sm text-text-secondary dark:text-text-secondary-dark">
                    <Users className="h-4 w-4" />
                    <span>{agent.users}</span>
                  </div>

                  {agent.website && (
                    <Button
                      variant="ghost"
                      size="sm"
                      className="text-accent dark:text-accent-dark hover:bg-accent dark:hover:bg-accent-dark hover:text-white p-2"
                      onClick={(e) => {
                        e.stopPropagation()
                        window.open(agent.website, '_blank')
                      }}
                    >
                      <ExternalLink className="h-4 w-4" />
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* CTA Section */}
        <div className="text-center">
          <Button
            size="lg"
            className="bg-accent dark:bg-accent-dark hover:bg-opacity-90 text-white px-8 py-4"
            onClick={() => window.location.href = '/agents'}
          >
            查看所有 AI Agents
            <ArrowRight className="ml-2 h-5 w-5" />
          </Button>
          <p className="mt-4 text-sm text-text-secondary dark:text-text-secondary-dark">
            还有更多优秀的 AI Agent 等待您的发现
          </p>
        </div>
      </div>
    </section>
  )
}