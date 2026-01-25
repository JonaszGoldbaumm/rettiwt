import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import PostDetail from './pages/PostDetail';
import Profile from './pages/Profile';

const Navbar = () => {
  const { isAuthenticated, logout } = useAuth();
  return (
    <nav style={{ padding: '1rem', borderBottom: '1px solid #eee', display: 'flex', gap: '10px' }}>
      <Link to="/">Home</Link>
      {isAuthenticated ? (
        <>
          <Link to="/profile/me">Profile</Link>
          <button onClick={logout}>Logout</button>
        </>
      ) : (
        <>
          <Link to="/login">Login</Link>
          <Link to="/register">Register</Link>
        </>
      )}
    </nav>
  );
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <main style={{ maxWidth: '600px', margin: '0 auto' }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/post/:postId" element={<PostDetail />} />
            <Route path="/profile/:userId" element={<Profile />} />
          </Routes>
        </main>
      </Router>
    </AuthProvider>
  );
}

export default App;