from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import time
from django.conf import settings


class AuthenticationTest(APITestCase):
    def setUp(self):
        """Set up test user and login URL"""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.login_url = reverse("rest_login")
        self.logout_url = reverse("rest_logout")
        self.protected_url = reverse("track-list")  # Adjust for a real route

    def test_login_success(self):
        """Test user can log in and get a token."""
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "testpass123"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)  # JWT token must be in response

    def test_login_invalid_credentials(self):
        """Test login fails with incorrect password."""
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_access_protected_route_without_token(self):
        """Test that an unauthenticated user cannot access a protected route."""
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_expiry(self):
        """Test if the access token expires correctly."""
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "testpass123"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data["access"]

        # Set auth headers
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        # Get token expiration time dynamically
        expiry_seconds = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds(
        )

        # Wait slightly beyond expiry (ensure full expiration)
        time.sleep(expiry_seconds + 2)

        # Try accessing the protected route after expiry
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_route_with_valid_token(self):
        """Test that an authenticated user can access a protected route."""
        # Login and get token
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "testpass123"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data["access"]

        # Set auth headers
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        # Try accessing the protected route
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        """Test that a user can log out successfully."""
        # Login first
        login_response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "testpass123"
        })
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # Get the access token
        access_token = login_response.data['access']

        # Set the token in the Authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Logout
        logout_response = self.client.post(self.logout_url)
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)

        # Try accessing protected route after logout
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_without_token(self):
        """Test logout without being authenticated."""
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
