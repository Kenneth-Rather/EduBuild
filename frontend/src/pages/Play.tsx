// uses react-router (open source)

import { useParams } from 'react-router'
import GamePlayer from '../components/GamePlayer'

// Student page: no navbar, no login.
function Play() {
  const { id = '' } = useParams()
  return <GamePlayer gameId={id} />
}

export default Play
