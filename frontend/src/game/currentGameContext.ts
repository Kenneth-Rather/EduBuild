import { createContext } from 'react'
import type { NewGame } from '../api/games'
import type { TriviaGameData } from '../types/trivia'

// The game being generated or played in this browser tab. Lives only in
// memory until the backend has a database: refreshing the page loses it.
export type CurrentGame = {
  request: NewGame // what the teacher asked for, kept so Try again can resend it
  status: 'generating' | 'done' | 'error'
  data?: TriviaGameData // set when status is 'done'
  error?: string // set when status is 'error'
}

export type CurrentGameStore = {
  game: CurrentGame | null
  startGeneration: (request: NewGame) => void
  retry: () => void
}

export const CurrentGameContext = createContext<CurrentGameStore | null>(null)
