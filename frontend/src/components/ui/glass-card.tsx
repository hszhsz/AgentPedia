import React from 'react'
import { cn } from '@/lib/utils'

interface GlassCardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'subtle' | 'strong'
  blur?: 'sm' | 'md' | 'lg' | 'xl'
}

const GlassCard = React.forwardRef<HTMLDivElement, GlassCardProps>(
  ({ className, variant = 'default', blur = 'md', ...props }, ref) => {
    const baseClasses = [
      'relative',
      'rounded-2xl',
      'border',
      'transition-all',
      'duration-300',
      'ease-out',
    ]

    const variantClasses = {
      default: [
        'bg-white/10',
        'border-white/20',
        'shadow-xl',
        'shadow-black/10',
        'backdrop-blur-md',
      ],
      subtle: [
        'bg-white/5',
        'border-white/10',
        'shadow-lg',
        'shadow-black/5',
        'backdrop-blur-sm',
      ],
      strong: [
        'bg-white/20',
        'border-white/30',
        'shadow-2xl',
        'shadow-black/20',
        'backdrop-blur-lg',
      ],
    }

    const blurClasses = {
      sm: 'backdrop-blur-sm',
      md: 'backdrop-blur-md',
      lg: 'backdrop-blur-lg',
      xl: 'backdrop-blur-xl',
    }

    const classes = cn(
      ...baseClasses,
      ...variantClasses[variant],
      blurClasses[blur],
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

GlassCard.displayName = 'GlassCard'

export { GlassCard }