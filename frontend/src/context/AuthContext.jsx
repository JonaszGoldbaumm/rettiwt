import { createContext, useContext, useState, useEffect } from "react";

const AuthContext = createContext();

export const AuthProvider = ({children}) => {
    const [token, setToken] = useState(localStorage.getItem('token'));
    const [user, setUser] = useState(null);

    const login = (newToken) => {
        localStorage.setItem('token', newToken);
        setToken(newToken);
    }
    const logout = () =>{
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
    }
    const isAuthenticated = !!token;

    return (
        <AuthContext.Provider value={{ token, login, logout, isAuthenticated, user, setUser }}>
        {children}
        </AuthContext.Provider>
    );
}

export const useAuth = () => useContext(AuthContext);