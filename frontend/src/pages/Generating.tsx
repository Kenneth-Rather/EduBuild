import { Link, useParams } from 'react-router'

function Generating() {
  const { id } = useParams()

  return (
    <>
      <h1>Building your game...</h1>
      {/* Placeholder links standing in for the success and failure results. */}
      <Link to={`/games/${id}`}>Done (go to Game page)</Link>
      <p>On error:</p>
      <Link to={`/games/${id}/generating`} reloadDocument>
        Try again
      </Link>
      <Link to="/dashboard">Back to My Games</Link>
    </>
  )
}

export default Generating
