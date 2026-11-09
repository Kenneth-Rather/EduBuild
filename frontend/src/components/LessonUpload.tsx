import type Uppy from '@uppy/core'
import Dashboard from '@uppy/react/dashboard'
import '@uppy/core/css/style.min.css'
import '@uppy/dashboard/css/style.min.css'
import { MAX_FILE_SIZE_MB, MAX_FILES } from './lessonUppy'

function LessonUpload({ uppy }: { uppy: Uppy }) {
  return (
    <div className="lesson-upload">
      <Dashboard
        uppy={uppy}
        hideUploadButton
        proudlyDisplayPoweredByUppy={false}
        theme="light"
        width="100%"
        height={220}
      />
      {/* Uppy hides its own note on short dashboards, so show it here. */}
      <p className="upload-note">
        Text files (.txt) only ·{' '}
        {MAX_FILES === 1 ? 'one file' : `up to ${MAX_FILES} files`}, up to{' '}
        {MAX_FILE_SIZE_MB} MB
      </p>
    </div>
  )
}

export default LessonUpload
