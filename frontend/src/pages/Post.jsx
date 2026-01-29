import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { apiFetch } from '../services/api';
import { useToast } from '../context/ToastContext';
import ProfilePic from '../components/ProfilePic';
import { Link } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';

const PostDetail = () => {
  const { postId } = useParams();
  const navigate = useNavigate();
  const { token, user } = useAuth();
  const [details, setDetails] = useState(null);
  const [commentText, setCommentText] = useState('');
  const [loading, setLoading] = useState(true);
  const { showToast } = useToast();
  const { theme } = useTheme();

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
      showToast("Action failed", "danger");
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
      showToast("Posting a comment failed", "danger");
    }
  };

  const handleDeletePost = async () => {
    if (!window.confirm("Delete this post?")) return;
    try {
      await apiFetch(`/post/${postId}`, { method: 'DELETE' }, token);
      navigate('/');
    } catch {
      showToast("Deleteing post failed", "danger");
    }
  };

  const handleDeleteComment = async (commentId) => {
    if (!window.confirm("Delete this comment?")) return;
    try {
      await apiFetch(`/post/comments/${commentId}`, { method: 'DELETE' }, token);
      fetchDetails();
    } catch {
      showToast("Deleteing comment failed", "danger");
    }
  };

  if (loading) return <div className="text-center mt-5">Loading post...</div>;
  if (!details) return <div className="text-center mt-5">Post not found</div>;

  const isPostAuthor = user && user.id === details.author.id;

  return (
    <div className="container mt-4 mb-5">
      <div className="card shadow-sm mx-auto">

        {/* media */}
        {details.has_media && (
          <div className="text-center border-bottom"
            style={{
              color: theme === "light" ? "#f8f9fa" : "#2c2c2c",
              backgroundColor: theme === "light" ? "#f8f9fa" : "#2c2c2c",
              padding: "1rem",
            }}
          >
            <img 
              src={`http://localhost:8080/post/${postId}/media`} 
              alt="Post content"
              className="img-fluid"
              style={{
                maxWidth: "75vh",
                objectFit: "contain",
                backgroundColor: theme === "light" ? "#f8f9fa" : "#2c2c2c",
                display: "inline-block",
              }}
            />
          </div>
        )}

        <div className="card-body">

          <div className="d-flex justify-content-between align-items-start mb-2">
            <div className="d-flex align-items-center">
                <ProfilePic
                  userId={details.author.id}
                  profilePic={details.author.profile_pic}
                  style={{ width: "40px", height: "40px" }}
                />

              <div className="ms-2">
                <Link to={`/profile/${details.author.id}`} className="text-decoration-none">
                  <strong>@{details.author.username}</strong>
                </Link>
                <div className="text-muted small">
                  {new Date(details.created_at).toLocaleString()}
                </div>
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
                    <div className='d-flex'>
                        <ProfilePic
                          userId={c.user.id}
                          profilePic={c.user.profile_pic}
                          style={{width: "32px", height: "32px"}}
                        />
                      <div className='ms-2'>
                        <Link to={'/profile/${c.user.id}'} className='text-decoration-none'>
                          <strong>@{c.user.username}</strong>
                        </Link>: {c.text}
                      </div>
                      <div className="text-muted small m-1">
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
