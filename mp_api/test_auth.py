from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from profiles.models import Profile  # Assuming you have a Profile model


class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('rest_login')
        self.tracks_url = reverse('track-list')
        self.user = User.objects.create_user(
            username='testuser', password='testpass123')
        self.profile = Profile.objects.get(owner=self.user)
        self.profile.role = 'composer'  # Assuming 'composer' is a valid role
        self.profile.save()

    def test_login_and_access_protected_route(self):
        # Attempt to access protected route without login
        response = self.client.get(self.tracks_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Login
        login_data = {'username': 'testuser', 'password': 'testpass123'}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

        # Access protected route with token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {
                                response.data['access']}")
        response = self.client.get(self.tracks_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test with a non-composer user
        non_composer = User.objects.create_user(
            username='noncomposer', password='testpass123')
        non_composer_profile = Profile.objects.get(owner=non_composer)
        # Assuming 'listener' is a role without access
        non_composer_profile.role = 'listener'
        non_composer_profile.save()

        login_data = {'username': 'noncomposer', 'password': 'testpass123'}
        response = self.client.post(self.login_url, login_data)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {
                                response.data['access']}")
        response = self.client.get(self.tracks_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
