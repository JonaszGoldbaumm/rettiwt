import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import PostDetail from './pages/Post';
import ProfilePage from './pages/Profile';
import ProfileEdit from './pages/EditProfile';
import './bootstrap/css/bootstrap.min.css';
import './bootstrap/js/bootstrap.bundle.min.js';

const Navbar = () => {
  const { isAuthenticated, user, logout } = useAuth();

  return (
    <nav
      className="navbar navbar-dark shadow-sm"
      style={{ backgroundColor: '#0d6efd', position: 'sticky', top: 0, zIndex: 1000 }}
    >
      <div className="container-fluid d-flex justify-content-around" style={{width:'100vm'}}>
        <Link to="/" className="btn btn-outline-light">Home</Link>
        {isAuthenticated ? (
          <>
            <Link to={`/profile/${user?.id}`} className="btn btn-outline-light">Profile</Link>
            <button className="btn btn-outline-light" onClick={logout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" className="btn btn-outline-light">Login</Link>
            <Link to="/register" className="btn btn-outline-light">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default function App() {
  return (
    <AuthProvider>
  <Router>
    <Navbar />   {/* Navbar itself handles full width */}
    <div style={{ width: '100vw', display: 'flex', justifyContent: 'center' }}>
      <main style={{ width: '80vw', maxWidth: '1200px' }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/post/:postId" element={<PostDetail />} />
          <Route path="/profile/:userId" element={<ProfilePage />} />
          <Route path="/profile/edit" element={<ProfileEdit />} />
        </Routes>
      </main>
    </div>
  </Router>
</AuthProvider>
  );
}
