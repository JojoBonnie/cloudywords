import base64
import io
import qrcode
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.util import random_hex
from .serializers import MFAVerifySerializer


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
