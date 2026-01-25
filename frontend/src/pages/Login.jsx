import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { apiFetch } from '../services/api';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [formData, setFormData] = useState({ username_or_email: '', password: '' });
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Assuming your backend returns { access_token: "..." }
      const data = await apiFetch('/login', {
        method: 'POST',
        body: JSON.stringify(formData),
      });
      login(data.access_token); 
      navigate('/');
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div className="auth-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Username or Email" required 
          onChange={e => setFormData({...formData, username_or_email: e.target.value})} />
        <input type="password" placeholder="Password" required 
          onChange={e => setFormData({...formData, password: e.target.value})} />
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;