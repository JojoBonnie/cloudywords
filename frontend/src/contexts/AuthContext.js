import React, { createContext, useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';

// Create context
const AuthContext = createContext(null);

// Create a provider component
export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [userCredits, setUserCredits] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Initialize auth state on app load
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      // Configure axios with the token
      axios.defaults.headers.common['Authorization'] = `Token ${token}`;

      // Fetch user info
      fetchUserInfo();
    } else {
      setLoading(false);
    }
  }, []);

  // Fetch user info including credits
  const fetchUserInfo = async () => {
    try {
      const userResponse = await axios.get(`${process.env.REACT_APP_API_URL}/auth/user/`);
      setCurrentUser(userResponse.data);

      // Fetch user credits
      const creditsResponse = await axios.get(`${process.env.REACT_APP_API_URL}/user/credits/`);
      setUserCredits(creditsResponse.data.credits_remaining);

      setLoading(false);
    } catch (err) {
      console.error('Error fetching user info (TEST):', err);
      logout();
      setLoading(false);
    }
  };

  // Login function
  const login = async (email, password) => {
    try {
      setLoading(true);
      setError(null); // Clear previous errors

      const response = await axios.post(`${process.env.REACT_APP_API_URL}/auth/login/`, {
        email,
        password
      });

      // Store token in localStorage
      // Handle both token formats (JWT and regular token)
      const token = response.data.access_token || response.data.access || response.data.key;

      if (!token) {
        throw new Error('No authentication token received');
      }

      localStorage.setItem('token', token);

      // Set default Authorization header
      axios.defaults.headers.common['Authorization'] = `Token ${token}`;

      // Fetch user info - but don't let it block the login success
      try {
        await fetchUserInfo();
      } catch (userInfoError) {
        console.warn('Failed to fetch user info after login, but login was successful:', userInfoError);
        // Set loading to false even if user info fetch fails
        setLoading(false);
      }

      toast.success('Login successful!');
      return true;
    } catch (err) {
      console.error('Login error:', err);
      const errorMessage = err.response?.data?.detail || err.message || 'Login failed. Please check your credentials.';
      setError(errorMessage);
      toast.error(errorMessage);
      setLoading(false);
      return false;
    }
  };

  // Register function
  const register = async (username, email, password1, password2) => {
    try {
      setLoading(true);
      await axios.post(`${process.env.REACT_APP_API_URL}/auth/registration/`, {
        username,
        email,
        password1,
        password2
      });

      toast.success('Registration successful!');
      setLoading(false);
      return true;
    } catch (err) {
      console.error('Registration error:', err);
      const errorMsg = err.response?.data?.detail ||
        Object.values(err.response?.data || {}).flat().join(' ') ||
        'Registration failed. Please try again.';
      setError(errorMsg);
      toast.error(errorMsg);
      setLoading(false);
      return false;
    }
  };

  // Logout function
  const logout = async () => {
    try {
      await axios.post(`${process.env.REACT_APP_API_URL}/auth/logout/`);
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      // Clear local storage and state
      localStorage.removeItem('token');
      delete axios.defaults.headers.common['Authorization'];
      setCurrentUser(null);
      setUserCredits(0);
      setLoading(false);
      toast.info('You have been logged out');
    }
  };

  // Update credits after using AI
  const updateCredits = async () => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_API_URL}/user/credits/`);
      setUserCredits(response.data.credits_remaining);
    } catch (err) {
      console.error('Error updating credits:', err);
    }
  };

  const value = {
    currentUser,
    userCredits,
    loading,
    error,
    login,
    register,
    logout,
    updateCredits
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Create a hook for using the auth context
export const useAuth = () => {
  return useContext(AuthContext);
};