import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { apiFetch } from '../services/api';
import { useNavigate, Link } from 'react-router-dom';
import { useToast } from '../context/ToastContext';

const Login = () => {
  const [formData, setFormData] = useState({ username_or_email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();
  const { showToast } = useToast();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const data = await apiFetch('/login', {
        method: 'POST',
        body: JSON.stringify(formData),
      });
      login(data);
      navigate('/');
    } catch (err) {
      showToast(err.message, "danger");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="d-flex justify-content-center mt-5 px-2">
      <div className="card p-4 shadow w-100" style={{ maxWidth: '500px' }}>
        <h3 className="text-center mb-3">Welcome Back</h3>

        <form onSubmit={handleSubmit}>
          <div className="form-group mb-3">
            <input
              className="form-control"
              placeholder="Username or Email"
              required
              onChange={e => setFormData({ ...formData, username_or_email: e.target.value })}
            />
          </div>

          <div className="form-group mb-3">
            <input
              className="form-control"
              type="password"
              placeholder="Password"
              required
              onChange={e => setFormData({ ...formData, password: e.target.value })}
            />
          </div>

          <button className="btn btn-primary w-100" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <p className="text-center mt-3 mb-0">
          No account? <Link to="/register">Create one</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
