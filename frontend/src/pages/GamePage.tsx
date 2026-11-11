// uses react-router (open source)

import { useState } from 'react'
import { useNavigate, useParams } from 'react-router'
import Button from '../components/Button'
import EditRequest from '../components/EditRequest'
import GamePlayer from '../components/GamePlayer'
import SharePopup from '../components/SharePopup'
import { useCurrentGame } from '../game/useCurrentGame'

function GamePage() {
  const { id = '' } = useParams()
  const navigate = useNavigate()
  const [tab, setTab] = useState<'play' | 'edit'>('play')
  const [sharing, setSharing] = useState(false)
  const { game } = useCurrentGame()

  return (
    <>
      <h1>{game?.request.name || 'Untitled game'}</h1>

      <div role="tablist">
        <Button onClick={() => setTab('play')} aria-selected={tab === 'play'}>
          Play
        </Button>
        <Button onClick={() => setTab('edit')} aria-selected={tab === 'edit'}>
          Edit
        </Button>
      </div>
      {tab === 'play' ? <GamePlayer gameId={id} /> : <EditRequest gameId={id} />}

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
