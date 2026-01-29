import { createContext, useContext, useState, useEffect } from "react";
import { apiFetch } from "../services/api";
import { Navigate, useNavigate } from "react-router-dom";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [user, setUser] = useState(null);

  const isAuthenticated = !!token;

  // fetch user info if token exists
  useEffect(() => {
    if (token && !user) {
      console.log("sprawdzamdane");
      apiFetch("/profile/me/profile", {}, token)
        .then(setUser)
        .catch(() => {
          logout();
        });
    }
  }, [token]);

  const login = async (authData) => {
    const { access_token, user_id, username } = authData;


    localStorage.setItem("token", access_token);
    

    setToken(access_token);
    setUser({ id: user_id, username: username });
  };

  const logout = () => {
    console.log("logging out");
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ token, login, logout, isAuthenticated, user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
