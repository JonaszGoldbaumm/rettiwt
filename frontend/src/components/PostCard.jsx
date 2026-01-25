import { useNavigate } from 'react-router-dom';

const PostCard = ({ post }) => {
  const navigate = useNavigate();

  return (
    <div 
      className="post-card" 
      onClick={() => navigate(`/post/${post.id}`)}
      style={{ borderBottom: '1px solid #ccc', padding: '10px', cursor: 'pointer' }}
    >
      <strong>@{post.user.username}</strong>
      <p>{post.text}</p>
      <div className="post-stats" style={{ fontSize: '0.8em', color: '#555' }}>
        <span>💬 {post.comment_count || 0}</span>
        <span style={{ marginLeft: '15px' }}>❤️ {post.like_count || 0}</span>
      </div>
    </div>
  );
};

export default PostCard;