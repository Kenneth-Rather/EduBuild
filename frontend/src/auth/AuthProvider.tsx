import { useState, type ReactNode } from 'react'
import { AuthContext } from './authContext'

const KEY = 'edubuild-logged-in'

function readFlag() {
  try {
    return localStorage.getItem(KEY) === 'true'
  } catch {
    return false
  }
}

function writeFlag(value: boolean) {
  try {
    if (value) localStorage.setItem(KEY, 'true')
    else localStorage.removeItem(KEY)
  } catch {
    // Storage unavailable: login just won't survive a refresh.
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isLoggedIn, setIsLoggedIn] = useState(readFlag)

  const logIn = () => {
    writeFlag(true)
    setIsLoggedIn(true)
  }
  const logOut = () => {
    writeFlag(false)
    setIsLoggedIn(false)
  }

  return (
    <AuthContext.Provider value={{ isLoggedIn, logIn, logOut }}>
      {children}
    </AuthContext.Provider>
  )
}
