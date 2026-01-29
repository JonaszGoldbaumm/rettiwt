import { Link } from "react-router-dom";

const NotFound = () => {
  return (
    <div className="d-flex flex-column align-items-center justify-content-center text-center" style={{ minHeight: "60vh" }}>
      <h1 className="display-4">404</h1>
      <p className="lead">Page not found</p>
      <p className="text-muted">The page you’re looking for doesn’t exist.</p>
      <Link to="/" className="btn btn-primary mt-3">
        Go Home
      </Link>
    </div>
  );
};

export default NotFound;
