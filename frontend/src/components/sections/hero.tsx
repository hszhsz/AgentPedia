'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { useIntl } from '@/components/providers/intl-provider'
import { Search, ArrowRight, Sparkles, TrendingUp } from 'lucide-react'

export function Hero() {
  const { t } = useIntl()
  const [searchQuery, setSearchQuery] = useState('')

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      // Navigate to search results
      window.location.href = `/agents?q=${encodeURIComponent(searchQuery.trim())}`
    }
  }

  const popularSearches = [
    'ChatGPT', 'Claude', 'GitHub Copilot', 'Midjourney', 'Perplexity'
  ]

  const stats = [
    { label: 'AI Agents', value: '1,200+' },
    { label: 'Categories', value: '25+' },
    { label: 'Users', value: '50K+' },
    { label: 'Updates', value: 'Daily' }
  ]

  return (
    <section className="relative overflow-hidden bg-gradient-to-br from-surface dark:from-surface-dark to-secondary dark:to-secondary-dark">
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg%20width%3D%2260%22%20height%3D%2260%22%20viewBox%3D%220%200%2060%2060%22%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%3E%3Cg%20fill%3D%22none%22%20fill-rule%3D%22evenodd%22%3E%3Cg%20fill%3D%22%23000000%22%20fill-opacity%3D%220.03%22%3E%3Ccircle%20cx%3D%227%22%20cy%3D%227%22%20r%3D%227%22/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')] opacity-50" />

      <div className="container relative py-20 lg:py-32">
        <div className="max-w-4xl mx-auto text-center">
          {/* Top Badge */}
          <div className="flex justify-center mb-6">
            <Badge variant="secondary" className="flex items-center space-x-2">
              <Sparkles className="h-4 w-4" />
              <span>探索 AI Agent 的无限可能</span>
            </Badge>
          </div>

          {/* Main Title */}
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-text-primary dark:text-text-primary-dark mb-6">
            {t('hero.title')}
            <span className="block text-accent dark:text-accent-dark">
              {t('hero.subtitle')}
            </span>
          </h1>

          {/* Description */}
          <p className="text-xl md:text-2xl text-text-secondary dark:text-text-secondary-dark mb-8 max-w-3xl mx-auto leading-relaxed">
            {t('hero.description')}
          </p>

          {/* Search Bar */}
          <form onSubmit={handleSearch} className="max-w-2xl mx-auto mb-8">
            <div className="relative group">
              <div className="absolute -inset-1 bg-gradient-to-r from-accent dark:from-accent-dark to-accent/50 dark:to-accent-dark/50 rounded-lg blur opacity-25 group-hover:opacity-30 transition duration-200"></div>
              <div className="relative flex items-center">
                <Input
                  type="text"
                  placeholder={t('hero.search.placeholder')}
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="h-14 px-6 pr-32 text-base bg-white dark:bg-gray-800 border-border dark:border-border-dark shadow-lg focus:ring-2 focus:ring-accent dark:focus:ring-accent-dark"
                />
                <Button
                  type="submit"
                  size="lg"
                  className="absolute right-2 h-10 px-6 bg-accent dark:bg-accent-dark hover:bg-opacity-90 text-white rounded-md"
                >
                  <Search className="h-5 w-5 mr-2" />
                  搜索
                </Button>
              </div>
            </div>
          </form>

          {/* Popular Searches */}
          <div className="mb-12">
            <p className="text-sm text-text-secondary dark:text-text-secondary-dark mb-3">
              热门搜索:
            </p>
            <div className="flex flex-wrap justify-center gap-2">
              {popularSearches.map((term) => (
                <button
                  key={term}
                  onClick={() => setSearchQuery(term)}
                  className="px-3 py-1 text-sm bg-secondary dark:bg-secondary-dark hover:bg-accent dark:hover:bg-accent-dark hover:text-white rounded-full transition-colors duration-200"
                >
                  {term}
                </button>
              ))}
            </div>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-4 mb-16">
            <Button
              size="lg"
              className="bg-accent dark:bg-accent-dark hover:bg-opacity-90 text-white px-8 py-4 text-lg h-14"
              onClick={() => window.location.href = '/agents'}
            >
              探索 AI Agents
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
            <Button
              variant="outline"
              size="lg"
              className="border-border dark:border-border-dark hover:bg-accent dark:hover:bg-accent-dark hover:text-white px-8 py-4 text-lg h-14"
              onClick={() => window.location.href = '/submit'}
            >
              提交您的 Agent
            </Button>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-3xl mx-auto">
            {stats.map((stat) => (
              <div key={stat.label} className="text-center">
                <div className="text-3xl md:text-4xl font-bold text-accent dark:text-accent-dark mb-2">
                  {stat.value}
                </div>
                <div className="text-sm text-text-secondary dark:text-text-secondary-dark">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom Gradient */}
      <div className="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-background dark:from-background-dark to-transparent" />
    </section>
  )
}