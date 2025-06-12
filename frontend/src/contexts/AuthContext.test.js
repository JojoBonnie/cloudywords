import React from 'react';
import { render, screen, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import axios from 'axios';
import { AuthProvider, useAuth } from './AuthContext';
import { toast } from 'react-toastify';

// Mock axios
jest.mock('axios');

// Mock react-toastify
jest.mock('react-toastify', () => ({
  toast: {
    success: jest.fn(),
    error: jest.fn(),
    info: jest.fn()
  }
}));

// Test component that uses the auth context
const TestComponent = () => {
  const { currentUser, userCredits, login, register, logout, updateCredits } = useAuth();
  
  return (
    <div>
      <div data-testid="user-info">
        {currentUser ? `Logged in as ${currentUser.username}` : 'Not logged in'}
      </div>
      <div data-testid="user-credits">
        Credits: {userCredits}
      </div>
      <button 
        data-testid="login-button" 
        onClick={() => login('test@example.com', 'password')}
      >
        Login
      </button>
      <button 
        data-testid="register-button" 
        onClick={() => register('testuser', 'test@example.com', 'password', 'password')}
      >
        Register
      </button>
      <button 
        data-testid="logout-button" 
        onClick={logout}
      >
        Logout
      </button>
      <button 
        data-testid="update-credits-button" 
        onClick={updateCredits}
      >
        Update Credits
      </button>
    </div>
  );
};

describe('AuthContext', () => {
  // Clear mocks before each test
  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.clear();
  });

  test('provides initial auth state', () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );
    
    expect(screen.getByTestId('user-info')).toHaveTextContent('Not logged in');
    expect(screen.getByTestId('user-credits')).toHaveTextContent('Credits: 0');
  });

  test('login function works correctly', async () => {
    // Mock successful login response
    axios.post.mockResolvedValueOnce({
      data: { access_token: 'test-token' }
    });
    
    // Mock user info response
    axios.get.mockResolvedValueOnce({
      data: { username: 'testuser', email: 'test@example.com' }
    });
    
    // Mock credits response
    axios.get.mockResolvedValueOnce({
      data: { credits_remaining: 3 }
    });
    
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );
    
    // Click login button
    await act(async () => {
      userEvent.click(screen.getByTestId('login-button'));
    });
    
    // Wait for state to update
    await waitFor(() => {
      expect(screen.getByTestId('user-info')).toHaveTextContent('Logged in as testuser');
      expect(screen.getByTestId('user-credits')).toHaveTextContent('Credits: 3');
    });
    
    // Check that axios was called correctly
    expect(axios.post).toHaveBeenCalledWith(
      `${process.env.REACT_APP_API_URL}/auth/login/`,
      { email: 'test@example.com', password: 'password' }
    );
    
    // Check that toast was called
    expect(toast.success).toHaveBeenCalledWith('Login successful!');
    
    // Check that token was stored in localStorage
    expect(localStorage.getItem('token')).toBe('test-token');
  });

  test('register function works correctly', async () => {
    // Mock successful registration response
    axios.post.mockResolvedValueOnce({
      data: { detail: 'Registration successful' }
    });
    
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );
    
    // Click register button
    await act(async () => {
      userEvent.click(screen.getByTestId('register-button'));
    });
    
    // Check that axios was called correctly
    expect(axios.post).toHaveBeenCalledWith(
      `${process.env.REACT_APP_API_URL}/auth/registration/`,
      { 
        username: 'testuser', 
        email: 'test@example.com', 
        password1: 'password', 
        password2: 'password' 
      }
    );
    
    // Check that toast was called
    expect(toast.success).toHaveBeenCalledWith(
      'Registration successful! Please check your email to verify your account.'
    );
  });

  test('logout function works correctly', async () => {
    // Mock successful logout response
    axios.post.mockResolvedValueOnce({});
    
    // Set up initial state as logged in
    localStorage.setItem('token', 'test-token');
    axios.defaults.headers.common['Authorization'] = 'Bearer test-token';
    
    // Mock user info response for initial load
    axios.get.mockResolvedValueOnce({
      data: { username: 'testuser', email: 'test@example.com' }
    });
    
    // Mock credits response for initial load
    axios.get.mockResolvedValueOnce({
      data: { credits_remaining: 3 }
    });
    
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );
    
    // Wait for initial state to load
    await waitFor(() => {
      expect(screen.getByTestId('user-info')).toHaveTextContent('Logged in as testuser');
    });
    
    // Click logout button
    await act(async () => {
      userEvent.click(screen.getByTestId('logout-button'));
    });
    
    // Wait for state to update
    await waitFor(() => {
      expect(screen.getByTestId('user-info')).toHaveTextContent('Not logged in');
      expect(screen.getByTestId('user-credits')).toHaveTextContent('Credits: 0');
    });
    
    // Check that axios was called correctly
    expect(axios.post).toHaveBeenCalledWith(
      `${process.env.REACT_APP_API_URL}/auth/logout/`
    );
    
    // Check that toast was called
    expect(toast.info).toHaveBeenCalledWith('You have been logged out');
    
    // Check that token was removed from localStorage
    expect(localStorage.getItem('token')).toBeNull();
  });

  test('updateCredits function works correctly', async () => {
    // Mock credits response
    axios.get.mockResolvedValueOnce({
      data: { credits_remaining: 5 }
    });
    
    // Set up initial state
    localStorage.setItem('token', 'test-token');
    
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );
    
    // Click update credits button
    await act(async () => {
      userEvent.click(screen.getByTestId('update-credits-button'));
    });
    
    // Wait for state to update
    await waitFor(() => {
      expect(screen.getByTestId('user-credits')).toHaveTextContent('Credits: 5');
    });
    
    // Check that axios was called correctly
    expect(axios.get).toHaveBeenCalledWith(
      `${process.env.REACT_APP_API_URL}/user/credits/`
    );
  });
});