import { useState, type FormEvent } from 'react'
import { useNavigate } from 'react-router'
import {
  createGame,
  DIFFICULTIES,
  GENRES,
  GRADES,
  type NewGame,
} from '../api/games'
import Button from '../components/Button'

function CreateGame() {
  const navigate = useNavigate()
  const [genre, setGenre] = useState<NewGame['genre']>(GENRES[0])
  const [grade, setGrade] = useState<NewGame['grade']>(GRADES[0])
  const [difficulty, setDifficulty] = useState<NewGame['difficulty']>(
    DIFFICULTIES[0],
  )
  const [topic, setTopic] = useState('')
  // Filled by the Uppy uploader once it's added from the file-upload branch.
  const [files] = useState<File[]>([])
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  const hasContent = topic.trim() !== '' || files.length > 0

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    if (!hasContent) return
    setError('')
    setSubmitting(true)
    try {
      const id = await createGame({
        genre,
        grade,
        difficulty,
        topic: topic.trim(),
        files,
      })
      navigate(`/games/${id}/generating`)
    } catch {
      setError("Couldn't start generating your game. Please try again.")
      setSubmitting(false)
    }
  }

  return (
    <form className="page-form" onSubmit={handleSubmit}>
      <h1>Create Game</h1>

      <fieldset>
        <legend>1. Game settings</legend>
        <label>
          Genre
          <select
            value={genre}
            onChange={(e) => setGenre(e.target.value as NewGame['genre'])}
          >
            {GENRES.map((g) => (
              <option key={g}>{g}</option>
            ))}
          </select>
        </label>
        <label>
          Grade level
          <select
            value={grade}
            onChange={(e) => setGrade(e.target.value as NewGame['grade'])}
          >
            {GRADES.map((g) => (
              <option key={g} value={g}>
                {g === 'K' ? 'Kindergarten' : `Grade ${g}`}
              </option>
            ))}
          </select>
        </label>
        <label>
          Difficulty
          <select
            value={difficulty}
            onChange={(e) =>
              setDifficulty(e.target.value as NewGame['difficulty'])
            }
          >
            {DIFFICULTIES.map((d) => (
              <option key={d}>{d}</option>
            ))}
          </select>
        </label>
      </fieldset>

      <fieldset>
        <legend>2. Lesson content</legend>
        <p className="hint">Fill in either or both.</p>
        <label>
          Topic
          <textarea
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            rows={3}
            placeholder="e.g. The Solar System: the Sun, stars, planets, moons, and the rotation of the Earth"
          />
        </label>
        <div className="upload-slot">
          {/* Uppy uploader goes here (file-upload branch). */}
          Upload course material (coming soon)
        </div>
      </fieldset>

      {error && (
        <p className="form-error" role="alert">
          {error}
        </p>
      )}
      <Button type="submit" disabled={!hasContent || submitting}>
        {submitting ? 'Please wait...' : 'Generate Game'}
      </Button>
    </form>
  )
}

export default CreateGame
