import axios from 'axios';
import { wordCloudApi, aiApi, userApi, authApi } from './api';

// Mock axios
jest.mock('axios');

describe('API Services', () => {
  // Reset mocks before each test
  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.clear();
  });

  describe('wordCloudApi', () => {
    test('getAll should call the correct endpoint', async () => {
      // Setup
      const mockResponse = { data: [{ id: 1, title: 'Test Word Cloud' }] };
      axios.get.mockResolvedValue(mockResponse);

      // Execute
      const result = await wordCloudApi.getAll();

      // Verify
      expect(axios.get).toHaveBeenCalledWith('/wordclouds/');
      expect(result).toEqual(mockResponse);
    });

    test('getById should call the correct endpoint with ID', async () => {
      // Setup
      const mockResponse = { data: { id: 1, title: 'Test Word Cloud' } };
      axios.get.mockResolvedValue(mockResponse);

      // Execute
      const result = await wordCloudApi.getById(1);

      // Verify
      expect(axios.get).toHaveBeenCalledWith('/wordclouds/1/');
      expect(result).toEqual(mockResponse);
    });

    test('create should call the correct endpoint with data', async () => {
      // Setup
      const mockData = { title: 'New Word Cloud', input_text: 'Test text' };
      const mockResponse = { data: { id: 1, ...mockData } };
      axios.post.mockResolvedValue(mockResponse);

      // Execute
      const result = await wordCloudApi.create(mockData);

      // Verify
      expect(axios.post).toHaveBeenCalledWith('/wordclouds/', mockData);
      expect(result).toEqual(mockResponse);
    });

    test('update should call the correct endpoint with ID and data', async () => {
      // Setup
      const mockData = { title: 'Updated Word Cloud', input_text: 'Updated text' };
      const mockResponse = { data: { id: 1, ...mockData } };
      axios.put.mockResolvedValue(mockResponse);

      // Execute
      const result = await wordCloudApi.update(1, mockData);

      // Verify
      expect(axios.put).toHaveBeenCalledWith('/wordclouds/1/', mockData);
      expect(result).toEqual(mockResponse);
    });

    test('delete should call the correct endpoint with ID', async () => {
      // Setup
      const mockResponse = { data: {} };
      axios.delete.mockResolvedValue(mockResponse);

      // Execute
      const result = await wordCloudApi.delete(1);

      // Verify
      expect(axios.delete).toHaveBeenCalledWith('/wordclouds/1/');
      expect(result).toEqual(mockResponse);
    });

    test('generate should call the correct endpoint with data', async () => {
      // Setup
      const mockData = { input_text: 'Test text' };
      const mockResponse = { data: { id: 1, image_url: 'http://example.com/image.png' } };
      axios.post.mockResolvedValue(mockResponse);

      // Execute
      const result = await wordCloudApi.generate(mockData);

      // Verify
      expect(axios.post).toHaveBeenCalledWith('/wordclouds/generate/', mockData);
      expect(result).toEqual(mockResponse);
    });

    test('export should call the correct endpoint with ID and format', async () => {
      // Setup
      const mockResponse = { data: new Blob(['test']) };
      axios.post.mockResolvedValue(mockResponse);

      // Execute
      const result = await wordCloudApi.export(1, 'png', 'high');

      // Verify
      expect(axios.post).toHaveBeenCalledWith(
        '/wordclouds/1/export/',
        { format: 'png', resolution: 'high' },
        { responseType: 'blob' }
      );
      expect(result).toEqual(mockResponse);
    });
  });

  describe('aiApi', () => {
    test('getWordSuggestions should call the correct endpoint with topic and count', async () => {
      // Setup
      const mockResponse = { data: ['word1', 'word2', 'word3'] };
      axios.post.mockResolvedValue(mockResponse);

      // Execute
      const result = await aiApi.getWordSuggestions('test', 3);

      // Verify
      expect(axios.post).toHaveBeenCalledWith('/ai/suggestions/', { topic: 'test', count: 3 });
      expect(result).toEqual(mockResponse);
    });
  });

  describe('userApi', () => {
    test('getCredits should call the correct endpoint', async () => {
      // Setup
      const mockResponse = { data: { credits_remaining: 3 } };
      axios.get.mockResolvedValue(mockResponse);

      // Execute
      const result = await userApi.getCredits();

      // Verify
      expect(axios.get).toHaveBeenCalledWith('/user/credits/');
      expect(result).toEqual(mockResponse);
    });
  });

  describe('authApi', () => {
    test('login should call the correct endpoint with credentials', async () => {
      // Setup
      const mockResponse = { data: { key: 'test-token' } };
      axios.post.mockResolvedValue(mockResponse);

      // Execute
      const result = await authApi.login('test@example.com', 'password');

      // Verify
      expect(axios.post).toHaveBeenCalledWith('/auth/login/', { email: 'test@example.com', password: 'password' });
      expect(result).toEqual(mockResponse);
    });

    test('register should call the correct endpoint with user data', async () => {
      // Setup
      const mockData = { username: 'testuser', email: 'test@example.com', password1: 'password', password2: 'password' };
      const mockResponse = { data: { key: 'test-token' } };
      axios.post.mockResolvedValue(mockResponse);

      // Execute
      const result = await authApi.register(mockData);

      // Verify
      expect(axios.post).toHaveBeenCalledWith('/auth/registration/', mockData);
      expect(result).toEqual(mockResponse);
    });

    test('logout should call the correct endpoint', async () => {
      // Setup
      const mockResponse = { data: {} };
      axios.post.mockResolvedValue(mockResponse);

      // Execute
      const result = await authApi.logout();

      // Verify
      expect(axios.post).toHaveBeenCalledWith('/auth/logout/');
      expect(result).toEqual(mockResponse);
    });

    test('getUser should call the correct endpoint', async () => {
      // Setup
      const mockResponse = { data: { username: 'testuser', email: 'test@example.com' } };
      axios.get.mockResolvedValue(mockResponse);

      // Execute
      const result = await authApi.getUser();

      // Verify
      expect(axios.get).toHaveBeenCalledWith('/auth/user/');
      expect(result).toEqual(mockResponse);
    });
  });
});