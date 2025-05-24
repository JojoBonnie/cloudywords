from rest_framework import serializers


class MFAVerifySerializer(serializers.Serializer):
    """Serializer for MFA token verification"""
    token = serializers.CharField(max_length=6, min_length=6)
