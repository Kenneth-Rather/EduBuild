// React context

import { useRef, useState, type ReactNode } from 'react'
import { GameApiError, generateQuestions, type NewGame } from '../api/games'
import { CurrentGameContext, type CurrentGame } from './currentGameContext'

export function CurrentGameProvider({ children }: { children: ReactNode }) {
  const [game, setGame] = useState<CurrentGame | null>(null)
  // Numbers each request so an older, slower reply can't overwrite a newer one.
  const latestRequest = useRef(0)

  async function run(request: NewGame) {
    const requestNumber = ++latestRequest.current
    setGame({ request, status: 'generating' })
    try {
      const data = await generateQuestions(request)
      if (requestNumber === latestRequest.current) {
        setGame({ request, status: 'done', data })
      }
    } catch (err) {
      if (requestNumber === latestRequest.current) {
        setGame({
          request,
          status: 'error',
          error:
            err instanceof GameApiError
              ? err.message
              : 'Something went wrong. Please try again.',
        })
      }
    }
  }

  const store = {
    game,
    startGeneration: (request: NewGame) => void run(request),
    retry: () => {
      if (game) void run(game.request)
    },
  }

  return (
    <CurrentGameContext.Provider value={store}>
      {children}
    </CurrentGameContext.Provider>
  )
}
