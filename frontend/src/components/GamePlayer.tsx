import TriviaGame from '../templates/trivia/TriviaGame'
import {
  SAMPLE_TRIVIA,
  SAMPLE_TRIVIA_TITLE,
} from '../templates/trivia/sampleData'

// Shared by the Game page's Play tab and the student Play page.
// Will load the game's data and pick the template for its genre.
// Prototype: every game shows the sample trivia game.
function GamePlayer({ gameId }: { gameId: string }) {
  void gameId
  return <TriviaGame title={SAMPLE_TRIVIA_TITLE} data={SAMPLE_TRIVIA} />
}

export default GamePlayer
