import { Navigate, Outlet } from 'react-router'
import { useAuth } from './useAuth'

// Wraps teacher-only routes: sends logged-out visitors to Login.
function RequireAuth() {
  const { isLoggedIn } = useAuth()
  return isLoggedIn ? <Outlet /> : <Navigate to="/login" replace />
}

export default RequireAuth
