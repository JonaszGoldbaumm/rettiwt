import { useState } from 'react';
import { useAuth } from '../context/AuthContext';

const CreatePost = ({ onPostCreated }) => {
  const { token, isAuthenticated } = useAuth();
  const [text, setText] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  if (!isAuthenticated) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData();
    
    formData.append('text', text); 
    if (file) {
      formData.append('media', file);
    }

    try {
      const response = await fetch('http://localhost:8000/post/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      if (response.ok) {
        setText('');
        setFile(null);
        e.target.reset(); 
        
        if (onPostCreated) onPostCreated();
      } else {
        const err = await response.json();
        throw new Error(err.detail || 'Failed to create post');
      }
    } catch (err) {
      alert(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="create-post-box" style={styles.container}>
      <form onSubmit={handleSubmit}>
        <textarea 
          placeholder="What's on your mind?" 
          value={text} 
          required
          onChange={(e) => setText(e.target.value)}
          style={styles.textarea}
        />
        <div style={styles.actions}>
          <input 
            type="file" 
            accept="image/jpeg,image/png" 
            onChange={(e) => setFile(e.target.files[0])}
            style={styles.fileInput}
          />
          <button type="submit" disabled={loading || !text.trim()} style={styles.button}>
            {loading ? 'Sending...' : 'Post'}
          </button>
        </div>
      </form>
    </section>
  );
};

const styles = {
  container: {
    padding: '1rem',
    border: '1px solid #e1e8ed',
    borderRadius: '12px',
    backgroundColor: '#fff',
    marginBottom: '20px'
  },
  textarea: {
    width: '100%',
    border: 'none',
    resize: 'none',
    fontSize: '1.2rem',
    outline: 'none',
    minHeight: '60px',
    fontFamily: 'inherit'
  },
  actions: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: '10px',
    borderTop: '1px solid #f0f0f0',
    paddingTop: '10px'
  },
  button: {
    backgroundColor: '#1da1f2',
    color: 'white',
    border: 'none',
    padding: '8px 16px',
    borderRadius: '20px',
    fontWeight: 'bold',
    cursor: 'pointer'
  }
};

export default CreatePost;