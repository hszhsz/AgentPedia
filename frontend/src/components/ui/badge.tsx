import * as React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const badgeVariants = cva(
  'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
  {
    variants: {
      variant: {
        default:
          'border-transparent bg-accent dark:bg-accent-dark text-white hover:bg-opacity-80',
        secondary:
          'border-transparent bg-secondary dark:bg-secondary-dark text-text-primary dark:text-text-primary-dark hover:bg-opacity-80',
        destructive:
          'border-transparent bg-error dark:bg-error-dark text-white hover:bg-opacity-80',
        outline: 'text-foreground border-border dark:border-border-dark',
        success:
          'border-transparent bg-success dark:bg-success-dark text-white hover:bg-opacity-80',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  )
}

export { Badge, badgeVariants }