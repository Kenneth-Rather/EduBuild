// React hook

import { useContext } from 'react'
import { CurrentGameContext } from './currentGameContext'

export function useCurrentGame() {
  const store = useContext(CurrentGameContext)
  if (!store) {
    throw new Error('useCurrentGame must be used inside <CurrentGameProvider>')
  }
  return store
}
