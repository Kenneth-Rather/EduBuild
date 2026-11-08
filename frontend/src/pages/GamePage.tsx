import { useState } from 'react'
import { useNavigate, useParams } from 'react-router'
import Button from '../components/Button'
import GamePlayer from '../components/GamePlayer'
import SharePopup from '../components/SharePopup'

function GamePage() {
  const { id = '' } = useParams()
  const navigate = useNavigate()
  const [tab, setTab] = useState<'play' | 'edit'>('play')
  const [sharing, setSharing] = useState(false)

  return (
    <>
      <h1>Game {id}</h1>

      <div role="tablist">
        <Button onClick={() => setTab('play')} aria-selected={tab === 'play'}>
          Play
        </Button>
        <Button onClick={() => setTab('edit')} aria-selected={tab === 'edit'}>
          Edit
        </Button>
      </div>
      {tab === 'play' ? <GamePlayer gameId={id} /> : <p>[Edit questions]</p>}

      <Button onClick={() => navigate('/dashboard')}>Save</Button>
      <Button
        onClick={() => {
          if (confirm('Regenerate this game?')) {
            navigate(`/games/${id}/generating`)
          }
        }}
      >
        Regenerate
      </Button>
      <Button onClick={() => setSharing(true)}>Share</Button>

      {sharing && <SharePopup gameId={id} onClose={() => setSharing(false)} />}
    </>
  )
}

export default GamePage
