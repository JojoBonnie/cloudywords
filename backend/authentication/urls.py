from django.urls import path
from .views import MFASetupView, MFAVerifyView, MFADisableView

urlpatterns = [
    path('mfa/setup/', MFASetupView.as_view(), name='mfa-setup'),
    path('mfa/verify/', MFAVerifyView.as_view(), name='mfa-verify'),
    path('mfa/disable/', MFADisableView.as_view(), name='mfa-disable'),
]
