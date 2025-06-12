from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile, UserCredit, WordCloud

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
        self.assertEqual(self.word_cloud.input_text, 'This is a test word cloud with some sample text for testing purposes.')
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