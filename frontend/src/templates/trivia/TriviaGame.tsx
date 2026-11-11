// From scratch: our trivia game template

import { useState } from 'react'
import type { TriviaGameData } from '../../types/trivia'
import './TriviaGame.css'

type TriviaGameProps = {
  title: string
  data: TriviaGameData
}

// Barebone trivia template: the "mold" the AI fills with questions.
// Prototype only: shows each question and lets the player pick an answer.
function TriviaGame({ title, data }: TriviaGameProps) {
  // The choice picked for each question, by question index.
  const [picked, setPicked] = useState<Record<number, string>>({})

  return (
    <div className="trivia">
      <h1>{title}</h1>
      {data.questions.map((q, i) => (
        <section key={i} className="trivia-question">
          <h2>
            {i + 1}. {q.question}
          </h2>
          <div className="trivia-choices">
            {q.choices.map((choice) => (
              <button
                key={choice}
                type="button"
                className="trivia-choice"
                aria-pressed={picked[i] === choice}
                onClick={() => setPicked({ ...picked, [i]: choice })}
              >
                {choice}
              </button>
            ))}
          </div>
        </section>
      ))}
    </div>
  )
}

export default TriviaGame
