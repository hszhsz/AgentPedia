'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { useIntl } from '@/components/providers/intl-provider'
import { Clock, ExternalLink, ArrowRight } from 'lucide-react'

interface Agent {
  id: string
  name: string
  description: string
  category: string
  status: 'released' | 'beta' | 'alpha' | 'concept'
  addedDate: string
  tags: string[]
  icon: string
  website?: string
}

const latestAgents: Agent[] = [
  {
    id: '7',
    name: 'Cursor',
    description: 'AI 驱动的代码编辑器，深度集成了 GPT-4，提供智能编程辅助',
    category: 'development',
    status: 'beta',
    addedDate: '2024-01-15',
    tags: ['编程', 'IDE', 'AI辅助'],
    icon: '🎯',
    website: 'https://cursor.sh'
  },
  {
    id: '8',
    name: 'Suno AI',
    description: 'AI 音乐生成平台，根据文本描述创作原创音乐和歌曲',
    category: 'entertainment',
    status: 'released',
    addedDate: '2024-01-12',
    tags: ['音乐生成', '创作', 'AI作曲'],
    icon: '🎵',
    website: 'https://suno.ai'
  },
  {
    id: '9',
    name: 'Pika Labs',
    description: 'AI 视频生成工具，将文本和图像转换为高质量视频内容',
    category: 'entertainment',
    status: 'beta',
    addedDate: '2024-01-10',
    tags: ['视频生成', '动画', '创作'],
    icon: '🎬',
    website: 'https://pika.art'
  },
  {
    id: '10',
    name: 'LlamaIndex',
    description: '连接 LLMs 与您的数据的框架，构建智能文档和知识应用',
    category: 'development',
    status: 'released',
    addedDate: '2024-01-08',
    tags: ['RAG', '数据处理', 'LLM框架'],
    icon: '📚',
    website: 'https://llamaindex.ai'
  },
  {
    id: '11',
    name: 'ElevenLabs',
    description: 'AI 语音合成平台，生成自然流畅的人声和语音克隆',
    category: 'communication',
    status: 'released',
    addedDate: '2024-01-05',
    tags: ['语音合成', '配音', '音频处理'],
    icon: '🎤',
    website: 'https://elevenlabs.io'
  },
  {
    id: '12',
    name: 'LangChain',
    description: '构建 LLM 应用的开发框架，提供模块化组件和工具链',
    category: 'development',
    status: 'released',
    addedDate: '2024-01-03',
    tags: ['LLM框架', '开发工具', 'Agent构建'],
    icon: '⛓️',
    website: 'https://langchain.com'
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

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now.getTime() - date.getTime())
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 1) return '1天前'
  if (diffDays < 7) return `${diffDays}天前`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)}周前`
  return `${Math.floor(diffDays / 30)}个月前`
}

export function LatestAgents() {
  const { t } = useIntl()

  return (
    <section className="py-20 bg-surface dark:bg-surface-dark">
      <div className="container">
        {/* Section Header */}
        <div className="text-center mb-16">
          <Badge variant="secondary" className="mb-4">
            🆕 最新上线
          </Badge>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-text-primary dark:text-text-primary-dark mb-4">
            {t('latest.title')}
          </h2>
          <p className="text-lg md:text-xl text-text-secondary dark:text-text-secondary-dark max-w-3xl mx-auto">
            探索最新加入平台的 AI Agent 项目，第一时间体验前沿 AI 技术
          </p>
        </div>

        {/* Timeline Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
          {latestAgents.map((agent, index) => (
            <div key={agent.id} className="relative">
              {/* Timeline Line */}
              {index < latestAgents.length - 1 && (
                <div className="hidden lg:block absolute top-full left-1/2 transform -translate-x-1/2 w-0.5 h-8 bg-border dark:border-border-dark" />
              )}

              <Card
                className="group hover:shadow-xl transition-all duration-300 border-border dark:border-border-dark hover:border-accent dark:hover:border-accent-dark cursor-pointer relative"
                onClick={() => window.location.href = `/agents/${agent.id}`}
              >
                {/* New Badge */}
                <div className="absolute -top-2 -right-2 z-10">
                  <Badge className="bg-accent dark:bg-accent-dark text-white text-xs">
                    NEW
                  </Badge>
                </div>

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
                          <div className="flex items-center space-x-1 text-xs text-text-secondary dark:text-text-secondary-dark">
                            <Clock className="h-3 w-3" />
                            <span>{formatDate(agent.addedDate)}</span>
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

                  {/* Action Button */}
                  <div className="flex items-center justify-between">
                    <div className="text-xs text-text-secondary dark:text-text-secondary-dark">
                      刚刚加入
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
            </div>
          ))}
        </div>

        {/* CTA Section */}
        <div className="text-center">
          <Button
            variant="outline"
            size="lg"
            className="border-border dark:border-border-dark hover:bg-accent dark:hover:bg-accent-dark hover:text-white px-8 py-4"
            onClick={() => window.location.href = '/agents?sort=newest'}
          >
            查看最新发布
            <ArrowRight className="ml-2 h-5 w-5" />
          </Button>
          <p className="mt-4 text-sm text-text-secondary dark:text-text-secondary-dark">
            持续更新中，每天都有新的 AI Agent 加入
          </p>
        </div>
      </div>
    </section>
  )
}