'use client'

import { createContext, useContext, useState, useEffect } from 'react'

type Locale = 'zh' | 'en'

interface IntlContextType {
  locale: Locale
  setLocale: (locale: Locale) => void
  t: (key: string, values?: Record<string, string | number>) => string
}

const IntlContext = createContext<IntlContextType | undefined>(undefined)

// 简单的翻译函数，后续可以替换为 next-intl
const translations: Record<Locale, Record<string, string>> = {
  zh: {
    'nav.home': '首页',
    'nav.agents': 'AI Agent',
    'nav.about': '关于',
    'nav.search.placeholder': '搜索AI Agent...',
    'hero.title': 'AgentPedia',
    'hero.subtitle': '全球AI Agent探索平台',
    'hero.description': '发现、探索、了解全球最优秀的AI Agent项目',
    'hero.search.placeholder': '搜索您感兴趣的AI Agent...',
    'featured.title': '热门AI Agent',
    'latest.title': '最新上线',
    'agent.view.details': '查看详情',
    'category.all': '全部分类',
    'category.development': '开发工具',
    'category.productivity': '效率工具',
    'category.communication': '通信协作',
    'category.entertainment': '娱乐休闲',
    'category.education': '教育学习',
    'status.released': '已发布',
    'status.beta': '测试版',
    'status.alpha': '内测版',
    'status.concept': '概念版',
    'theme.toggle': '切换主题',
    'language.switch': '切换语言',
  },
  en: {
    'nav.home': 'Home',
    'nav.agents': 'AI Agents',
    'nav.about': 'About',
    'nav.search.placeholder': 'Search AI Agents...',
    'hero.title': 'AgentPedia',
    'hero.subtitle': 'Global AI Agent Explorer',
    'hero.description': 'Discover, explore, and understand the world\'s best AI Agent projects',
    'hero.search.placeholder': 'Search for AI Agents you\'re interested in...',
    'featured.title': 'Featured AI Agents',
    'latest.title': 'Latest Releases',
    'agent.view.details': 'View Details',
    'category.all': 'All Categories',
    'category.development': 'Development Tools',
    'category.productivity': 'Productivity',
    'category.communication': 'Communication',
    'category.entertainment': 'Entertainment',
    'category.education': 'Education',
    'status.released': 'Released',
    'status.beta': 'Beta',
    'status.alpha': 'Alpha',
    'status.concept': 'Concept',
    'theme.toggle': 'Toggle Theme',
    'language.switch': 'Switch Language',
  },
}

export function IntlProvider({ children }: { children: React.ReactNode }) {
  const [locale, setLocaleState] = useState<Locale>('zh')

  useEffect(() => {
    // 从localStorage读取语言设置
    const savedLocale = localStorage.getItem('locale') as Locale | null
    if (savedLocale && ['zh', 'en'].includes(savedLocale)) {
      setLocaleState(savedLocale)
    } else {
      // 检测浏览器语言
      const browserLocale = navigator.language.toLowerCase()
      setLocaleState(browserLocale.startsWith('zh') ? 'zh' : 'en')
    }
  }, [])

  useEffect(() => {
    localStorage.setItem('locale', locale)
    document.documentElement.lang = locale
  }, [locale])

  const setLocale = (newLocale: Locale) => {
    setLocaleState(newLocale)
  }

  const t = (key: string, values?: Record<string, string | number>): string => {
    let text = translations[locale][key] || key

    if (values) {
      Object.entries(values).forEach(([placeholder, value]) => {
        text = text.replace(`{{${placeholder}}}`, String(value))
      })
    }

    return text
  }

  return (
    <IntlContext.Provider value={{ locale, setLocale, t }}>
      {children}
    </IntlContext.Provider>
  )
}

export const useIntl = () => {
  const context = useContext(IntlContext)
  if (context === undefined) {
    throw new Error('useIntl must be used within an IntlProvider')
  }
  return context
}