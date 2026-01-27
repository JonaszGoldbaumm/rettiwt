import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { apiFetch } from '../services/api';
import PostCard from '../components/PostCard';
import ProfilePic from '../components/ProfilePic';
import FollowButton from '../components/FollowButton';

const ProfilePage = () => {
  const { userId } = useParams();
  const { token, isAuthenticated, user } = useAuth();

  const [profile, setProfile] = useState(null);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchProfileAndPosts = async () => {
    setLoading(true);
    setError(null);
    try {
      const profileData = await apiFetch(`/profile/${userId}`, {}, token);
      setProfile(profileData);

      const postsData = await apiFetch(`/feed/user/${userId}`, {}, token);
      setPosts(postsData.posts || []);
    } catch (err) {
      console.error(err);
      setError("Failed to load profile.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfileAndPosts();
  }, [userId, token]);

  if (loading) return <div className="text-center mt-5">Loading profile...</div>;
  if (error) return <div className="text-center mt-5 text-danger">{error}</div>;
  if (!profile) return <div className="text-center mt-5">User not found</div>;

  return (
    <div className="container mt-4 mb-5">
      <div className="card shadow-sm p-4 mb-4 text-center">
        <ProfilePic 
          userId={profile.id} 
          profilePic={profile.profile_pic} 
          style={{ width: '120px', height: '120px' }} 
        />
        <h3 className="mt-2">@{profile.username}</h3>
        {profile.description && <p className="text-muted">{profile.description}</p>}

        <div className="d-flex justify-content-center gap-4 mt-3">
          <span>Followers: {profile.followers_count}</span>
          <span>Following: {profile.followed_count}</span>
        </div>
        {isAuthenticated && parseInt(userId) !== user.id && (
        <div className="text-center mt-3">
            <FollowButton
            profileId={userId}
            onToggle={fetchProfileAndPosts} // Refresh profile after follow/unfollow
            />
        </div>
        )}

        {isAuthenticated && user && parseInt(userId) === user.id && (
          <div className="text-center mt-3">
            <Link to="/profile/edit" className="btn btn-outline-primary">
              Edit Profile
            </Link>
          </div>
        )}
      </div>

      <h4 className="mb-3">Posts</h4>
      {posts.length === 0 ? (
        <p className="text-center fs-5 text-muted">No posts yet.</p>
      ) : (
        posts.map(p => <PostCard key={p.id} post={p} />)
      )}
    </div>
  );
};

export default ProfilePage;
