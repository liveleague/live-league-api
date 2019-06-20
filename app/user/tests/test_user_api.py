from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


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
        payload = {
            'email': 'test@test.com',
            'password': 'testpass',
            'name': 'test user'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token(self):
        """Test that a token is created for the new user."""
        payload = {
            'email': 'test@test.com',
            'password': 'testpass',
            'name': 'test user'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """
        Test that a token is not created if invalid credentials
        are given by the new user.
        """
        create_user(
            email='test@test.com',
            password='testpass',
            name='test user'
        )
        payload = {
            'email': 'test@test.com',
            'password': 'wrong',
            'name': 'test user'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that a token is not created if the user doesn't exist."""
        payload = {'email': 'test@test.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """
        Test that an email address and password
        are required to create a token.
        """
        res = self.client.post(TOKEN_URL, {'email': 'test', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test the user API (private)."""

    def setUp(self):
        self.user = create_user(
            email='test@test.com',
            password='testpass',
            name='test user',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving the profile of a logged in user."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'name': self.user.name,
            'facebook': self.user.facebook,
            'instagram': self.user.instagram,
            'phone': self.user.phone,
            'soundcloud': self.user.soundcloud,
            'spotify': self.user.spotify,
            'twitter': self.user.twitter,
            'website': self.user.website,
            'youtube': self.user.youtube
        })

    def test_post_me_not_allowed(self):
        """Test that the POST method is not allowed on the 'me' URL."""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile of an authenticated user."""
        payload = {'name': 'new name', 'password': 'newpass'}
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
