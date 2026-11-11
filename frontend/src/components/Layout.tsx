// uses react-router (open source)

import { Outlet } from 'react-router'
import Navbar from './Navbar'

// Shared shell for every page: the navbar on top, the current page below.
function Layout() {
  return (
    <>
      <Navbar />
      <main>
        <Outlet />
      </main>
    </>
  )
}

export default Layout
