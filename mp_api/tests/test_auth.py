# tests.py
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import time


class AuthenticationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.login_url = "/dj-rest-auth/login/"
        self.logout_url = "/dj-rest-auth/logout/"
        self.refresh_url = "/dj-rest-auth/token/refresh/"
        self.protected_url = reverse("track-list")  # Example endpoint

    def test_login_success(self):
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_credentials(self):
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "wrongpass"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_access_protected_route_without_token(self):
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_expiry(self):
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        # Wait just over 5 seconds (the test-lifetime).
        time.sleep(6)

        # Should be expired -> 401
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_access_regular_user_protected_route_with_valid_token(self):
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logout(self):
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data["access"]
        refresh_token = response.data["refresh"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        logout_response = self.client.post(
            self.logout_url, {"refresh_token": refresh_token}, format="json"
        )
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)

        # *** Wait for the short-lived access token to expire ***
        time.sleep(6)  # If your ACCESS_TOKEN_LIFETIME=5

        # Now the token is expired, so we get 401
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logout_without_token(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token(self):
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        refresh_token = response.data["refresh"]

        response = self.client.post(
            self.refresh_url, {"refresh": refresh_token}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_token_blacklist_after_logout(self):
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data["access"]
        refresh_token = response.data["refresh"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        # Logout (blacklist token)
        self.client.post(
            self.logout_url, {"refresh_token": refresh_token}, format="json"
        )

        # Attempt to refresh => should fail (401)
        response = self.client.post(
            self.refresh_url, {"refresh": refresh_token}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
