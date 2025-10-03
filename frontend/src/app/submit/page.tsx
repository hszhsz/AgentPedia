'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import agentService from '@/services/agents'
import { useAuth } from '@/contexts/AuthContext'
import { useIntl } from '@/components/providers/intl-provider'
import { ArrowLeft, Save, Eye, EyeOff, Globe, Lock, Users } from 'lucide-react'

interface FormData {
  name: string
  description: string
  type: 'chat' | 'task' | 'code' | 'creative'
  visibility: 'public' | 'private' | 'unlisted'
  model_config: {
    provider: string
    model_name: string
    temperature: number
    max_tokens: number
    top_p: number
    frequency_penalty: number
    presence_penalty: number
  }
  functional_config: {
    system_prompt: string
    welcome_message: string
    max_conversation_length: number
    enable_memory: boolean
    enable_web_search: boolean
    enable_code_execution: boolean
    allowed_file_types: string[]
  }
  rate_limits: {
    requests_per_minute: number
    requests_per_hour: number
    requests_per_day: number
  }
}

const modelProviders = [
  { value: 'openai', label: 'OpenAI' },
  { value: 'anthropic', label: 'Anthropic' },
  { value: 'google', label: 'Google' },
  { value: 'meta', label: 'Meta' },
  { value: 'cohere', label: 'Cohere' },
  { value: 'other', label: 'Other' }
]

const agentTypes = [
  { value: 'chat', label: 'Chat Agent', description: '对话型智能体' },
  { value: 'task', label: 'Task Agent', description: '任务型智能体' },
  { value: 'code', label: 'Code Agent', description: '编程型智能体' },
  { value: 'creative', label: 'Creative Agent', description: '创意型智能体' }
]

const visibilityOptions = [
  { value: 'public', label: '公开', icon: Globe, description: '所有人可见' },
  { value: 'private', label: '私密', icon: Lock, description: '仅自己可见' },
  { value: 'unlisted', label: '不公开', icon: Users, description: '链接可见' }
]

export default function SubmitAgentPage() {
  const router = useRouter()
  const { user } = useAuth()
  const { t } = useIntl()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)

  const [formData, setFormData] = useState<FormData>({
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
      presence_penalty: 0.0
    },
    functional_config: {
      system_prompt: '',
      welcome_message: '你好！我是你的AI助手，有什么可以帮助你的吗？',
      max_conversation_length: 50,
      enable_memory: true,
      enable_web_search: false,
      enable_code_execution: false,
      allowed_file_types: ['txt', 'pdf', 'doc', 'docx']
    },
    rate_limits: {
      requests_per_minute: 60,
      requests_per_hour: 3600,
      requests_per_day: 86400
    }
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!user) {
      setError('请先登录')
      return
    }

    setLoading(true)
    setError('')

    try {
      await agentService.createAgent(formData)
      setSuccess(true)
      setTimeout(() => {
        router.push('/agents')
      }, 2000)
    } catch (err: any) {
      setError(err.message || '创建失败')
    } finally {
      setLoading(false)
    }
  }

  const updateFormData = (path: string[], value: any) => {
    setFormData(prev => {
      const newData = { ...prev }
      let current: any = newData
      for (let i = 0; i < path.length - 1; i++) {
        current = current[path[i]]
      }
      current[path[path.length - 1]] = value
      return newData
    })
  }

  if (success) {
    return (
      <div className="min-h-screen bg-background dark:bg-background-dark flex items-center justify-center">
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <CardTitle className="text-green-600">创建成功！</CardTitle>
            <CardDescription>你的Agent已成功创建，即将跳转到Agent列表...</CardDescription>
          </CardHeader>
        </Card>
      </div>
    )
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-background dark:bg-background-dark flex items-center justify-center">
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <CardTitle>需要登录</CardTitle>
            <CardDescription>请先登录以创建Agent</CardDescription>
          </CardHeader>
          <CardFooter>
            <Button onClick={() => router.push('/login')} className="w-full">
              前往登录
            </Button>
          </CardFooter>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background dark:bg-background-dark">
      <div className="container mx-auto py-8 px-4">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="mb-8">
            <Button
              variant="ghost"
              onClick={() => router.back()}
              className="mb-4"
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              返回
            </Button>
            <h1 className="text-3xl font-bold text-text-primary dark:text-text-primary-dark mb-2">
              提交你的 Agent
            </h1>
            <p className="text-text-secondary dark:text-text-secondary-dark">
              创建一个自定义的AI智能体，与其他用户分享你的创意
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-8">
            {/* Basic Information */}
            <Card>
              <CardHeader>
                <CardTitle>基本信息</CardTitle>
                <CardDescription>设置你的Agent的基本属性</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Agent 名称 *</label>
                  <Input
                    value={formData.name}
                    onChange={(e) => updateFormData(['name'], e.target.value)}
                    placeholder="给你的Agent起个名字"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">描述 *</label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => updateFormData(['description'], e.target.value)}
                    placeholder="描述你的Agent的功能和特点"
                    className="w-full px-3 py-2 border border-border dark:border-border-dark rounded-md bg-background dark:bg-background-dark text-text-primary dark:text-text-primary-dark"
                    rows={3}
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Agent 类型 *</label>
                  <div className="grid grid-cols-2 gap-3">
                    {agentTypes.map((type) => (
                      <div
                        key={type.value}
                        onClick={() => updateFormData(['type'], type.value)}
                        className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                          formData.type === type.value
                            ? 'border-accent dark:border-accent-dark bg-accent/10 dark:bg-accent-dark/10'
                            : 'border-border dark:border-border-dark hover:border-accent dark:hover:border-accent-dark'
                        }`}
                      >
                        <div className="font-medium">{type.label}</div>
                        <div className="text-sm text-text-secondary dark:text-text-secondary-dark">
                          {type.description}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">可见性</label>
                  <div className="grid grid-cols-3 gap-3">
                    {visibilityOptions.map((option) => {
                      const Icon = option.icon
                      return (
                        <div
                          key={option.value}
                          onClick={() => updateFormData(['visibility'], option.value)}
                          className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                            formData.visibility === option.value
                              ? 'border-accent dark:border-accent-dark bg-accent/10 dark:bg-accent-dark/10'
                              : 'border-border dark:border-border-dark hover:border-accent dark:hover:border-accent-dark'
                          }`}
                        >
                          <Icon className="h-5 w-5 mb-2" />
                          <div className="font-medium">{option.label}</div>
                          <div className="text-sm text-text-secondary dark:text-text-secondary-dark">
                            {option.description}
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Model Configuration */}
            <Card>
              <CardHeader>
                <CardTitle>模型配置</CardTitle>
                <CardDescription>配置AI模型的相关参数</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">模型提供商 *</label>
                    <select
                      value={formData.model_config.provider}
                      onChange={(e) => updateFormData(['model_config', 'provider'], e.target.value)}
                      className="w-full px-3 py-2 border border-border dark:border-border-dark rounded-md bg-background dark:bg-background-dark text-text-primary dark:text-text-primary-dark"
                    >
                      {modelProviders.map((provider) => (
                        <option key={provider.value} value={provider.value}>
                          {provider.label}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">模型名称 *</label>
                    <Input
                      value={formData.model_config.model_name}
                      onChange={(e) => updateFormData(['model_config', 'model_name'], e.target.value)}
                      placeholder="gpt-3.5-turbo"
                      required
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      温度 ({formData.model_config.temperature})
                    </label>
                    <input
                      type="range"
                      min="0"
                      max="2"
                      step="0.1"
                      value={formData.model_config.temperature}
                      onChange={(e) => updateFormData(['model_config', 'temperature'], parseFloat(e.target.value))}
                      className="w-full"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">
                      最大Token数 ({formData.model_config.max_tokens})
                    </label>
                    <Input
                      type="number"
                      min="1"
                      max="32000"
                      value={formData.model_config.max_tokens}
                      onChange={(e) => updateFormData(['model_config', 'max_tokens'], parseInt(e.target.value))}
                    />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Functional Configuration */}
            <Card>
              <CardHeader>
                <CardTitle>功能配置</CardTitle>
                <CardDescription>设置Agent的功能特性</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">系统提示词</label>
                  <textarea
                    value={formData.functional_config.system_prompt}
                    onChange={(e) => updateFormData(['functional_config', 'system_prompt'], e.target.value)}
                    placeholder="定义Agent的角色和行为规则..."
                    className="w-full px-3 py-2 border border-border dark:border-border-dark rounded-md bg-background dark:bg-background-dark text-text-primary dark:text-text-primary-dark"
                    rows={4}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">欢迎消息</label>
                  <Input
                    value={formData.functional_config.welcome_message}
                    onChange={(e) => updateFormData(['functional_config', 'welcome_message'], e.target.value)}
                    placeholder="用户开始对话时的欢迎消息"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      最大对话长度 ({formData.functional_config.max_conversation_length})
                    </label>
                    <Input
                      type="number"
                      min="1"
                      max="1000"
                      value={formData.functional_config.max_conversation_length}
                      onChange={(e) => updateFormData(['functional_config', 'max_conversation_length'], parseInt(e.target.value))}
                    />
                  </div>

                  <div className="flex items-center space-x-4">
                    <label className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={formData.functional_config.enable_memory}
                        onChange={(e) => updateFormData(['functional_config', 'enable_memory'], e.target.checked)}
                      />
                      <span className="text-sm">启用记忆</span>
                    </label>

                    <label className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={formData.functional_config.enable_web_search}
                        onChange={(e) => updateFormData(['functional_config', 'enable_web_search'], e.target.checked)}
                      />
                      <span className="text-sm">启用网络搜索</span>
                    </label>

                    <label className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={formData.functional_config.enable_code_execution}
                        onChange={(e) => updateFormData(['functional_config', 'enable_code_execution'], e.target.checked)}
                      />
                      <span className="text-sm">启用代码执行</span>
                    </label>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Rate Limits */}
            <Card>
              <CardHeader>
                <CardTitle>速率限制</CardTitle>
                <CardDescription>设置Agent的使用限制</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">每分钟限制</label>
                    <Input
                      type="number"
                      min="1"
                      value={formData.rate_limits.requests_per_minute}
                      onChange={(e) => updateFormData(['rate_limits', 'requests_per_minute'], parseInt(e.target.value))}
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">每小时限制</label>
                    <Input
                      type="number"
                      min="1"
                      value={formData.rate_limits.requests_per_hour}
                      onChange={(e) => updateFormData(['rate_limits', 'requests_per_hour'], parseInt(e.target.value))}
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">每天限制</label>
                    <Input
                      type="number"
                      min="1"
                      value={formData.rate_limits.requests_per_day}
                      onChange={(e) => updateFormData(['rate_limits', 'requests_per_day'], parseInt(e.target.value))}
                    />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Error Display */}
            {error && (
              <Card className="border-red-200 dark:border-red-800">
                <CardContent className="pt-6">
                  <p className="text-red-600 dark:text-red-400">{error}</p>
                </CardContent>
              </Card>
            )}

            {/* Submit Button */}
            <div className="flex justify-end">
              <Button
                type="submit"
                disabled={loading || !formData.name || !formData.description}
                className="px-8"
              >
                <Save className="h-4 w-4 mr-2" />
                {loading ? '创建中...' : '创建 Agent'}
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}