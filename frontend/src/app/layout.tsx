import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { ThemeProvider } from '@/components/providers/theme-provider'
import { QueryProvider } from '@/components/providers/query-provider'
import { IntlProvider } from '@/components/providers/intl-provider'
import { Header, Footer } from '@/components/layout'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'AgentPedia - 全球AI Agent探索平台',
  description: '全球首个专注于AI Agent领域的信息聚合平台，为开发者、研究者、投资者提供全面的AI Agent生态信息查询服务',
  keywords: ['AI Agent', '人工智能', 'Agentpedia', 'AI工具', '智能体'],
  authors: [{ name: 'AgentPedia Team' }],
  openGraph: {
    title: 'AgentPedia - 全球AI Agent探索平台',
    description: '探索全球AI Agent生态，发现最新AI智能体项目',
    type: 'website',
    locale: 'zh_CN',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'AgentPedia',
    description: '全球AI Agent信息聚合平台',
  },
  robots: {
    index: true,
    follow: true,
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider>
          <QueryProvider>
            <IntlProvider>
              <div className="min-h-screen flex flex-col">
                <Header />
                <main className="flex-1">
                  {children}
                </main>
                <Footer />
              </div>
            </IntlProvider>
          </QueryProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}