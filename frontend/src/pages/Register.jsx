import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { apiFetch } from '../services/api';
import { useToast } from '../context/ToastContext';

const Register = () => {
  const [formData, setFormData] = useState({ username: '', email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { showToast } = useToast();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await apiFetch('/register', {
        method: 'POST',
        body: JSON.stringify(formData),
      });
      navigate('/login');
    } catch (err) {
      showToast(err.message, "danger");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="d-flex justify-content-center mt-5 px-2">
      <div className="card p-4 shadow w-100" style={{ maxWidth: '500px' }}>
        <h3 className="text-center mb-3">Create Account</h3>

        <form onSubmit={handleSubmit}>
          <div className="form-group mb-3">
            <input
              className="form-control"
              placeholder="Username"
              required
              onChange={e => setFormData({ ...formData, username: e.target.value })}
            />
          </div>

          <div className="form-group mb-3">
            <input
              className="form-control"
              type="email"
              placeholder="Email"
              required
              onChange={e => setFormData({ ...formData, email: e.target.value })}
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
            {loading ? 'Creating...' : 'Register'}
          </button>
        </form>

        <p className="text-center mt-3 mb-0">
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
