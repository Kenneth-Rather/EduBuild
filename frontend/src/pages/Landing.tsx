import { Link, Navigate } from 'react-router'
import { useAuth } from '../auth/useAuth'

function Landing() {
  const { isLoggedIn } = useAuth()
  if (isLoggedIn) return <Navigate to="/dashboard" replace />

  return (
    <>
      <h1>Landing</h1>
      <Link to="/login">Get Started</Link>
    </>
  )
}

export default Landing
