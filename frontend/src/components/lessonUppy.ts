import Uppy from '@uppy/core'

// Lesson files teachers can upload, and how many / how big.
export const ALLOWED_FILE_TYPES = [
  // '.pdf',
  // '.doc',
  // '.docx',
  // '.ppt',
  // '.pptx',
  '.txt',
]
export const MAX_FILES = 1
export const MAX_FILE_SIZE_MB = 20

// Uppy only collects the files here; they're sent with the rest of the
// form when the teacher clicks Generate Game.
export function createLessonUppy() {
  return new Uppy({
    autoProceed: false,
    restrictions: {
      allowedFileTypes: ALLOWED_FILE_TYPES,
      maxNumberOfFiles: MAX_FILES,
      maxFileSize: MAX_FILE_SIZE_MB * 1024 * 1024,
    },
  })
}
