import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { apiFetch } from '../services/api';
import PostCard from '../components/PostCard';
import CreatePost from '../components/CreatePost';

const Home = () => {
  const { token, isAuthenticated } = useAuth();
  const [feedType, setFeedType] = useState('global');
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchFeed = async (type = feedType) => {
    setLoading(true);
    try {
      let endpoint = '/feed/';
      if (type === 'followed') endpoint = '/feed/followed';
      if (type === 'media') endpoint = '/feed/media';
      const data = await apiFetch(endpoint, {}, token);
      setPosts(data.posts || []);
    } catch {
      setPosts([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!isAuthenticated && feedType !== 'global') {
      setFeedType('global');
    }
  }, [isAuthenticated, feedType]);

  useEffect(() => {
    fetchFeed(feedType);
  }, [feedType, token]);

  return (
    <div className="d-flex flex-column align-items-center px-2">
      {isAuthenticated && <CreatePost onPostCreated={() => fetchFeed()} />}

      {isAuthenticated && (
        <div className="btn-group mb-3">
          <button className="btn btn-outline-primary" onClick={() => setFeedType('global')}>Global</button>
          <button className="btn btn-outline-primary" onClick={() => setFeedType('media')}>Media</button>
          <button className="btn btn-outline-primary" onClick={() => setFeedType('followed')}>Following</button>
        </div>
      )}

      {loading ? (
        <div className="text-center mt-5">Loading feed...</div>
      ) : posts.length === 0 ? (
        <h3 className="text-center text-muted mt-5">No posts found</h3>
      ) : (
        posts.map(p => (
          <div key={p.id} className="w-100 w-md-75 w-lg-50 mb-3">
            <PostCard post={p} />
          </div>
        ))
      )}
    </div>
  );
};

export default Home;
