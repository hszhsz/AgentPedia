import React from 'react'
import { cn } from '@/lib/utils'

interface GlassProgressProps {
  value: number
  max?: number
  size?: 'sm' | 'md' | 'lg'
  variant?: 'default' | 'gradient' | 'glow'
  color?: 'blue' | 'purple' | 'green' | 'yellow' | 'red'
  showLabel?: boolean
  className?: string
}

const GlassProgress: React.FC<GlassProgressProps> = ({
  value,
  max = 100,
  size = 'md',
  variant = 'default',
  color = 'blue',
  showLabel = false,
  className,
}) => {
  const percentage = Math.min((value / max) * 100, 100)

  const sizeClasses = {
    sm: 'h-1',
    md: 'h-2',
    lg: 'h-3',
  }

  const colorClasses = {
    blue: 'from-blue-400 to-blue-600',
    purple: 'from-purple-400 to-purple-600',
    green: 'from-green-400 to-green-600',
    yellow: 'from-yellow-400 to-yellow-600',
    red: 'from-red-400 to-red-600',
  }

  const variantClasses = {
    default: 'bg-gradient-to-r',
    gradient: 'bg-gradient-to-r',
    glow: cn(
      'bg-gradient-to-r',
      'shadow-lg',
      'shadow-blue-500/50'
    ),
  }

  return (
    <div className={cn('relative', className)}>
      {showLabel && (
        <div className="text-white/80 text-sm font-medium mb-2">
          {percentage.toFixed(1)}%
        </div>
      )}
      <div
        className={cn(
          'w-full rounded-full bg-white/10 backdrop-blur-sm border border-white/20 overflow-hidden',
          sizeClasses[size]
        )}
      >
        <div
          className={cn(
            'h-full rounded-full transition-all duration-500 ease-out',
            variantClasses[variant],
            colorClasses[color]
          )}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  )
}

export { GlassProgress }