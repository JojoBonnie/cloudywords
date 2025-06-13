import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      // Use Token format for Django REST Framework (consistent with AuthContext)
      config.headers['Authorization'] = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle token expiration
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response && error.response.status === 401) {
      // Token expired or invalid, redirect to login
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Word Cloud API
export const wordCloudApi = {
  getAll: () => api.get('/wordclouds/'),
  
  getById: (id) => api.get(`/wordclouds/${id}/`),
  
  create: (wordCloudData) => api.post('/wordclouds/', wordCloudData),
  
  update: (id, wordCloudData) => api.put(`/wordclouds/${id}/`, wordCloudData),
  
  delete: (id) => api.delete(`/wordclouds/${id}/`),
  
  generate: (wordCloudData) => api.post('/wordclouds/generate/', wordCloudData),
  
  export: (id, format, resolution) => api.post(
    `/wordclouds/${id}/export/`,
    { format, resolution },
    { responseType: 'blob' }
  ),
};

// AI Suggestions API
export const aiApi = {
  getWordSuggestions: (topic, count) => api.post('ai/suggestions/', { topic, count }),
};

// User API
export const userApi = {
  getCredits: () => api.get('user/credits/'),
};

// Auth API
export const authApi = {
  login: (email, password) => api.post('auth/login/', { email, password }),
  
  register: (userData) => api.post('auth/registration/', userData),
  
  logout: () => api.post('auth/logout/'),
  
  getUser: () => api.get('auth/user/'),
  
  setupMFA: () => api.post('auth/mfa/setup/'),
  
  verifyMFA: (token) => api.post('auth/mfa/verify/', { token }),
  
  disableMFA: () => api.post('auth/mfa/disable/'),
};

export default api;