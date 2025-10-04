import React from 'react'
import { MiniChart } from './mini-chart'
import { cn } from '@/lib/utils'

interface MetricSparklineProps {
  title: string
  current: number
  previous?: number
  data: number[]
  format?: 'number' | 'currency' | 'percentage'
  size?: 'sm' | 'md' | 'lg'
  color?: 'blue' | 'purple' | 'green' | 'yellow' | 'red'
  className?: string
}

const MetricSparkline: React.FC<MetricSparklineProps> = ({
  title,
  current,
  previous,
  data,
  format = 'number',
  size = 'md',
  color = 'blue',
  className,
}) => {
  const formatValue = (value: number) => {
    switch (format) {
      case 'currency':
        return new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: 'USD',
          minimumFractionDigits: 0,
          maximumFractionDigits: 0,
        }).format(value)
      case 'percentage':
        return `${value.toFixed(1)}%`
      default:
        return new Intl.NumberFormat('en-US', {
          notation: 'compact',
          maximumFractionDigits: 1,
        }).format(value)
    }
  }

  const trend = previous ? current - previous : 0
  const trendPercentage = previous ? (trend / previous) * 100 : 0

  const getTrendIcon = () => {
    if (trend > 0) return '↗'
    if (trend < 0) return '↘'
    return '→'
  }

  const getTrendColor = () => {
    if (trend > 0) return 'text-green-400'
    if (trend < 0) return 'text-red-400'
    return 'text-gray-400'
  }

  const sizeClasses = {
    sm: {
      container: 'p-3',
      title: 'text-xs',
      value: 'text-lg',
      trend: 'text-xs',
      chart: 'sm',
    },
    md: {
      container: 'p-4',
      title: 'text-sm',
      value: 'text-xl',
      trend: 'text-sm',
      chart: 'md',
    },
    lg: {
      container: 'p-5',
      title: 'text-base',
      value: 'text-2xl',
      trend: 'text-base',
      chart: 'lg',
    },
  }

  const classes = sizeClasses[size]

  return (
    <div
      className={cn(
        'bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-4',
        'hover:bg-white/15 transition-all duration-200',
        className
      )}
    >
      <div className="flex items-start justify-between mb-3">
        <div>
          <div className="text-white/60 font-medium mb-1">
            {title}
          </div>
          <div className="text-white font-bold mb-1">
            {formatValue(current)}
          </div>
          {previous && (
            <div className={cn(
              'flex items-center font-medium',
              getTrendColor()
            )}>
              <span className="mr-1">
                {getTrendIcon()}
              </span>
              <span>
                {Math.abs(trendPercentage).toFixed(1)}%
              </span>
            </div>
          )}
        </div>
      </div>
      <MiniChart
        data={data}
        color={color}
        size={classes.chart}
        showGradient
      />
    </div>
  )
}

export { MetricSparkline }