import { Link, Navigate } from 'react-router'
import { useAuth } from '../auth/useAuth'

function Landing() {
  const { isLoggedIn } = useAuth()
  if (isLoggedIn) return <Navigate to="/dashboard" replace />

  return (
    <>
      <h1>EduBuild</h1>
      <p>Your all-in-one student engagement tool</p>
      <Link to="/login">Get Started</Link>
    </>
  )
}

export default Landing
