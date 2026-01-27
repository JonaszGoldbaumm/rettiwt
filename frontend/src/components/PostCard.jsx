import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import ProfilePic from './ProfilePic';

const PostCard = ({ post }) => {
  const dateStr = new Date(post.created_at).toLocaleString();
  const [hasMedia, setHasMedia] = useState(false);

  useEffect(() => {
    const checkMedia = async () => {
      try {
        const res = await fetch(`http://localhost:8080/post/${post.id}/media`, {
          method: 'GET',
        });

        if (res.ok) {
          setHasMedia(true); // Media exists
        }
      } catch (err) {
        // Ignore errors → treat as no media
        setHasMedia(false);
      }
    };

    checkMedia();
  }, [post.id]);

  return (
    <div className="card mb-4 shadow-sm rounded-4">
      <div className="card-body">
        <div className="d-flex align-items-center mb-2">
          <ProfilePic userId={post.user.id} profilePic={post.user.profile_pic} />
          <div className="ms-2">
            <strong>@{post.user.username}</strong>
            {hasMedia && (
              <span className="ms-1 text-muted" title="Contains media">📷</span>
            )}
            <br />
            <Link to={`/post/${post.id}`} className="text-muted small">{dateStr}</Link>
          </div>
        </div>

        <p>{post.text.length > 100 ? post.text.slice(0, 100) + "..." : post.text}</p>

        <div className="text-muted small mt-2">
          ❤️ {post.like_count || 0} &nbsp; 💬 {post.comment_count || 0}
        </div>
      </div>
    </div>
  );
};

export default PostCard;
