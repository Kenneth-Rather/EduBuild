import { useNavigate } from 'react-router'
import Button from '../components/Button'

function CreateGame() {
  const navigate = useNavigate()

  return (
    <>
      <h1>Create Game</h1>
      <h2>Game settings</h2>
      <h2>Lesson content</h2>
      {/* Placeholder ID until the backend creates the game. */}
      <Button onClick={() => navigate('/games/1/generating')}>
        Generate Game
      </Button>
    </>
  )
}

export default CreateGame
