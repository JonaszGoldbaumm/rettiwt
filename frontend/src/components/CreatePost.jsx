import { useState } from 'react';
import { useAuth } from '../context/AuthContext';

const CreatePost = ({ onPostCreated }) => {
  const { token, isAuthenticated } = useAuth();
  const [text, setText] = useState('');
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);

  if (!isAuthenticated) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData();
    formData.append('text', text);
    if (file) formData.append('media', file);

    try {
      const res = await fetch('http://localhost:8080/post/', {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
        body: formData,
      });

      if (!res.ok) throw new Error('Post failed');

      setText('');
      setFile(null);
      setPreview(null);
      onPostCreated?.();
    } catch (err) {
      alert(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card p-3 mb-4 shadow-sm w-100 w-md-75 w-lg-50 mx-auto">
      <form onSubmit={handleSubmit}>
        <textarea
          className="form-control mb-2"
          placeholder="What's on your mind?"
          value={text}
          onChange={e => setText(e.target.value)}
          required
        />
        {preview && <img src={preview} className="img-fluid rounded mb-2" alt="Preview" />}
        <div className="d-flex justify-content-between align-items-center">
          <input
            type="file"
            accept="image/*"
            className="form-control form-control-sm w-50"
            onChange={e => {
              const f = e.target.files[0];
              setFile(f);
              setPreview(URL.createObjectURL(f));
            }}
          />
          <button className="btn btn-primary" disabled={loading || !text.trim()}>
            {loading ? 'Posting...' : 'Post'}
          </button>
        </div>
      </form>
    </div>

  );
};

export default CreatePost;
