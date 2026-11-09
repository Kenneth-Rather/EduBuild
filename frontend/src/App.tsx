import { lazy, Suspense } from 'react'
import { BrowserRouter, Route, Routes } from 'react-router'
import { AuthProvider } from './auth/AuthProvider'
import RequireAuth from './auth/RequireAuth'
import Layout from './components/Layout'
import { CurrentGameProvider } from './game/CurrentGameProvider'
import GamePage from './pages/GamePage'
import Generating from './pages/Generating'
import Landing from './pages/Landing'
import Login from './pages/Login'
import MyGames from './pages/MyGames'
import NotFound from './pages/NotFound'
import Play from './pages/Play'
import Register from './pages/Register'
import './App.css'

// Loaded only when opened, so Uppy isn't downloaded on every other page.
const CreateGame = lazy(() => import('./pages/CreateGame'))

function App() {
  return (
    <AuthProvider>
      <CurrentGameProvider>
        <BrowserRouter>
          <Routes>
            {/* Student page sits outside Layout, so it has no navbar. */}
            <Route path="play/:id" element={<Play />} />

            <Route element={<Layout />}>
              <Route index element={<Landing />} />
              <Route path="login" element={<Login />} />
              <Route path="register" element={<Register />} />

              <Route element={<RequireAuth />}>
                <Route path="dashboard" element={<MyGames />} />
                <Route
                  path="create"
                  element={
                    <Suspense fallback={<p>Loading...</p>}>
                      <CreateGame />
                    </Suspense>
                  }
                />
                <Route path="games/:id/generating" element={<Generating />} />
                <Route path="games/:id" element={<GamePage />} />
              </Route>

              <Route path="*" element={<NotFound />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </CurrentGameProvider>
    </AuthProvider>
  )
}

export default App
