from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """Helper function to create a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the user API (public)."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        """Test creating a new user."""
        payload = {
            'email': 'test@test.com',
            'password': 'testpass',
            'name': 'test user',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_user_short_password(self):
        """Test that an error is raised if a new user has a short password."""
        payload = {'email': 'test@test.com', 'password': 'test'}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_user_already_exists(self):
        """
        Test that an error is raised if a new user tries to
        use an email address that has already been registered.
        """
        payload = {'email': 'test@test.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
