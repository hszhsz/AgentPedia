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
    'about.title': '关于 AgentPedia',
    'about.mission.title': '我们的使命',
    'about.mission.description': 'AgentPedia 致力于成为全球最全面的 AI Agent 信息聚合平台，为开发者、研究者和用户提供一个探索、了解和发现 AI Agent 生态系统的中心枢纽。',
    'about.vision.title': '我们的愿景',
    'about.vision.description': '我们希望通过整合全球 AI Agent 资源，推动人工智能技术的发展，让每个人都能轻松了解和使用最新的 AI 智能体技术。',
    'about.features.title': '核心功能',
    'about.features.comprehensive.title': '全面的信息库',
    'about.features.comprehensive.description': '收录全球范围内的 AI Agent 项目，提供详细的项目信息和特性介绍。',
    'about.features.realtime.title': '实时更新',
    'about.features.realtime.description': '持续追踪最新的 AI Agent 发展动态，确保信息的时效性和准确性。',
    'about.features.open.title': '开放平台',
    'about.features.open.description': '支持社区贡献和项目提交，共同构建开放的 AI Agent 生态系统。',
    'about.features.community.title': '社区驱动',
    'about.features.community.description': '依靠社区力量维护和更新信息，确保内容质量和多样性。',
    'about.team.title': '关于团队',
    'about.team.description': '我们是一群热爱 AI 技术的开发者和研究者，致力于推动 AI Agent 技术的发展和普及。',
    'about.contact.title': '联系我们',
    'about.contact.description': '如果您有任何问题、建议或合作意向，欢迎随时与我们联系。',
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
    'about.title': 'About AgentPedia',
    'about.mission.title': 'Our Mission',
    'about.mission.description': 'AgentPedia is dedicated to becoming the most comprehensive AI Agent information aggregation platform globally, providing a central hub for developers, researchers, and users to explore, understand, and discover the AI Agent ecosystem.',
    'about.vision.title': 'Our Vision',
    'about.vision.description': 'We hope to promote the development of artificial intelligence technology by integrating global AI Agent resources, enabling everyone to easily understand and use the latest AI intelligent agent technologies.',
    'about.features.title': 'Core Features',
    'about.features.comprehensive.title': 'Comprehensive Database',
    'about.features.comprehensive.description': 'Collect AI Agent projects from around the world, providing detailed project information and feature introductions.',
    'about.features.realtime.title': 'Real-time Updates',
    'about.features.realtime.description': 'Continuously track the latest AI Agent developments to ensure information timeliness and accuracy.',
    'about.features.open.title': 'Open Platform',
    'about.features.open.description': 'Support community contributions and project submissions to jointly build an open AI Agent ecosystem.',
    'about.features.community.title': 'Community-driven',
    'about.features.community.description': 'Rely on community power to maintain and update information, ensuring content quality and diversity.',
    'about.team.title': 'About Our Team',
    'about.team.description': 'We are a group of developers and researchers who love AI technology, dedicated to promoting the development and popularization of AI Agent technology.',
    'about.contact.title': 'Contact Us',
    'about.contact.description': 'If you have any questions, suggestions, or cooperation intentions, please feel free to contact us at any time.',
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