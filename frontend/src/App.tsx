import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom"

import DashboardLayout from "./layouts/DashboardLayout"

import JobsPage from "./pages/JobsPage"
import WorkersPage from "./pages/WorkersPage"
import JobDetailsPage from "./pages/JobDetailsPage"

function App() {

  return (
    <BrowserRouter>

      <DashboardLayout>

        <Routes>

          <Route
            path="/"
            element={<JobsPage />}
          />

          <Route
            path="/workers"
            element={<WorkersPage />}
          />

          <Route
            path="/jobs/:jobId"
            element={<JobDetailsPage />}
          />

        </Routes>

      </DashboardLayout>

    </BrowserRouter>
  )
}

export default App