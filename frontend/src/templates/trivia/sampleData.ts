// sample questions copied from the backend's fake AI answers (llm.py)

import type { TriviaGameData } from '../../types/trivia'

// Hardcoded sample for the prototype: the writer's fake output on the
// orchestrator branch (backend/pipeline/llm.py).
export const SAMPLE_TRIVIA_TITLE = 'The Water Cycle'

export const SAMPLE_TRIVIA: TriviaGameData = {
  questions: [
    {
      question: 'What does water turn into when it freezes?',
      choices: ['Ice', 'Steam', 'Sand'],
      answer: 'Ice',
      source: 'When water gets very cold, it freezes into ice.',
    },
    {
      question: 'What does water turn into when it boils?',
      choices: ['Ice', 'Steam', 'Mud'],
      answer: 'Steam',
      source: 'When water gets very hot, it boils and turns into steam.',
    },
  ],
}
