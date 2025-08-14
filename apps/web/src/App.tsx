import { Navigate, Route, Routes } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Register from './pages/Register';
import ProjectsList from './pages/ProjectsList';
import ProjectForm from './pages/ProjectForm';
import ProjectDetails from './pages/ProjectDetails';

function App() {
  const token = localStorage.getItem('token') || '';
  const role = localStorage.getItem('role') || '';
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/projects" element={<ProjectsList token={token} role={role} />} />
      <Route path="/projects/new" element={<ProjectForm token={token} />} />
      <Route path="/projects/:id" element={<ProjectDetails token={token} />} />
      <Route path="/projects/:id/edit" element={<ProjectForm token={token} editing />} />
      <Route path="*" element={<Navigate to="/login" />} />
    </Routes>
  );
}

export default App;
