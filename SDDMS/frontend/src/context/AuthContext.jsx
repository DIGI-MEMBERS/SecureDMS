import { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [role, setRole] = useState("Investigating Officer");
  const [isAuthenticated, setIsAuthenticated] = useState(true);

  const login = (userData, userRole) => {
    setUser(userData);
    setRole(userRole);
    setIsAuthenticated(true);
  };

  const logout = () => {
    setUser(null);
    setRole(null);
    setIsAuthenticated(false);
  };

  const value = {
    user,
    role,
    isAuthenticated,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}