from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom adapter to handle AllAuth customizations for the Word Cloud project.
    
    This adapter overrides Django AllAuth's default behavior to integrate
    with our React frontend, particularly for email confirmations.
    
    For contributors:
    - This adapter ensures email confirmation links point to our frontend instead of Django's default pages
    - In production, update the base URL to match your deployed frontend domain
    """
    
    def get_email_confirmation_url(self, request, emailconfirmation):
        """
        Generate the URL for email confirmation.
        
        This method overrides the default Django AllAuth behavior to redirect
        users to our React frontend for completing email confirmation.
        
        Args:
            request: The HTTP request object
            emailconfirmation: The EmailConfirmation instance containing the verification key
            
        Returns:
            str: Frontend URL with the confirmation key as a parameter
            
        Note:
            For production deployment, this URL should be configured via 
            environment variables rather than hardcoded.
        """
        # For development, point to frontend confirmation page
        # TODO: In production, get this URL from environment variables
        return f"http://localhost:3000/confirm-email/{emailconfirmation.key}"
