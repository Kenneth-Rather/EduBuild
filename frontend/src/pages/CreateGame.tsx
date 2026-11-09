import { useUppyState } from '@uppy/react'
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
import LessonUpload from '../components/LessonUpload'
import { createLessonUppy } from '../components/lessonUppy'

function CreateGame() {
  const navigate = useNavigate()
  const [genre, setGenre] = useState<NewGame['genre']>(GENRES[0])
  const [grade, setGrade] = useState<NewGame['grade']>(GRADES[0])
  const [difficulty, setDifficulty] = useState<NewGame['difficulty']>(
    DIFFICULTIES[0],
  )
  const [name, setName] = useState('')
  // One Uppy instance for the life of the page, so files survive re-renders.
  const [uppy] = useState(createLessonUppy)
  const uppyFiles = useUppyState(uppy, (state) => state.files)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  // Games are generated from the uploaded lesson file only, for now.
  const hasContent = Object.keys(uppyFiles).length > 0

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    if (!hasContent) return
    setError('')
    setSubmitting(true)
    // Uppy wraps each file; File objects are what gets sent to the backend.
    const files = uppy
      .getFiles()
      .map((file) => file.data)
      .filter((data): data is File => data instanceof File)
    try {
      const id = await createGame({
        genre,
        grade,
        difficulty,
        name: name.trim(),
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
          Game name
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="e.g. The Water Cycle"
          />
        </label>
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
        <p className="hint">Upload the lesson to build the game from.</p>
        <div className="upload-field">
          <span className="field-label">Course material</span>
          <LessonUpload uppy={uppy} />
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
