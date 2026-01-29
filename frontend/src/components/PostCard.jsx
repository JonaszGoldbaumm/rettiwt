import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { apiFetch } from '../services/api';
import ProfilePic from './ProfilePic';
import { useToast } from '../context/ToastContext';

const PostCard = ({ post, onLikeUpdate }) => {
  const dateStr = new Date(post.created_at).toLocaleString();
  const [hasMedia, setHasMedia] = useState(false);
  const [mediaUrl, setMediaUrl] = useState(null);
  const { token } = useAuth();
  const { showToast } = useToast();
  const [liked, setLiked] = useState(post.liked_by_user);
  const [likeCount, setLikeCount] = useState(post.like_count || 0);

  useEffect(() => {
    if (!post.has_media) {
      setHasMedia(false);
      setMediaUrl(null);
      return;
    }

    
    setHasMedia(true);
    setMediaUrl(`http://localhost:8080/post/${post.id}/media`);
  }, [post.id, post.has_media]);

  const handleLike = async () => {
    if (!token) {
      showToast("You must be logged in to like a post", "warning");
      return;
    }
    try {
      await apiFetch(`/post/${post.id}/like`, { method: 'POST' }, token);
      // toggle local state immediately
      const newLiked = !liked;
      setLiked(newLiked);
      setLikeCount(prev => newLiked ? prev + 1 : prev - 1);
      if (onLikeUpdate) onLikeUpdate(post.id, newLiked);
    } catch {
      showToast("Action failed", "danger");
    }
  };

  return (
    <div className="card mb-4 shadow-sm rounded-4 position-relative">
      {/* Media thumbnail (top right) */}
      {hasMedia && mediaUrl && (
        <div style={{
          position: 'absolute',
          top: '8px',
          right: '8px',
          maxWidth: '15%',
          height: '64px',
          overflow: 'hidden',
          borderRadius: '4px',
        }}>
          <img 
            src={mediaUrl} 
            alt="media preview"
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              objectPosition: 'center',
            }}
          />
        </div>
      )}

      <div className="card-body">
        <div className="d-flex align-items-center mb-2">
          <ProfilePic userId={post.user.id} profilePic={post.user.profile_pic} />
          <div className="ms-2">
            <Link to={`/profile/${post.user.id}`} className="text-decoration-none">
              <strong>@{post.user.username}</strong>
            </Link>
            <br />
            <Link to={`/post/${post.id}`} className="text-muted small">{dateStr}</Link>
          </div>
        </div>

        <p>{post.text.length > 100 ? post.text.slice(0, 100) + "..." : post.text}</p>

        {/* Like / comment info */}
        <div className="d-flex align-items-center gap-3 mt-2">
          <span 
            style={{ cursor: 'pointer', fontSize: '1.2rem', userSelect: 'none' }}
            onClick={handleLike}
            title={liked ? "Unlike" : "Like"}
          >
            {liked ? '❤️' : '🤍'} {likeCount}
          </span>
          <span>💬 {post.comment_count || 0}</span>
        </div>
      </div>
    </div>
  );
};

export default PostCard;
