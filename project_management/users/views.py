import logging
from django.contrib.auth import login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import (
    RegisterSerializer,
    VerifyEmailSerializer,
    LoginSerializer,
    UserProfileSerializer,
)
from icecream import ic

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    """Registers a user and sends an email verification."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        logger.info("New user registration attempt.")
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("User registered successfully. Verification email sent.")
            return Response(
                {"message": "User registered. Check email for verification."},
                status=status.HTTP_201_CREATED,
            )

        logger.warning("User registration failed: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    """Verifies user email and activates account."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            logger.info("User email verified successfully.")
            return Response(
                {"message": "Email verified successfully!"}, status=status.HTTP_200_OK
            )

        logger.warning("Email verification failed: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Logs in a user and starts a session."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        logger.info("User login attempt.")
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            logger.info(f"User {user.email} logged in successfully.")
            response = Response(
                {"message": "Login successful"}, status=status.HTTP_200_OK
            )
            response.set_cookie(
                key="sessionid", value=request.session.session_key, httponly=True
            )
            return response
        logger.warning("Login failed: Invalid credentials.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """Logs out user and destroys session."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logger.info(f"User {request.user.email} logged out.")
        logout(request)
        return Response(
            {"message": "Logged out successfully"}, status=status.HTTP_200_OK
        )


class UserProfileView(APIView):
    """Fetches authenticated user's details."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        logger.info(f"User {request.user.email} fetched profile details.")
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
