// From scratch

import { useCurrentGame } from '../game/useCurrentGame'
import TriviaGame from '../templates/trivia/TriviaGame'

// Shared by the Game page's Play tab and the student Play page.
// Picks the template for the game's genre (only trivia so far).
// Until the backend stores games, it shows the game generated in this tab,
// whatever the ID in the URL.
function GamePlayer({ gameId }: { gameId: string }) {
  void gameId
  const { game } = useCurrentGame()

  if (game?.status !== 'done' || !game.data) {
    return <p>Game not found.</p>
  }

  return (
    <TriviaGame
      title={game.request.name || 'Untitled game'}
      data={game.data}
    />
  )
}

export default GamePlayer
