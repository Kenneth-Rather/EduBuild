import { BrowserRouter, Route, Routes } from 'react-router'
import { AuthProvider } from './auth/AuthProvider'
import RequireAuth from './auth/RequireAuth'
import Layout from './components/Layout'
import CreateGame from './pages/CreateGame'
import GamePage from './pages/GamePage'
import Generating from './pages/Generating'
import Landing from './pages/Landing'
import Login from './pages/Login'
import MyGames from './pages/MyGames'
import NotFound from './pages/NotFound'
import Play from './pages/Play'
import Register from './pages/Register'
import './App.css'

function App() {
  return (
    <AuthProvider>
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
              <Route path="create" element={<CreateGame />} />
              <Route path="games/:id/generating" element={<Generating />} />
              <Route path="games/:id" element={<GamePage />} />
            </Route>

            <Route path="*" element={<NotFound />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App
