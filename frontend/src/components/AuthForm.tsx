import { useState, type FormEvent, type ReactNode } from 'react'
import { AuthError } from '../api/auth'
import Button from './Button'

type AuthFormProps = {
  title: string
  submitLabel: string
  // Runs on submit; throw an AuthError to show its message.
  onSubmit: (form: FormData) => Promise<void>
  children: ReactNode // the input fields
  footer: ReactNode // the link to the other page
}

// Shared shell for the Login and Register pages.
function AuthForm({ title, submitLabel, onSubmit, children, footer }: AuthFormProps) {
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      await onSubmit(new FormData(event.currentTarget))
    } catch (err) {
      setError(
        err instanceof AuthError
          ? err.message
          : 'Something went wrong. Please try again.',
      )
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form className="auth-form" onSubmit={handleSubmit}>
      <h1>{title}</h1>
      {children}
      {error && (
        <p className="form-error" role="alert">
          {error}
        </p>
      )}
      <Button type="submit" disabled={submitting}>
        {submitting ? 'Please wait...' : submitLabel}
      </Button>
      <p>{footer}</p>
    </form>
  )
}

export default AuthForm
