import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { apiFetch } from '../services/api';

const PostDetail = () => {
  const { postId } = useParams();
  const navigate = useNavigate();
  const { token, user } = useAuth();
  const [details, setDetails] = useState(null);
  const [commentText, setCommentText] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchDetails = async () => {
    try {
      const data = await apiFetch(`/post/${postId}`, {}, token);
      setDetails(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchDetails(); }, [postId]);

  const handleLike = async () => {
    try {
      await apiFetch(`/post/${postId}/like`, { method: 'POST' }, token);
      fetchDetails();
    } catch {
      alert("Action failed");
    }
  };

  const handleComment = async (e) => {
    e.preventDefault();
    try {
      await apiFetch(`/post/${postId}/comment`, {
        method: 'POST',
        body: JSON.stringify({ text: commentText })
      }, token);
      setCommentText('');
      fetchDetails();
    } catch {
      alert("Comment failed");
    }
  };

  const handleDeletePost = async () => {
    if (!window.confirm("Delete this post?")) return;
    try {
      await apiFetch(`/post/${postId}`, { method: 'DELETE' }, token);
      navigate('/');
    } catch {
      alert("Delete failed");
    }
  };

  const handleDeleteComment = async (commentId) => {
    if (!window.confirm("Delete this comment?")) return;
    try {
      await apiFetch(`/post/comments/${commentId}`, { method: 'DELETE' }, token);
      fetchDetails();
    } catch {
      alert("Delete failed");
    }
  };

  if (loading) return <div className="text-center mt-5">Loading post...</div>;
  if (!details) return <div className="text-center mt-5">Post not found</div>;

  const isPostAuthor = user && user.id === details.author.id;

  return (
    <div className="container mt-4 mb-5">
      <div className="card shadow-sm mx-auto">

        {/* Media */}
        <div className="text-center bg-light border-bottom">
          <img 
            src={`http://localhost:8080/post/${postId}/media`} 
            alt="Post content"
            className="img-fluid"
            style={{ maxWidth: '75vh', objectFit: 'contain' }}
            onError={(e) => e.target.style.display = 'none'}
          />
        </div>

        <div className="card-body">

          <div className="d-flex justify-content-between align-items-start mb-2">
            <div>
              <strong>@{details.author.username}</strong>
              <div className="text-muted small">
                {new Date(details.created_at).toLocaleString()}
              </div>
            </div>

            {isPostAuthor && (
              <button
                className="btn btn-sm btn-outline-danger"
                onClick={handleDeletePost}
              >
                🗑 Delete Post
              </button>
            )}
          </div>

          <p className="fs-5">{details.text}</p>

          <div className="d-flex justify-content-between align-items-center mb-3">
            <button 
              className={`btn ${details.liked_by_user ? 'btn-danger' : 'btn-outline-danger'}`}
              onClick={handleLike}
            >
              {details.liked_by_user ? '❤️' : '🤍'} {details.like_count}
            </button>
          </div>

          <hr />

          <h5>Comments</h5>

          {details.comments.length === 0 ? (
            <p className="text-muted">No comments yet.</p>
          ) : (
            details.comments.map(c => {
              const isCommentAuthor = user && user.id === c.user.id;
              return (
                <div key={c.id} className="border rounded p-2 mb-2">
                  <div className="d-flex justify-content-between">
                    <div>
                      <strong>{c.user.username}</strong>: {c.text}
                      <div className="text-muted small">
                        {new Date(c.created_at).toLocaleString()}
                      </div>
                    </div>

                    {isCommentAuthor && (
                      <button
                        className="btn btn-sm btn-outline-danger"
                        onClick={() => handleDeleteComment(c.id)}
                      >
                        🗑
                      </button>
                    )}
                  </div>
                </div>
              );
            })
          )}

          {token && (
            <form onSubmit={handleComment} className="mt-3">
              <div className="input-group">
                <input 
                  type="text" 
                  className="form-control" 
                  placeholder="Write a comment..." 
                  value={commentText}
                  onChange={(e) => setCommentText(e.target.value)}
                  required
                />
                <button className="btn btn-primary" type="submit">Post</button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};

export default PostDetail;
