// Implemented from scratch: calls our Django /api/generate-game/ endpoint.

// Calls to the backend's game endpoints.

import type { TriviaGameData, TriviaQuestion } from '../types/trivia'
import { getStoredUsername } from './auth'
import { API_URL } from './client'

export const GENRES = ['Trivia'] as const
export const GRADES = ['K', '1', '2', '3', '4', '5', '6'] as const
export const DIFFICULTIES = ['Easy', 'Medium', 'Hard'] as const

export type NewGame = {
  genre: (typeof GENRES)[number]
  grade: (typeof GRADES)[number]
  difficulty: (typeof DIFFICULTIES)[number]
  name: string // shown as the game's title
  files: File[]
}

// Placeholder until the backend stores games and gives them real IDs.
export const PLACEHOLDER_GAME_ID = '1'

// Error with a message that's safe to show the teacher.
export class GameApiError extends Error {}

// Sends the lesson file and settings to the backend's AI pipeline and returns
// the generated questions. Takes a while: the backend only replies when done.
export async function generateQuestions(
  game: NewGame,
): Promise<TriviaGameData> {
  const file = game.files[0]
  if (!file) throw new GameApiError('Please upload a .txt lesson file.')

  const form = new FormData()
  form.append('file', file)
  form.append('grade', game.grade)
  form.append('difficulty', game.difficulty)
  form.append('name', game.name)
  form.append('username', getStoredUsername())

  let response: Response
  try {
    response = await fetch(`${API_URL}/api/generate-game/`, {
      method: 'POST',
      body: form,
    })
  } catch {
    throw new GameApiError("Couldn't reach the server. Please try again.")
  }

  // Success: { status: "success", questions }. Failure: { status: "error", message }.
  let body: { status?: string; questions?: unknown; message?: string }
  try {
    body = await response.json()
  } catch {
    throw new GameApiError('Something went wrong. Please try again.')
  }
  if (!response.ok || body.status !== 'success') {
    throw new GameApiError(
      body.message ?? 'Something went wrong. Please try again.',
    )
  }
  if (!Array.isArray(body.questions)) {
    throw new GameApiError('The server sent back an unexpected answer.')
  }
  return { questions: body.questions as TriviaQuestion[] }
}

// Asks the AI to change a game, in the teacher's own words.
// TODO: the backend has no edit endpoint yet; this pretends it worked.
export async function requestGameEdit(
  gameId: string,
  request: string,
): Promise<void> {
  void gameId
  void request
}
