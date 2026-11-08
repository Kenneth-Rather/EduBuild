import { useState, type FormEvent } from 'react'
import { useNavigate } from 'react-router'
import { requestGameEdit } from '../api/games'
import Button from './Button'

// Game page's Edit tab: the teacher describes the changes they want and
// the AI rebuilds the game with them.
function EditRequest({ gameId }: { gameId: string }) {
  const navigate = useNavigate()
  const [request, setRequest] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  const hasRequest = request.trim() !== ''

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    if (!hasRequest) return
    setError('')
    setSubmitting(true)
    try {
      await requestGameEdit(gameId, request.trim())
      navigate(`/games/${gameId}/generating`)
    } catch {
      setError("Couldn't send your changes. Please try again.")
      setSubmitting(false)
    }
  }

  return (
    <form className="edit-request" onSubmit={handleSubmit}>
      <label>
        What changes would you like to make to the game?
        <textarea
          value={request}
          onChange={(e) => setRequest(e.target.value)}
          rows={4}
          placeholder="e.g. Make question 2 easier, or change the answer choices for question 1"
        />
      </label>
      {error && (
        <p className="form-error" role="alert">
          {error}
        </p>
      )}
      <Button type="submit" disabled={!hasRequest || submitting}>
        {submitting ? 'Please wait...' : 'Apply changes'}
      </Button>
    </form>
  )
}

export default EditRequest
