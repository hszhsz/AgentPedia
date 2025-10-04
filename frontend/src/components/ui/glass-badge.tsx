import React from 'react'
import { cn } from '@/lib/utils'

interface GlassBadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'primary' | 'secondary' | 'success' | 'warning' | 'error'
  size?: 'sm' | 'md' | 'lg'
  glow?: boolean
}

const GlassBadge = React.forwardRef<HTMLDivElement, GlassBadgeProps>(
  ({ className, variant = 'default', size = 'md', glow = false, ...props }, ref) => {
    const baseClasses = [
      'inline-flex',
      'items-center',
      'justify-center',
      'rounded-lg',
      'font-medium',
      'backdrop-blur-sm',
      'border',
      'transition-all',
      'duration-200',
    ]

    const variantClasses = {
      default: [
        'bg-white/10',
        'border-white/20',
        'text-white',
      ],
      primary: [
        'bg-blue-500/20',
        'border-blue-400/30',
        'text-blue-100',
      ],
      secondary: [
        'bg-gray-500/20',
        'border-gray-400/30',
        'text-gray-100',
      ],
      success: [
        'bg-green-500/20',
        'border-green-400/30',
        'text-green-100',
      ],
      warning: [
        'bg-yellow-500/20',
        'border-yellow-400/30',
        'text-yellow-100',
      ],
      error: [
        'bg-red-500/20',
        'border-red-400/30',
        'text-red-100',
      ],
    }

    const sizeClasses = {
      sm: ['px-2', 'py-0.5', 'text-xs'],
      md: ['px-3', 'py-1', 'text-sm'],
      lg: ['px-4', 'py-1.5', 'text-base'],
    }

    const glowClasses = glow ? [
      'shadow-md',
      'shadow-white/10',
    ] : []

    const classes = cn(
      ...baseClasses,
      ...variantClasses[variant],
      ...sizeClasses[size],
      ...glowClasses,
      className
    )

    return (
      <div
        ref={ref}
        className={classes}
        {...props}
      />
    )
  }
)

GlassBadge.displayName = 'GlassBadge'

export { GlassBadge }