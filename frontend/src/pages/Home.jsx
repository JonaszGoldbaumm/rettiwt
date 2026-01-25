import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { apiFetch } from '../services/api';
import PostCard from '../components/PostCard';

const Home = () => {
  const { token, isAuthenticated } = useAuth();
  const [feedType, setFeedType] = useState('global');
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    const fetchFeed = async () => {
      try {
        const endpoint = feedType === 'global' ? '/feed/global' : '/feed/followed';
        const data = await apiFetch(endpoint, {}, token);
        setPosts(data.posts);
      } catch (err) {
        console.error(err);
      }
    };
    fetchFeed();
  }, [feedType, token]);

  return (
    <div>
      <div className="feed-toggle">
        <button onClick={() => setFeedType('global')}>Global</button>
        {isAuthenticated && (
          <button onClick={() => setFeedType('followed')}>Following</button>
        )}
      </div>

      <div className="feed-list">
        {posts.map(post => <PostCard key={post.id} post={post} />)}
      </div>
    </div>
  );
};

export default Home;