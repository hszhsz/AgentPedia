import { Hero, FeaturedAgents, LatestAgents } from '@/components/sections'

export default function HomePage() {
  return (
    <div className="min-h-screen">
      <main>
        <Hero />
        <FeaturedAgents />
        <LatestAgents />
      </main>
    </div>
  )
}