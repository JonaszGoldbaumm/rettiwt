import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiFetch } from '../services/api';

const Register = () => {
  const [formData, setFormData] = useState({ username: '', email: '', password: '' });
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await apiFetch('/register', {
        method: 'POST',
        body: JSON.stringify(formData),
      });
      alert('Registration successful! Please login.');
      navigate('/login');
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div className="auth-container">
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Username" required 
          onChange={e => setFormData({...formData, username: e.target.value})} />
        <input type="email" placeholder="Email" required 
          onChange={e => setFormData({...formData, email: e.target.value})} />
        <input type="password" placeholder="Password" required 
          onChange={e => setFormData({...formData, password: e.target.value})} />
        <button type="submit">Join Rettiwt</button>
      </form>
    </div>
  );
};

export default Register;