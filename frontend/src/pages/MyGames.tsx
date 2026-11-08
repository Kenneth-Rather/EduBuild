import { Link } from 'react-router'

function MyGames() {
  return (
    <>
      <h1>My Games</h1>
      <Link to="/create">Create New Game</Link>
      <ul>
        <li>
          <Link to="/games/1">Example game</Link>
        </li>
      </ul>
    </>
  )
}

export default MyGames
