import React from 'react'
import { cn } from '@/lib/utils'

interface MiniChartProps {
  data: number[]
  color?: 'blue' | 'purple' | 'green' | 'yellow' | 'red'
  size?: 'sm' | 'md' | 'lg'
  showGradient?: boolean
  className?: string
}

const MiniChart: React.FC<MiniChartProps> = ({
  data,
  color = 'blue',
  size = 'md',
  showGradient = true,
  className,
}) => {
  if (!data || data.length === 0) return null

  const sizeClasses = {
    sm: 'h-12 w-24',
    md: 'h-16 w-32',
    lg: 'h-20 w-40',
  }

  const colorClasses = {
    blue: 'stroke-blue-400',
    purple: 'stroke-purple-400',
    green: 'stroke-green-400',
    yellow: 'stroke-yellow-400',
    red: 'stroke-red-400',
  }

  const gradientId = `gradient-${color}`

  const minValue = Math.min(...data)
  const maxValue = Math.max(...data)
  const range = maxValue - minValue || 1

  const points = data.map((value, index) => {
    const x = (index / (data.length - 1)) * 100
    const y = 100 - ((value - minValue) / range) * 100
    return `${x},${y}`
  }).join(' ')

  const createPath = () => {
    if (data.length < 2) return ''

    let path = `M 0,${100 - ((data[0] - minValue) / range) * 100}`

    for (let i = 1; i < data.length; i++) {
      const x = (i / (data.length - 1)) * 100
      const y = 100 - ((data[i] - minValue) / range) * 100
      path += ` L ${x},${y}`
    }

    return path
  }

  const createAreaPath = () => {
    if (data.length < 2) return ''

    const path = createPath()
    return `${path} L 100,100 L 0,100 Z`
  }

  return (
    <div className={cn('relative', sizeClasses[size], className)}>
      <svg
        viewBox="0 0 100 100"
        preserveAspectRatio="none"
        className="w-full h-full"
      >
        {showGradient && (
          <defs>
            <linearGradient
              id={gradientId}
              x1="0%"
              y1="0%"
              x2="0%"
              y2="100%"
            >
              <stop
                offset="0%"
                className="stop-current opacity-30"
              />
              <stop
                offset="100%"
                className="stop-current opacity-0"
              />
            </linearGradient>
          </defs>
        )}

        {/* Area */}
        {showGradient && (
          <path
            d={createAreaPath()}
            fill={`url(#${gradientId})`}
            className={colorClasses[color]}
          />
        )}

        {/* Line */}
        <path
          d={createPath()}
          fill="none"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className={cn(colorClasses[color], 'drop-shadow-sm')}
        />

        {/* Points */}
        {data.map((value, index) => {
          const x = (index / (data.length - 1)) * 100
          const y = 100 - ((value - minValue) / range) * 100
          const isLast = index === data.length - 1
          const isFirst = index === 0

          return (
            <circle
              key={index}
              cx={x}
              cy={y}
              r={isLast || isFirst ? 3 : 1.5}
              className={cn(
                colorClasses[color],
                'fill-current',
                (isLast || isFirst) && 'drop-shadow-sm'
              )}
            />
          )
        })}
      </svg>
    </div>
  )
}

export { MiniChart }