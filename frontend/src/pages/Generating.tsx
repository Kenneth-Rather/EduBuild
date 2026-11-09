import { Link, Navigate, useParams } from 'react-router'
import Button from '../components/Button'
import { useCurrentGame } from '../game/useCurrentGame'

function Generating() {
  const { id } = useParams()
  const { game, retry } = useCurrentGame()

  if (!game) {
    return (
      <>
        <h1>No game in progress</h1>
        <Link to="/create">Create a game</Link>
      </>
    )
  }

  if (game.status === 'done') {
    return <Navigate to={`/games/${id}`} replace />
  }

  if (game.status === 'error') {
    return (
      <>
        <h1>Something went wrong</h1>
        <p className="form-error" role="alert">
          {game.error}
        </p>
        <Button onClick={retry}>Try again</Button>
        <Link to="/dashboard">Back to My Games</Link>
      </>
    )
  }

  return (
    <>
      <h1>Building your game...</h1>
      <p role="status">This can take a minute.</p>
    </>
  )
}

export default Generating
