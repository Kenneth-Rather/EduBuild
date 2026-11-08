import { Link, useNavigate } from 'react-router'
import { useAuth } from '../auth/useAuth'
import Button from '../components/Button'

function Register() {
  const { logIn } = useAuth()
  const navigate = useNavigate()

  return (
    <>
      <h1>Register</h1>
      <Button
        onClick={() => {
          logIn()
          navigate('/dashboard')
        }}
      >
        Create account
      </Button>
      <p>
        Already have an account? <Link to="/login">Log in</Link>
      </p>
    </>
  )
}

export default Register
