import { Routes, Route } from 'react-router-dom'
import { HomePage } from '@/pages/home-page'
import { ResultsPage } from '@/pages/results-page'

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/results" element={<ResultsPage />} />
    </Routes>
  )
}

export default App
