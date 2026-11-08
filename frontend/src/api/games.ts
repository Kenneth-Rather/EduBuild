// Calls to the backend's game endpoints.

export const GENRES = ['Trivia'] as const
export const GRADES = ['K', '1', '2', '3', '4', '5', '6'] as const
export const DIFFICULTIES = ['Easy', 'Medium', 'Hard'] as const

export type NewGame = {
  genre: (typeof GENRES)[number]
  grade: (typeof GRADES)[number]
  difficulty: (typeof DIFFICULTIES)[number]
  topic: string
  files: File[]
}

// Starts generating a game and returns its ID.
// TODO: the backend has no game endpoints yet; this pretends game 1 was made.
export async function createGame(game: NewGame): Promise<string> {
  void game
  return '1'
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
