from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import WordCloud, UserCredit, UserProfile

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
            'color_scheme': 'Default',
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
            'color_scheme': 'Default',
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

class AIWordSuggestionsTest(TestCase):
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
        self.suggestions_url = reverse('ai-word-suggestions')

    def test_get_word_suggestions(self):
        """Test getting AI word suggestions"""
        data = {
            'topic': 'test',
            'count': 5
        }
        response = self.client.post(self.suggestions_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The actual response content will depend on the AI implementation
        # but we can at least check that the response has the expected structure
        self.assertIn('suggestions', response.data)

class WordCloudGenerateTest(TestCase):
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
        self.generate_url = reverse('wordcloud-generate')

    def test_generate_word_cloud(self):
        """Test generating a word cloud"""
        data = {
            'title': 'Generated Word Cloud',
            'input_text': 'This is a test for generating a word cloud.',
            'width': 800,
            'height': 400,
            'font': 'arial',
            'color_scheme': 'default',
            'background_color': 'white',
            'max_words': 200,
            'word_density': 80,
            'orientation': 'random'
        }
        response = self.client.post(self.generate_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['title'], 'Generated Word Cloud')

class WordCloudExportTest(TestCase):
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

        # URL
        self.export_url = reverse('wordcloud-export', args=[self.word_cloud.id])

    def test_export_word_cloud(self):
        """Test exporting a word cloud"""
        data = {
            'format': 'png',
            'resolution': 'high'
        }
        response = self.client.post(self.export_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The response should be a file download, so we can't check the content directly
        # but we can check that the response has the correct content type
        self.assertEqual(response['Content-Type'], 'image/png')


class UserProfileModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_profile_creation(self):
        """Test that a UserProfile is automatically created when a User is created"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)
        self.assertEqual(self.user.profile.user, self.user)
        self.assertFalse(self.user.profile.mfa_enabled)

    def test_profile_str_method(self):
        """Test the string representation of a UserProfile"""
        self.assertEqual(str(self.user.profile), 'testuser')


class UserCreditModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_credit_creation(self):
        """Test that a UserCredit is automatically created when a User is created"""
        self.assertTrue(hasattr(self.user, 'credits'))
        self.assertIsInstance(self.user.credits, UserCredit)
        self.assertEqual(self.user.credits.user, self.user)
        self.assertEqual(self.user.credits.credits_remaining, 3)  # Default is 3

    def test_credit_str_method(self):
        """Test the string representation of a UserCredit"""
        self.assertEqual(str(self.user.credits), 'testuser - 3 credits')


class WordCloudModelTest(TestCase):
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

    def test_word_cloud_creation(self):
        """Test that a WordCloud can be created with the required fields"""
        self.assertEqual(self.word_cloud.user, self.user)
        self.assertEqual(self.word_cloud.title, 'Test Word Cloud')
        self.assertEqual(self.word_cloud.input_text,
                         'This is a test word cloud with some sample text for testing purposes.')
        self.assertFalse(self.word_cloud.is_ai_generated)

        # Test default values
        self.assertEqual(self.word_cloud.width, 800)
        self.assertEqual(self.word_cloud.height, 400)
        self.assertEqual(self.word_cloud.font, 'arial')
        self.assertEqual(self.word_cloud.color_scheme, 'default')
        self.assertEqual(self.word_cloud.background_color, 'white')
        self.assertEqual(self.word_cloud.max_words, 200)
        self.assertEqual(self.word_cloud.word_density, 80)
        self.assertEqual(self.word_cloud.orientation, 'random')

    def test_word_cloud_str_method(self):
        """Test the string representation of a WordCloud"""
        self.assertEqual(str(self.word_cloud), 'Test Word Cloud')