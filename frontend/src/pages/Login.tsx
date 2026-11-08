import { Link, useNavigate } from 'react-router'
import { useAuth } from '../auth/useAuth'
import Button from '../components/Button'

function Login() {
  const { logIn } = useAuth()
  const navigate = useNavigate()

  return (
    <>
      <h1>Log in</h1>
      <Button
        onClick={() => {
          logIn()
          navigate('/dashboard')
        }}
      >
        Log in
      </Button>
      <p>
        No account? <Link to="/register">Register</Link>
      </p>
    </>
  )
}

export default Login
