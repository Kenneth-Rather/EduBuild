// Shared by the Game page's Play tab and the student Play page.
// Will take a game's data and pick the right template (trivia for now).
function GamePlayer({ gameId }: { gameId: string }) {
  return <p>[GamePlayer for game {gameId}]</p>
}

export default GamePlayer
