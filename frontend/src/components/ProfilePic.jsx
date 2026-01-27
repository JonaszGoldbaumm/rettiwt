import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const ProfilePic = ({ userId, style }) => {
  const defaultSrc = '/default_pp.jpeg';
  const [src, setSrc] = useState(defaultSrc);

  useEffect(() => {
    if (userId) {
      setSrc(`http://localhost:8080/profile/${userId}/photo?ts=${Date.now()}`);
    } else {
      setSrc(defaultSrc);
    }
  }, [userId]);

  return (
    <Link to={userId ? `/profile/${userId}` : '#'}>
      <img
        src={src}
        alt="Profile"
        onError={() => setSrc(defaultSrc)} // fallback on error
        style={{
          width: '40px',
          height: '40px',
          objectFit: 'cover',
          borderRadius: '50%',
          ...style,
        }}
      />
    </Link>
  );
};

export default ProfilePic;
