import React from 'react'
import { GlassCard } from './glass-card'
import { cn } from '@/lib/utils'

interface MetricCardProps {
  title: string
  value: string | number
  subtitle?: string
  icon?: React.ReactNode
  trend?: {
    value: number
    direction: 'up' | 'down' | 'neutral'
  }
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  icon,
  trend,
  size = 'md',
  className,
}) => {
  const sizeClasses = {
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  }

  const valueSizeClasses = {
    sm: 'text-2xl',
    md: 'text-3xl',
    lg: 'text-4xl',
  }

  const titleSizeClasses = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base',
  }

  const getTrendIcon = (direction: 'up' | 'down' | 'neutral') => {
    switch (direction) {
      case 'up':
        return '↗'
      case 'down':
        return '↘'
      default:
        return '→'
    }
  }

  const getTrendColor = (direction: 'up' | 'down' | 'neutral') => {
    switch (direction) {
      case 'up':
        return 'text-green-400'
      case 'down':
        return 'text-red-400'
      default:
        return 'text-gray-400'
    }
  }

  return (
    <GlassCard className={cn(sizeClasses[size], className)}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className={cn(
            'text-white/60 font-medium mb-1',
            titleSizeClasses[size]
          )}>
            {title}
          </div>
          <div className={cn(
            'text-white font-bold mb-1',
            valueSizeClasses[size]
          )}>
            {value}
          </div>
          {subtitle && (
            <div className="text-white/60 text-sm">
              {subtitle}
            </div>
          )}
          {trend && (
            <div className={cn(
              'flex items-center mt-2 text-sm font-medium',
              getTrendColor(trend.direction)
            )}>
              <span className="mr-1">
                {getTrendIcon(trend.direction)}
              </span>
              <span>
                {Math.abs(trend.value)}%
              </span>
            </div>
          )}
        </div>
        {icon && (
          <div className="ml-4 text-white/40">
            {icon}
          </div>
        )}
      </div>
    </GlassCard>
  )
}

export { MetricCard }