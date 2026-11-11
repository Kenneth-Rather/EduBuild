// matches the backend writer's JSON output.

// Shape of a trivia game, matching the backend writer's output.

export interface TriviaQuestion {
  question: string
  choices: string[]
  answer: string // the correct choice's text
  source: string // lesson sentence that backs up the answer
}

export interface TriviaGameData {
  questions: TriviaQuestion[]
}
