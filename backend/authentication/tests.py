from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from core.models import UserProfile

class AuthenticationTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Set up the API client
        self.client = APIClient()
    
    def test_login(self):
        """Test user login"""
        url = reverse('rest_login')
        data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('key', response.data)
    
    def test_logout(self):
        """Test user logout"""
        # First login to get the token
        login_url = reverse('rest_login')
        login_data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        token = login_response.data['key']
        
        # Set the token in the client
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        
        # Now logout
        logout_url = reverse('rest_logout')
        response = self.client.post(logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_registration(self):
        """Test user registration"""
        url = reverse('rest_register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_get_user(self):
        """Test retrieving user information"""
        # First login to get the token
        login_url = reverse('rest_login')
        login_data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        token = login_response.data['key']
        
        # Set the token in the client
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        
        # Now get user info
        url = reverse('rest_user_details')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')

class MFATest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Set up the API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # URLs
        self.setup_url = reverse('mfa-setup')
        self.verify_url = reverse('mfa-verify')
        self.disable_url = reverse('mfa-disable')
    
    def test_mfa_setup(self):
        """Test setting up MFA"""
        response = self.client.post(self.setup_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('qr_code', response.data)
        self.assertIn('secret_key', response.data)
    
    def test_mfa_disable(self):
        """Test disabling MFA"""
        # First enable MFA
        profile = UserProfile.objects.get(user=self.user)
        profile.mfa_enabled = True
        profile.save()
        
        # Now disable MFA
        response = self.client.post(self.disable_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that MFA is disabled
        profile.refresh_from_db()
        self.assertFalse(profile.mfa_enabled)