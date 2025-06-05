"""
Django settings for wordcloud_project project.

This is the main configuration file for the Cloudy Words project. 
It contains settings for database connections, authentication, static/media files,
API integrations, and security configurations.

For new contributors:
1. Create a .env file based on .env.example
2. Set DEBUG=True for local development
3. Run 'python manage.py collectstatic' if static files aren't loading
4. Use SQLite for local development (default configuration)
"""

import os
from datetime import timedelta
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

# -------------------------------------------------------------------------
# Environment Configuration
# -------------------------------------------------------------------------
# Load environment variables from .env file
# Create a .env file in the project root based on .env.example
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# This sets the base directory for the project, used for file path references
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------------------------
# Core Django Settings
# -------------------------------------------------------------------------
# SECURITY WARNING: keep the secret key used in production secret!
# In production, set this in environment variables or .env file
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-dev-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
# Set DEBUG=True in .env for development, False for production
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Hosts that are allowed to access this application
# For production, add your domain names to this list
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# -------------------------------------------------------------------------
# Application Definition
# -------------------------------------------------------------------------
# List of installed Django applications
# Django's built-in apps + third-party + project-specific apps
INSTALLED_APPS = [
    # Django built-in apps
    'django.contrib.admin',          # Admin site
    'django.contrib.auth',           # Authentication system
    'django.contrib.contenttypes',   # Content type system
    'django.contrib.sessions',       # Session framework
    'django.contrib.messages',       # Messaging framework
    'django.contrib.staticfiles',    # Static files management
    'django.contrib.sites',          # Site framework (required for allauth)

    # Third party apps
    'rest_framework',                # Django REST Framework for API
    'rest_framework.authtoken',      # Token authentication
    'corsheaders',                   # Cross-Origin Resource Sharing
    'drf_yasg',                      # Swagger/OpenAPI documentation
    'django_filters',                # Filtering for API endpoints

    # Authentication apps
    'allauth',                       # Advanced authentication
    'allauth.account',               # User accounts
    'allauth.socialaccount',         # Social authentication
    'allauth.socialaccount.providers.google',  # Google OAuth
    'allauth.socialaccount.providers.github',  # GitHub OAuth
    'dj_rest_auth',                  # REST API auth endpoints
    'dj_rest_auth.registration',     # Registration endpoints
    'django_otp',                    # Two-factor authentication
    'django_otp.plugins.otp_totp',   # Time-based one-time passwords

    # Project-specific apps
    'core',                          # Core functionality
    'authentication',                # Custom authentication logic
    'wordcloud_api',                 # Word cloud API endpoints
]

# -------------------------------------------------------------------------
# Middleware Configuration
# -------------------------------------------------------------------------
# Middleware is executed in order, so the order matters here
MIDDLEWARE = [
    # Security middleware - should be at/near the top
    'django.middleware.security.SecurityMiddleware',     # Security headers and checks
    
    # Static file serving (development and production)
    'whitenoise.middleware.WhiteNoiseMiddleware',        # Efficient static file serving
    
    # Session and CORS handling
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session support
    'corsheaders.middleware.CorsMiddleware',             # CORS handling (must be before CommonMiddleware)
    'django.middleware.common.CommonMiddleware',         # Common request processing
    
    # Security middleware (duplicate) - this appears to be a mistake, can be removed
    "django.middleware.security.SecurityMiddleware",
    
    # Authentication middlewares
    "allauth.account.middleware.AccountMiddleware",      # Allauth account handling
    'django.middleware.csrf.CsrfViewMiddleware',         # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Authentication
    'django_otp.middleware.OTPMiddleware',               # Two-factor authentication
    
    # Other middleware
    'django.contrib.messages.middleware.MessageMiddleware',  # Flash messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
]

# -------------------------------------------------------------------------
# URL Configuration
# -------------------------------------------------------------------------
# Root URL configuration module
ROOT_URLCONF = 'wordcloud_project.urls'

# -------------------------------------------------------------------------
# Template Configuration
# -------------------------------------------------------------------------
# Settings for Django's template engine
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Project-level templates directory
        'APP_DIRS': True,                  # Look for templates in app directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Required by allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application path for production deployment
WSGI_APPLICATION = 'wordcloud_project.wsgi.application'

# -------------------------------------------------------------------------
# Database Configuration
# -------------------------------------------------------------------------
# Database settings using dj-database-url for flexible configuration
# In development: SQLite database is used by default
# In production: Set DATABASE_URL in environment variables for PostgreSQL, MySQL, etc.
# Example: DATABASE_URL=postgres://user:password@host:port/database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Default to SQLite for development
        'NAME': BASE_DIR / 'db.sqlite3',         # SQLite database file
    }
}

# -------------------------------------------------------------------------
# Password Validation
# -------------------------------------------------------------------------
# Password validators enforce password complexity
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# -------------------------------------------------------------------------
# Internationalization
# -------------------------------------------------------------------------
# Language and time settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'      # Use UTC for all stored times
USE_I18N = True        # Enable internationalization
USE_TZ = True          # Enable timezone awareness

# -------------------------------------------------------------------------
# Static Files Configuration (CSS, JavaScript, Images)
# -------------------------------------------------------------------------
# Static files configuration (for development)
# In development, Django serves static files directly
# In production, these should be served by a web server or CDN

# URL prefix for static files
STATIC_URL = '/static/'

# Local directories where static files are stored
# Add your app-specific static directories here if needed
STATICFILES_DIRS = [BASE_DIR / 'static']  

# Directory where collectstatic will collect all static files
# Run python manage.py collectstatic to populate this directory
STATIC_ROOT = BASE_DIR / 'staticfiles'  

# -------------------------------------------------------------------------
# Media Files Configuration (User Uploads)
# -------------------------------------------------------------------------
# Media files configuration (for development)
# These are files uploaded by users

# URL prefix for media files
MEDIA_URL = '/media/'

# Directory where media files are stored
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_REDIRECT_URL = '/dashboard/' # Where to go after login
ACCOUNT_LOGOUT_REDIRECT_URL = '/' # Where to go after logout
SOCIALACCOUNT_LOGIN_ON_GET = True  # Automatically log in users after social account authentication

# -------------------------------------------------------------------------
# Storage Backends
# -------------------------------------------------------------------------
# For development, use local file system storage
# For production, these would be changed to Azure Blob Storage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# -------------------------------------------------------------------------
# Default Primary Key Field Type
# -------------------------------------------------------------------------
# Use BigAutoField as default primary key field type (Django 3.2+)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------------------------------------------------
# CORS (Cross-Origin Resource Sharing) Settings
# -------------------------------------------------------------------------
# Control which domains can access your API
# For production, add your frontend domain(s)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",    # React development server
    "http://127.0.0.1:3000",    # Alternative local address
]
# Allow cookies to be sent with CORS requests
CORS_ALLOW_CREDENTIALS = True

# Trusted origins for CSRF (should match CORS origins)
# Also configurable via environment variables
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000').split(',')

# -------------------------------------------------------------------------
# REST Framework Settings
# -------------------------------------------------------------------------
# Configuration for Django REST Framework
REST_FRAMEWORK = {
    # Authentication methods (in order of precedence)
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT tokens
        'rest_framework.authentication.SessionAuthentication',        # Session auth
        'rest_framework.authentication.TokenAuthentication',          # Token auth
    ),
    # Default permission policy - require authentication
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAuthenticated',
    ),
    # Pagination settings
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # Default number of items per page
}

# -------------------------------------------------------------------------
# JWT (JSON Web Token) Settings
# -------------------------------------------------------------------------
# Configuration for SimpleJWT (used for token-based authentication)
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),      # How long access tokens are valid
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),      # How long refresh tokens are valid
    'ROTATE_REFRESH_TOKENS': True,                    # Issue new refresh token when refreshing
    'BLACKLIST_AFTER_ROTATION': True,                 # Blacklist old refresh tokens
}

# -------------------------------------------------------------------------
# Authentication Settings
# -------------------------------------------------------------------------
# Configure authentication backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',         # Default Django auth
    'allauth.account.auth_backends.AuthenticationBackend',  # AllAuth
)

# Site ID for django.contrib.sites
SITE_ID = 1

# AllAuth settings
ACCOUNT_EMAIL_REQUIRED = True                 # Email is required for registration
ACCOUNT_EMAIL_VERIFICATION = 'optional'       # Email verification is optional
ACCOUNT_AUTHENTICATION_METHOD = 'email'       # Use email for authentication (corrected setting name)
ACCOUNT_ADAPTER = 'authentication.adapters.CustomAccountAdapter'  # Custom adapter for email confirmation

# -------------------------------------------------------------------------
# Social Authentication Settings
# -------------------------------------------------------------------------
# Configuration for social authentication providers (Google, GitHub)
# You need to register your app with these providers and get client IDs/secrets
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'github': {
        'APP': {
            'client_id': os.getenv('GITHUB_CLIENT_ID'),
            'secret': os.getenv('GITHUB_CLIENT_SECRET'),
            'key': ''
        },
        'SCOPE': [
            'user',
            'email',
        ],
    }
}

# -------------------------------------------------------------------------
# Email Settings
# -------------------------------------------------------------------------
# In development: Console backend (prints emails to console)
# In production: Configure SMTP server via environment variables
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')

# -------------------------------------------------------------------------
# API Integration Settings
# -------------------------------------------------------------------------
# OpenAI API key for generating word clouds
# Get this from your OpenAI account and set in .env
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# -------------------------------------------------------------------------
# Azure Storage Settings (For Production)
# -------------------------------------------------------------------------
# These settings are used in production for cloud storage
# For development, local storage is used instead (see storage backends above)
AZURE_ACCOUNT_NAME = os.getenv('AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = os.getenv('AZURE_ACCOUNT_KEY')
AZURE_CONTAINER_NAME = os.getenv('AZURE_CONTAINER_NAME', 'wordcloud-images')

# -------------------------------------------------------------------------
# Application-Specific Settings
# -------------------------------------------------------------------------
# Free usage limit for OpenAI API (number of generations)
FREE_OPENAI_USAGE_LIMIT = 3

# -------------------------------------------------------------------------
# API Documentation Settings
# -------------------------------------------------------------------------
# Settings for Swagger/OpenAPI documentation
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
