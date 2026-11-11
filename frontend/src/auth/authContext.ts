// React context
import { createContext } from 'react'

// Placeholder auth: a flag in localStorage until the backend has real login.
export type Auth = {
  isLoggedIn: boolean
  logIn: () => void
  logOut: () => void
}

export const AuthContext = createContext<Auth | null>(null)
