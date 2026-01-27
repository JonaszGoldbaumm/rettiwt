import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import { apiFetch } from "../services/api";

const FollowButton = ({ profileId, onToggle }) => {
  const { token, user, isAuthenticated } = useAuth();
  const [following, setFollowing] = useState(false);
  const [loading, setLoading] = useState(false);

  // Check initial follow status
  useEffect(() => {
    if (!isAuthenticated || !profileId) return;

    const checkFollowing = async () => {
      try {
        const data = await apiFetch(`/profile/${profileId}/isfollow`, {}, token);
        setFollowing(data.following);
      } catch (err) {
        console.error(err);
      }
    };

    checkFollowing();
  }, [profileId, isAuthenticated, token]);

  const handleToggle = async () => {
    if (!isAuthenticated || !profileId || user.id === parseInt(profileId)) return;
    setLoading(true);

    try {
      const data = await apiFetch(`/profile/${profileId}/follow`, { method: "POST" }, token);
      setFollowing(data.following);
      if (onToggle) onToggle(); // refresh profile info
    } catch (err) {
      alert("Failed to toggle follow status");
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) return null;

  const isOwner = parseInt(profileId) === user.id;

  return (
    <button
      className={`btn ${following ? "btn-success" : "btn-outline-primary"}`}
      onClick={handleToggle}
      disabled={isOwner || loading}
    >
      {isOwner ? "Your Profile" : following ? "Following" : "Follow"}
    </button>
  );
};

export default FollowButton;
