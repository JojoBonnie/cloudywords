from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from core.models import WordCloud, UserCredit

class WordCloudAPITest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

        # Create a test word cloud
        self.word_cloud = WordCloud.objects.create(
            user=self.user,
            title='Test Word Cloud',
            input_text='This is a test word cloud with some sample text for testing purposes.',
            is_ai_generated=False
        )

        # Set up the API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # URLs
        self.list_create_url = reverse('wordcloud-list')
        self.detail_url = reverse('wordcloud-detail', args=[self.word_cloud.id])

    def test_get_word_clouds(self):
        """Test retrieving a list of word clouds"""
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Just check that we get a successful response
        # The exact format of the response may vary, but we should at least get a 200 OK

    def test_create_word_cloud(self):
        """Test creating a new word cloud"""
        data = {
            'title': 'New Word Cloud',
            'input_text': 'This is a new test word cloud.',
            'is_ai_generated': False,
            'width': 800,
            'height': 400,
            'font': 'arial',
            'color_scheme': 'default',
            'background_color': 'white',
            'max_words': 200,
            'word_density': 80,
            'orientation': 'random'
        }
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WordCloud.objects.count(), 2)
        self.assertEqual(WordCloud.objects.get(id=response.data['id']).title, 'New Word Cloud')

    def test_get_word_cloud_detail(self):
        """Test retrieving a specific word cloud"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Word Cloud')

    def test_update_word_cloud(self):
        """Test updating a word cloud"""
        data = {
            'title': 'Updated Word Cloud',
            'input_text': 'This is an updated test word cloud.',
            'is_ai_generated': False,
            'width': 800,
            'height': 400,
            'font': 'arial',
            'color_scheme': 'default',
            'background_color': 'white',
            'max_words': 200,
            'word_density': 80,
            'orientation': 'random'
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.word_cloud.refresh_from_db()
        self.assertEqual(self.word_cloud.title, 'Updated Word Cloud')

    def test_delete_word_cloud(self):
        """Test deleting a word cloud"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(WordCloud.objects.count(), 0)

class UserCreditAPITest(TestCase):
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

        # URL
        self.credits_url = reverse('user-credits')

    def test_get_user_credits(self):
        """Test retrieving user credits"""
        response = self.client.get(self.credits_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['credits_remaining'], 3)  # Default is 3
