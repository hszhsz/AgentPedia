'use client'

import { AuthProvider } from '@/contexts/AuthContext'

export function AuthProviderClient({ children }: { children: React.ReactNode }) {
  return <AuthProvider>{children}</AuthProvider>
}