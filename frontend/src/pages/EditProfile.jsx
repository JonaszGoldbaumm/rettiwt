import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { apiFetch } from '../services/api';

const ProfileEdit = () => {
  const { token, user } = useAuth();
  const navigate = useNavigate();

  const [username, setUsername] = useState('');
  const [description, setDescription] = useState('');
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePatch = async (endpoint, body, isFormData = false) => {
    try {
      await apiFetch(endpoint, {
        method: 'PATCH',
        body: isFormData ? body : JSON.stringify(body)
      }, token);
      alert('Update successful');
      if (endpoint.includes('profile-pic')) setFile(null);
    } catch (err) {
      alert(err.message);
    }
  };

  const handleUsername = (e) => { e.preventDefault(); handlePatch('/profile/me/username', { new_username: username }); };
  const handleDescription = (e) => { e.preventDefault(); handlePatch('/profile/me/description', { description }); };
  const handlePassword = (e) => { e.preventDefault(); handlePatch('/profile/me/password', { old_password: oldPassword, new_password: newPassword }); };
  const handleProfilePic = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    if (file) formData.append('pic', file);
    await handlePatch('/profile/me/profile-pic', formData, true);
  };

  return (
    <div className="d-flex justify-content-center mt-5 px-2">
      <div className="card p-4 shadow w-100" style={{ maxWidth: '500px' }}>
      <h3>Edit Profile</h3>

      {/* Profile Picture */}
      <div className="card p-3 mb-3">
        <form onSubmit={handleProfilePic}>
          <label className="form-label">Profile Picture</label>
          <input 
            type="file" 
            className="form-control mb-2" 
            accept="image/*"
            onChange={e => setFile(e.target.files[0])} 
          />
          <button className="btn btn-primary" type="submit">Update Picture</button>
        </form>
      </div>

      {/* Username */}
      <div className="card p-3 mb-3">
        <form onSubmit={handleUsername}>
          <label className="form-label">Username</label>
          <input 
            type="text" 
            className="form-control mb-2" 
            placeholder={user.username}
            value={username} 
            onChange={e => setUsername(e.target.value)} 
          />
          <button className="btn btn-primary" type="submit">Change Username</button>
        </form>
      </div>

      {/* Description */}
      <div className="card p-3 mb-3">
        <form onSubmit={handleDescription}>
          <label className="form-label">Description</label>
          <textarea 
            className="form-control mb-2" 
            placeholder="Write something about yourself..." 
            value={description} 
            onChange={e => setDescription(e.target.value)}
          />
          <button className="btn btn-primary" type="submit">Change Description</button>
        </form>
      </div>

      {/* Password */}
      <div className="card p-3 mb-3">
        <form onSubmit={handlePassword}>
          <label className="form-label">Old Password</label>
          <input 
            type="password" 
            className="form-control mb-2" 
            value={oldPassword} 
            onChange={e => setOldPassword(e.target.value)} 
          />
          <label className="form-label">New Password</label>
          <input 
            type="password" 
            className="form-control mb-2" 
            value={newPassword} 
            onChange={e => setNewPassword(e.target.value)} 
          />
          <button className="btn btn-primary" type="submit">Change Password</button>
        </form>
      </div>
        </div>
    </div>
  );
};

export default ProfileEdit;
