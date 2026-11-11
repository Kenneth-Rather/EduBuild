// uses react-router (open source)
import { Link, useNavigate } from 'react-router'
import { useAuth } from '../auth/useAuth'
import Button from './Button'

function Navbar() {
  const { isLoggedIn, logOut } = useAuth()
  const navigate = useNavigate()

  if (!isLoggedIn) {
    return (
      <nav>
        <Link to="/">EduBuild</Link>
        <Link to="/login">Log in</Link>
        <Link to="/register">Register</Link>
      </nav>
    )
  }

  return (
    <nav>
      <Link to="/dashboard">EduBuild</Link>
      <Link to="/dashboard">My Games</Link>
      <Link to="/create">Create Game</Link>
      <Button
        onClick={() => {
          logOut()
          navigate('/')
        }}
      >
        Log out
      </Button>
    </nav>
  )
}

export default Navbar
