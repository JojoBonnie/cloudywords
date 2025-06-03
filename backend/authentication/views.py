import base64
import io
import qrcode
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.util import random_hex
from .serializers import MFAVerifySerializer

# import requests
# import os
# from django.shortcuts import redirect
# from django.contrib.auth import login, authenticate # For Django's built-in user system
# from rest_framework.decorators import api_view, permission_classes
# # from rest_framework.permissions import AllowAny
# import secrets # For generating state parameter securely




class MFASetupView(APIView):
    """
    API view to set up Multi-Factor Authentication for a user.
    
    This endpoint initializes MFA setup by:
    1. Generating a new TOTP device for the user
    2. Creating a QR code for scanning with authenticator apps
    3. Returning the QR code image and secret key
    
    The setup requires a subsequent verification step using MFAVerifyView
    to complete the process and enable MFA on the account.
    
    Permissions:
        - User must be authenticated
    
    HTTP Methods:
        - POST: Initialize MFA setup
    
    Returns:
        - QR code image (base64 encoded)
        - Secret key (for manual entry in authenticator app)
        - Status message
    
    Error Handling:
        - Authentication errors return 401 Unauthorized
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Handle POST request to initialize MFA setup.
        
        Creates a new TOTP device for the user and generates a QR code
        that can be scanned with an authenticator app (like Google Authenticator).
        
        Args:
            request: The HTTP request object containing user information
            
        Returns:
            Response: JSON response with QR code, secret key, and message
        """
        user = request.user
        
        # Delete any existing TOTP devices for this user
        # This ensures we don't have multiple pending setup devices
        TOTPDevice.objects.filter(user=user).delete()
        
        # Create a new TOTP device with a random key
        # The device is initially unconfirmed until verification
        device = TOTPDevice.objects.create(
            user=user,
            name='Default',
            key=random_hex(),  # Generate a random secret key
            confirmed=False    # Will be set to True after verification
        )
        
        # Generate the provisioning URI for the QR code
        # This URI contains the necessary information for authenticator apps
        totp_uri = device.config_url
        
        # Generate QR code using the qrcode library
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        # Create QR code image and convert to base64 for embedding in HTML/JSON
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        # Update user profile to indicate MFA is in setup phase (not yet enabled)
        user.profile.mfa_enabled = False
        user.profile.save()
        
        # Return the QR code, secret key, and setup instructions
        return Response({
            'qr_code': qr_code_base64,  # Base64 encoded QR code image
            'secret_key': device.key,    # Secret key for manual entry
            'message': 'MFA setup initialized. Please verify with a token to complete setup.'
        })


class MFAVerifyView(APIView):
    """
    API view to verify MFA token and complete the MFA setup process.
    
    This endpoint:
    1. Validates the token provided by the user's authenticator app
    2. Marks the TOTP device as confirmed if validation succeeds
    3. Enables MFA on the user's profile
    
    This endpoint should be called after MFASetupView to complete the setup.
    
    Permissions:
        - User must be authenticated
    
    HTTP Methods:
        - POST: Verify token and complete MFA setup
    
    Request Format:
        {
            "token": "123456"  # 6-digit code from authenticator app
        }
    
    Returns:
        - Success or error message
    
    Error Handling:
        - Invalid token returns 400 Bad Request
        - Missing MFA device returns 400 Bad Request
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Handle POST request to verify MFA token and complete setup.
        
        Verifies the token from the user's authenticator app against the
        previously created TOTP device. If successful, enables MFA on the account.
        
        Args:
            request: The HTTP request object containing the token and user
            
        Returns:
            Response: JSON response with success or error message
        """
        user = request.user
        serializer = MFAVerifySerializer(data=request.data)
        
        # Validate the request data using the serializer
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Extract the token from validated data
        token = serializer.validated_data['token']
        
        # Find the user's unconfirmed TOTP device
        device = TOTPDevice.objects.filter(user=user, confirmed=False).first()
        
        # Check if a device exists (user should have initialized setup)
        if not device:
            return Response(
                {'error': 'No MFA device found. Please set up MFA first.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify the token against the device
        if device.verify_token(token):
            # If verified, confirm the device and enable MFA
            device.confirmed = True
            device.save()
            
            # Update user profile to indicate MFA is now enabled
            user.profile.mfa_enabled = True
            user.profile.save()
            
            return Response({'message': 'MFA setup completed successfully.'})
        else:
            # If verification fails, return an error
            return Response(
                {'error': 'Invalid token. Please try again.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class MFADisableView(APIView):
    """
    API view to disable Multi-Factor Authentication for a user.
    
    This endpoint:
    1. Removes all TOTP devices associated with the user
    2. Updates the user's profile to disable MFA
    
    Permissions:
        - User must be authenticated
    
    HTTP Methods:
        - POST: Disable MFA for the authenticated user
    
    Returns:
        - Success message
    
    Security Note:
        - Consider adding additional security measures before allowing
          MFA to be disabled, such as password re-entry or cooldown periods
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Handle POST request to disable MFA.
        
        Removes all TOTP devices for the user and updates their profile
        to indicate that MFA is disabled.
        
        Args:
            request: The HTTP request object containing user information
            
        Returns:
            Response: JSON response with success message
        """
        user = request.user
        
        # Delete all TOTP devices associated with this user
        # This effectively disables MFA since no devices remain for verification
        TOTPDevice.objects.filter(user=user).delete()
        
        # Update user profile to indicate MFA is disabled
        user.profile.mfa_enabled = False
        user.profile.save()
        
        return Response({'message': 'MFA has been disabled successfully.'})

# --- Initiate GitHub Login (Backend Initiated Redirect) ---
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def github_login_redirect(request):
#     """
#     Redirects the user to GitHub for OAuth login.
    
#     This function generates a state parameter to prevent CSRF attacks
#     and redirects the user to GitHub's authorization URL.
    
#     Returns:
#         Redirect response to GitHub's OAuth authorization page
#     """
#     client_id = settings.GITHUB_CLIENT_ID
#     redirect_uri = settings.GITHUB_REDIRECT_URI
#     scope = "read:user user:email" # Request basic user info and email
#     state = secrets.token_urlsafe(32)  # Generate a secure random state parameter
#     request.session['github_oauth_state'] = state

#     github_auth_url = (
#         f"https://github.com/login/oauth/authorize?"
#         f"client_id={client_id}&"
#         f"redirect_uri={redirect_uri}&"
#         f"scope={scope}&"
#         f"state={state}"
#     )
#     return redirect(github_auth_url)

# --- GitHub OAuth Callback ---
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def github_callback(request):
#     """
#     Handles the callback from GitHub after user authorization.
    
#     This function exchanges the authorization code for an access token,
#     retrieves the user's GitHub profile information, and logs them in.
    
#     Returns:
#         Redirect response to the frontend or an error message
#     """
#     code = request.GET.get('code')
#     state = request.GET.get('state')
#      # 1. Verify the state parameter
#     stored_state = request.session.pop('github_oauth_state', None)

#     if not state or state != stored_state:
#         # Potentially a CSRF attack or invalid state
#         return Response({'error': 'State mismatch or missing.'}, status=status.HTTP_400_BAD_REQUEST)

#     if not code:
#         return Response({'error': 'Authorization code not provided.'}, status=status.HTTP_400_BAD_REQUEST)
    
#     client_id = settings.GITHUB_CLIENT_ID
#     client_secret = settings.GITHUB_CLIENT_SECRET
#     redirect_uri = settings.GITHUB_REDIRECT_URI
    
#     # 2. Exchange code for access token
#     token_url = "https://github.com/login/oauth/access_token"
#     token_params = {
#         'client_id': client_id,
#         'client_secret': client_secret,
#         'code': code,
#         'redirect_uri': redirect_uri,
#     }
#     headers = {'Accept': 'application/json'}

#     try:
#         token_response = requests.post(token_url, data=token_params, headers=headers)
#         token_response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
#         token_data = token_response.json()
#         access_token = token_data.get('access_token')

#         if not access_token:
#             return Response({'error': 'Failed to get access token from GitHub.', 'details': token_data}, 
#                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         # 3. Fetch user data using the access token
#         user_info_url = "https://api.github.com/user"
#         user_headers = {'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}
#         user_response = requests.get(user_info_url, headers=user_headers)
#         user_response.raise_for_status()
#         github_user_data = user_response.json()

#         # Get emails (this is a separate endpoint if 'user:email' scope is granted)
#         emails_url = "https://api.github.com/user/emails"
#         emails_response = requests.get(emails_url, headers=user_headers)
#         emails_response.raise_for_status()
#         github_emails = emails_response.json()
        
#         primary_email = next((e['email'] for e in github_emails if e['primary'] and e['verified']), None)
#         if not primary_email:
#             primary_email = next((e['email'] for e in github_emails if e['verified']), None) # Fallback

#         github_id = github_user_data.get('id')
#         username = github_user_data.get('login') # GitHub username
#         name = github_user_data.get('name') or username
#         avatar_url = github_user_data.get('avatar_url')
        
#         # 4. Create/Get User in Django and Log them in
#         # We'll use the GitHub ID as a unique identifier for the user
#         try:
#             # Try to find a user by their GitHub ID
#             # You might want to store github_id in a custom user model or a separate profile model
#             user = User.objects.get(profile__github_id=github_id)
#             # If you don't have a profile model, you might look up by username or email
#             # user = User.objects.get(username=username) # Be careful with username conflicts
#         except User.DoesNotExist:
#             # If user does not exist, create a new one
#             # Ensure username is unique, append ID if necessary
#             base_username = username
#             counter = 1
#             while User.objects.filter(username=username).exists():
#                 username = f"{base_username}{counter}"
#                 counter += 1

#             user = User.objects.create_user(
#                 username=username,
#                 email=primary_email or f'{github_id}@github.com', # Fallback email
#                 password=None # No password for social login users
#             )
#             # Link GitHub ID to the Django user. Best practice is via a custom user model or profile.
#             # For simplicity, let's assume you have a Profile model or add a field to User.
#             # Example with a simple Profile model:
#             # Profile.objects.create(user=user, github_id=github_id, avatar_url=avatar_url)
#             # If you add github_id directly to User model:
#             user.github_id = github_id
#             user.save()


#         # Log the user into Django's authentication system
#         # This will set a session cookie (if SessionAuthentication is used)
#         login(request, user)

#         # IMPORTANT: Redirect to your React frontend after successful login.
#         # This redirect should go to a success page or dashboard in your React app.
#         frontend_success_url = os.environ.get('FRONTEND_SUCCESS_URL', 'http://localhost:3000/dashboard')
#         return redirect(frontend_success_url)

#     except requests.exceptions.RequestException as e:
#         print(f"Error communicating with GitHub: {e}")
#         return Response({'error': f'GitHub API error: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     except Exception as e:
#         print(f"Internal server error during GitHub OAuth: {e}")
#         return Response({'error': f'Internal server error: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#  Django view to check authentication status (e.g., in authentication/views.py)
# @api_view(['GET'])
# @permission_classes([AllowAny]) # Anyone can check, but response varies based on auth
# def check_auth_status(request):
#     return Response({
#         'is_authenticated': request.user.is_authenticated,
#         'username': request.user.username if request.user.is_authenticated else None
#     })