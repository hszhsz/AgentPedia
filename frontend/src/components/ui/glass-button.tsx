import React from 'react'
import { cn } from '@/lib/utils'

interface GlassButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'primary' | 'secondary' | 'ghost' | 'outline'
  size?: 'sm' | 'md' | 'lg' | 'xl'
  glow?: boolean
}

const GlassButton = React.forwardRef<HTMLButtonElement, GlassButtonProps>(
  ({ className, variant = 'default', size = 'md', glow = false, ...props }, ref) => {
    const baseClasses = [
      'relative',
      'inline-flex',
      'items-center',
      'justify-center',
      'rounded-xl',
      'font-medium',
      'transition-all',
      'duration-300',
      'ease-out',
      'backdrop-blur-md',
      'border',
      'overflow-hidden',
      'group',
    ]

    const variantClasses = {
      default: [
        'bg-white/10',
        'border-white/20',
        'text-white',
        'hover:bg-white/20',
        'hover:border-white/30',
        'active:bg-white/30',
      ],
      primary: [
        'bg-gradient-to-r',
        'from-blue-500/20',
        'to-purple-500/20',
        'border-blue-400/30',
        'text-white',
        'hover:from-blue-500/30',
        'hover:to-purple-500/30',
        'hover:border-blue-400/50',
        'active:from-blue-500/40',
        'active:to-purple-500/40',
      ],
      secondary: [
        'bg-white/15',
        'border-white/25',
        'text-gray-200',
        'hover:bg-white/25',
        'hover:border-white/35',
        'active:bg-white/35',
      ],
      ghost: [
        'bg-transparent',
        'border-transparent',
        'text-white/80',
        'hover:bg-white/10',
        'hover:border-white/20',
        'active:bg-white/20',
      ],
      outline: [
        'bg-transparent',
        'border-white/40',
        'text-white',
        'hover:bg-white/10',
        'hover:border-white/60',
        'active:bg-white/20',
      ],
    }

    const sizeClasses = {
      sm: ['px-3', 'py-1.5', 'text-sm'],
      md: ['px-4', 'py-2', 'text-base'],
      lg: ['px-6', 'py-3', 'text-lg'],
      xl: ['px-8', 'py-4', 'text-xl'],
    }

    const glowClasses = glow ? [
      'shadow-lg',
      'shadow-white/20',
      'hover:shadow-xl',
      'hover:shadow-white/30',
    ] : []

    const classes = cn(
      ...baseClasses,
      ...variantClasses[variant],
      ...sizeClasses[size],
      ...glowClasses,
      className
    )

    return (
      <button
        ref={ref}
        className={classes}
        {...props}
      />
    )
  }
)

GlassButton.displayName = 'GlassButton'

export { GlassButton }