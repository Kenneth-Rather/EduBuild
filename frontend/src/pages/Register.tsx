import { Link, useNavigate } from 'react-router'
import { register } from '../api/auth'
import { useAuth } from '../auth/useAuth'
import AuthForm from '../components/AuthForm'

function Register() {
  const { logIn } = useAuth()
  const navigate = useNavigate()

  async function handleSubmit(form: FormData) {
    await register(
      String(form.get('name')),
      String(form.get('email')),
      String(form.get('password')),
    )
    // New accounts are logged in straight away.
    logIn()
    navigate('/dashboard')
  }

  return (
    <AuthForm
      title="Register"
      submitLabel="Create account"
      onSubmit={handleSubmit}
      footer={
        <>
          Already have an account? <Link to="/login">Log in</Link>
        </>
      }
    >
      <label>
        Name
        <input name="name" autoComplete="name" required />
      </label>
      <label>
        Email
        {/* Any address is allowed, not only .edu. */}
        <input name="email" type="email" autoComplete="email" required />
      </label>
      <label>
        Password
        <input
          name="password"
          type="password"
          autoComplete="new-password"
          required
        />
      </label>
    </AuthForm>
  )
}

export default Register
