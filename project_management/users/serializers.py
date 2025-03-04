from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
from .utils import send_verification_email


class RegisterSerializer(serializers.ModelSerializer):
    """Handles user registration and email verification."""
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Creates a user and sends an email verification."""
        user = CustomUser.objects.create_user(**validated_data)
        user.is_active = False  # User cannot log in until verified
        user.save()

        # Send verification email
        send_verification_email(email=user.email, verification_code=user.verification_code)
        return user

class VerifyEmailSerializer(serializers.Serializer):
    """Handles email verification."""
    email = serializers.EmailField()
    verification_code = serializers.UUIDField()

    def validate(self, data):
        """Checks if email and verification code are correct."""
        try:
            user = CustomUser.objects.get(email=data['email'], verification_code=data['verification_code'])
            if user.is_verified:
                raise serializers.ValidationError("User is already verified.")
            user.is_verified = True
            user.is_active = True  # Activate user
            user.save()
            return user
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid email or verification code.")

class LoginSerializer(serializers.Serializer):
    """Handles user login."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Authenticate user and start session."""
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        if not user.is_verified:
            raise serializers.ValidationError("Email not verified.")
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    """Fetches authenticated user details."""
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'is_verified')
