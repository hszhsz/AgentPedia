'use client'

import { useState } from 'react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { useIntl } from '@/components/providers/intl-provider'
import { useTheme } from '@/components/providers/theme-provider'
import { Search, Menu, X, Sun, Moon, Globe } from 'lucide-react'

export function Header() {
  const { t, locale, setLocale } = useIntl()
  const { theme, toggleTheme } = useTheme()
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen)

  const toggleLanguage = () => {
    setLocale(locale === 'zh' ? 'en' : 'zh')
  }

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border dark:border-border-dark bg-background/95 dark:bg-background-dark/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center space-x-2">
          <div className="h-8 w-8 rounded-lg bg-accent dark:bg-accent-dark flex items-center justify-center">
            <span className="text-white font-bold text-lg">A</span>
          </div>
          <span className="font-bold text-xl text-text-primary dark:text-text-primary-dark">
            AgentPedia
          </span>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center space-x-8">
          <Link
            href="/"
            className="text-sm font-medium text-text-primary dark:text-text-primary-dark hover:text-accent dark:hover:text-accent-dark transition-colors"
          >
            {t('nav.home')}
          </Link>
          <Link
            href="/agents"
            className="text-sm font-medium text-text-primary dark:text-text-primary-dark hover:text-accent dark:hover:text-accent-dark transition-colors"
          >
            {t('nav.agents')}
          </Link>
          <Link
            href="/about"
            className="text-sm font-medium text-text-primary dark:text-text-primary-dark hover:text-accent dark:hover:text-accent-dark transition-colors"
          >
            {t('nav.about')}
          </Link>
        </nav>

        {/* Search Bar - Desktop */}
        <div className="hidden md:flex flex-1 max-w-md mx-8">
          <div className="relative w-full">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-text-secondary dark:text-text-secondary-dark" />
            <Input
              type="text"
              placeholder={t('nav.search.placeholder')}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 bg-secondary dark:bg-secondary-dark border-border dark:border-border-dark"
            />
          </div>
        </div>

        {/* Right Side Actions */}
        <div className="flex items-center space-x-2">
          {/* Theme Toggle */}
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleTheme}
            className="hidden md:flex"
          >
            {theme === 'light' ? (
              <Moon className="h-5 w-5" />
            ) : (
              <Sun className="h-5 w-5" />
            )}
            <span className="sr-only">{t('theme.toggle')}</span>
          </Button>

          {/* Language Toggle */}
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleLanguage}
            className="hidden md:flex"
          >
            <Globe className="h-5 w-5" />
            <span className="sr-only">{t('language.switch')}</span>
          </Button>

          {/* Mobile Menu Toggle */}
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleMenu}
            className="md:hidden"
          >
            {isMenuOpen ? (
              <X className="h-5 w-5" />
            ) : (
              <Menu className="h-5 w-5" />
            )}
          </Button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden border-t border-border dark:border-border-dark bg-background dark:bg-background-dark">
          <div className="container px-4 py-4 space-y-4">
            {/* Mobile Navigation */}
            <nav className="flex flex-col space-y-3">
              <Link
                href="/"
                className="text-sm font-medium text-text-primary dark:text-text-primary-dark hover:text-accent dark:hover:text-accent-dark transition-colors"
                onClick={() => setIsMenuOpen(false)}
              >
                {t('nav.home')}
              </Link>
              <Link
                href="/agents"
                className="text-sm font-medium text-text-primary dark:text-text-primary-dark hover:text-accent dark:hover:text-accent-dark transition-colors"
                onClick={() => setIsMenuOpen(false)}
              >
                {t('nav.agents')}
              </Link>
              <Link
                href="/about"
                className="text-sm font-medium text-text-primary dark:text-text-primary-dark hover:text-accent dark:hover:text-accent-dark transition-colors"
                onClick={() => setIsMenuOpen(false)}
              >
                {t('nav.about')}
              </Link>
            </nav>

            {/* Mobile Search */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-text-secondary dark:text-text-secondary-dark" />
              <Input
                type="text"
                placeholder={t('nav.search.placeholder')}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 bg-secondary dark:bg-secondary-dark border-border dark:border-border-dark"
              />
            </div>

            {/* Mobile Actions */}
            <div className="flex items-center space-x-2 pt-2 border-t border-border dark:border-border-dark">
              <Button
                variant="ghost"
                size="sm"
                onClick={toggleTheme}
                className="flex items-center space-x-2"
              >
                {theme === 'light' ? (
                  <Moon className="h-4 w-4" />
                ) : (
                  <Sun className="h-4 w-4" />
                )}
                <span>{t('theme.toggle')}</span>
              </Button>

              <Button
                variant="ghost"
                size="sm"
                onClick={toggleLanguage}
                className="flex items-center space-x-2"
              >
                <Globe className="h-4 w-4" />
                <span>{t('language.switch')}</span>
              </Button>
            </div>
          </div>
        </div>
      )}
    </header>
  )
}