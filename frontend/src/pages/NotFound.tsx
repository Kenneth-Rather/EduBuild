// uses react-router (open source)

import { Link } from 'react-router'

function NotFound() {
  return (
    <>
      <h1>Page not found</h1>
      <Link to="/">Back to home</Link>
    </>
  )
}

export default NotFound
