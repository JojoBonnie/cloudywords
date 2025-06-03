from django.urls import path
from .views import MFASetupView, MFAVerifyView, MFADisableView
# from . import views

urlpatterns = [
    path('mfa/setup/', MFASetupView.as_view(), name='mfa-setup'),
    path('mfa/verify/', MFAVerifyView.as_view(), name='mfa-verify'),
    path('mfa/disable/', MFADisableView.as_view(), name='mfa-disable'),
    # path('github/', views.github_login_redirect, name='github_login'),
    # path('github/callback/', views.github_callback, name='github_callback'),
    # path('check-status/', views.check_auth_status, name='check_auth_status'),
]
