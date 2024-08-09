import React, { createContext, useState, useContext } from 'react';

const AuthContext = createContext();

const currentToken = localStorage.getItem('token');

export const AuthProvider = ({ children }) => {
    const [apiToken, setAPIToken] = useState(currentToken)

  const login = async(username,
    password) => {
    try {
        const response = await axios.post(`${API_URL}/token`, {
          username,
          password
        },  {
          headers: {
            'Content-Type': 'application/json'
          }});
        localStorage.setItem('token', response.data.access_token);
        setAPIToken(response.data.access_token)
    } catch (error) {
        console.error('Login failed:', error);
    }
  };
  const logout = () => {
    localStorage.setItem('token', null);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated: !!apiToken, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
