from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Promoter


CREATE_promoter_URL = reverse('user:create-promoter')
ME_URL = reverse('user:me')


def create_promoter(**params):
    """Helper function to create a new promoter."""
    return Promoter.objects.create_promoter(**params)


class PublicpromoterApiTests(TestCase):
    """Test the promoter API (public)."""

    def setUp(self):
        self.client = APIClient()

    def test_create_promoter(self):
        """Test creating a new promoter."""
        payload = {
            'email': 'promoter@test.com',
            'password': 'testpass',
            'name': 'test promoter',
        }
        res = self.client.post(CREATE_promoter_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        promoter = Promoter.objects.get(**res.data)
        self.assertTrue(promoter.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_promoter_short_password(self):
        """
        Test that an error is raised if a new promoter has a short password.
        """
        payload = {'email': 'promoter@test.com', 'password': 'test'}
        res = self.client.post(CREATE_promoter_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        promoter_exists = Promoter.objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(promoter_exists)

    def test_create_promoter_already_exists(self):
        """
        Test that an error is raised if a new promoter tries to
        use an email address that has already been registered.
        """
        payload = {
            'email': 'promoter@test.com',
            'password': 'testpass',
            'name': 'test promoter'
        }
        create_promoter(**payload)
        res = self.client.post(CREATE_promoter_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivatepromoterApiTests(TestCase):
    """Test the promoter API (private)."""

    def setUp(self):
        self.promoter = create_promoter(
            email='promoter@test.com',
            password='testpass',
            name='test promoter',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.promoter)

    def test_retrieve_profile_success(self):
        """Test retrieving the profile of a logged in promoter."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.promoter.email,
            'name': self.promoter.name,
            'description': self.promoter.description,
            'is_verified': self.promoter.is_verified,
            'facebook': self.promoter.facebook,
            'instagram': self.promoter.instagram,
            'phone': self.promoter.phone,
            'soundcloud': self.promoter.soundcloud,
            'spotify': self.promoter.spotify,
            'twitter': self.promoter.twitter,
            'website': self.promoter.website,
            'youtube': self.promoter.youtube
        })

    def test_update_promoter_profile(self):
        """Test updating the promoter profile of an authenticated promoter."""
        payload = {'name': 'new name', 'password': 'newpass'}
        res = self.client.patch(ME_URL, payload)
        self.promoter.refresh_from_db()
        self.assertEqual(self.promoter.name, payload['name'])
        self.assertTrue(self.promoter.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
