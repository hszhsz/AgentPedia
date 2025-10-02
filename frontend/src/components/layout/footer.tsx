'use client'

import Link from 'next/link'
import { useIntl } from '@/components/providers/intl-provider'
import { Github, Twitter, Mail, Heart } from 'lucide-react'

export function Footer() {
  const { t } = useIntl()

  return (
    <footer className="border-t border-border dark:border-border-dark bg-background dark:bg-background-dark">
      <div className="container py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <div className="h-8 w-8 rounded-lg bg-accent dark:bg-accent-dark flex items-center justify-center">
                <span className="text-white font-bold text-lg">A</span>
              </div>
              <span className="font-bold text-xl text-text-primary dark:text-text-primary-dark">
                AgentPedia
              </span>
            </div>
            <p className="text-sm text-text-secondary dark:text-text-secondary-dark mb-4 max-w-md">
              {t('hero.description')}
            </p>
            <div className="flex items-center space-x-4">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-text-secondary dark:text-text-secondary-dark hover:text-accent dark:hover:text-accent-dark transition-colors"
              >
                <Github className="h-5 w-5" />
                <span className="sr-only">GitHub</span>
              </a>
              <a
                href="https://twitter.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-text-secondary dark:text-text-secondary-dark hover:text-accent dark:hover:text-accent-dark transition-colors"
              >
                <Twitter className="h-5 w-5" />
                <span className="sr-only">Twitter</span>
              </a>
              <a
                href="mailto:contact@agentpedia.com"
                className="text-text-secondary dark:text-text-secondary-dark hover:text-accent dark:hover:text-accent-dark transition-colors"
              >
                <Mail className="h-5 w-5" />
                <span className="sr-only">Email</span>
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-semibold text-text-primary dark:text-text-primary-dark mb-4">
              快速链接
            </h3>
            <ul className="space-y-2">
              <li>
                <Link
                  href="/"
                  className="text-sm text-text-secondary dark:text-text-secondary-dark hover:text-accent dark:hover:text-accent-dark transition-colors"
                >
                  {t('nav.home')}
                </Link>
              </li>
              <li>
                <Link
                  href="/agents"
                  className="text-sm text-text-secondary dark:text-text-secondary-dark hover:text-accent dark:hover:text-accent-dark transition-colors"
                >
                  {t('nav.agents')}
                </Link>
              </li>
              <li>
                <Link
                  href="/about"
                  className="text-sm text-text-secondary dark:text-text-secondary-dark hover:text-accent dark:hover:text-accent-dark transition-colors"
                >
                  {t('nav.about')}
                </Link>
              </li>
              <li>
                <Link
                  href="/submit"
                  className="text-sm text-text-secondary dark:text-text-secondary-dark hover:text-accent dark:hover:text-accent-dark transition-colors"
                >
                  提交 Agent
                </Link>
              </li>
            </ul>
          </div>

          {/* Categories */}
          <div>
            <h3 className="font-semibold text-text-primary dark:text-text-primary-dark mb-4">
              分类
            </h3>
            <ul className="space-y-2">
              <li>
                <Link
                  href="/agents?category=development"
                  className="text-sm text-text-secondary dark:text-text-secondary-dark hover:text-accent dark:hover:text-accent-dark transition-colors"
                >
                  {t('category.development')}
                </Link>
              </li>
              <li>
                <Link
                  href="/agents?category=productivity"
                  className="text-sm text-text-secondary dark:text-text-secondary-dark hover:text-accent dark:hover:text-accent-dark transition-colors"
                >
                  {t('category.productivity')}
                </Link>
              </li>
              <li>
                <Link
                  href="/agents?category=communication"
                  className="text-sm text-text-secondary dark:text-text-secondary-dark hover:text-accent dark:hover:text-accent-dark transition-colors"
                >
                  {t('category.communication')}
                </Link>
              </li>
              <li>
                <Link
                  href="/agents?category=education"
                  className="text-sm text-text-secondary dark:text-text-secondary-dark hover:text-accent dark:hover:text-accent-dark transition-colors"
                >
                  {t('category.education')}
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="border-t border-border dark:border-border-dark mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-sm text-text-secondary dark:text-text-secondary-dark">
              © 2024 AgentPedia. All rights reserved.
            </p>
            <div className="flex items-center space-x-4 mt-4 md:mt-0">
              <Link
                href="/privacy"
                className="text-sm text-text-secondary dark:text-text-secondary-dark hover:text-accent dark:hover:text-accent-dark transition-colors"
              >
                隐私政策
              </Link>
              <Link
                href="/terms"
                className="text-sm text-text-secondary dark:text-text-secondary-dark hover:text-accent dark:hover:text-accent-dark transition-colors"
              >
                服务条款
              </Link>
              <Link
                href="/contact"
                className="text-sm text-text-secondary dark:text-text-secondary-dark hover:text-accent dark:hover:text-accent-dark transition-colors"
              >
                联系我们
              </Link>
            </div>
          </div>
          <div className="flex items-center justify-center mt-4 text-sm text-text-secondary dark:text-text-secondary-dark">
            Made with <Heart className="h-4 w-4 mx-1 text-red-500" /> by the AgentPedia Team
          </div>
        </div>
      </div>
    </footer>
  )
}