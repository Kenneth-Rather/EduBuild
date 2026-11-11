// uses react-router (open source)

import { Link, useNavigate } from 'react-router'
import { login } from '../api/auth'
import { useAuth } from '../auth/useAuth'
import AuthForm from '../components/AuthForm'

function Login() {
  const { logIn } = useAuth()
  const navigate = useNavigate()

  async function handleSubmit(form: FormData) {
    await login(String(form.get('email')), String(form.get('password')))
    logIn()
    navigate('/dashboard')
  }

  return (
    <AuthForm
      title="Log in"
      submitLabel="Log in"
      onSubmit={handleSubmit}
      footer={
        <>
          No account? <Link to="/register">Register</Link>
        </>
      }
    >
      <label>
        Email
        <input name="email" type="email" autoComplete="email" required />
      </label>
      <label>
        Password
        <input
          name="password"
          type="password"
          autoComplete="current-password"
          required
        />
      </label>
    </AuthForm>
  )
}

export default Login
