from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Promoter


CREATE_PROMOTER_URL = reverse('user:create-promoter')
ME_URL = reverse('user:me')
RETRIEVE_PROMOTER_URL = reverse(
    'user:promoter', kwargs={'slug': 'test-promoter'}
)
LIST_PROMOTERS_URL = reverse('user:list-promoters')


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
        res = self.client.post(CREATE_PROMOTER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        promoter = Promoter.objects.get(**res.data)
        self.assertTrue(promoter.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_promoter_short_password(self):
        """
        Test that an error is raised if a new promoter has a short password.
        """
        payload = {'email': 'promoter@test.com', 'password': 'test'}
        res = self.client.post(CREATE_PROMOTER_URL, payload)
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
        res = self.client.post(CREATE_PROMOTER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_promoter(self):
        """Test retrieving an promoter."""
        test_promoter = {
            'email': 'promoter@test.com',
            'password': 'testpass',
            'name': 'test promoter',
            'is_verified': True
        }
        create_promoter(**test_promoter)
        res = self.client.get(RETRIEVE_PROMOTER_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('name', res.data)

    def test_retrieve_promoter_non_existent(self):
        """Test retrieving an promoter that doesn't exist."""
        res = self.client.get(RETRIEVE_PROMOTER_URL)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_promoter_hidden_fields(self):
        """Test that certain fields are hidden when retrieving an promoter."""
        test_promoter = {
            'email': 'promoter@test.com',
            'password': 'testpass',
            'name': 'test promoter',
            'phone': '+447546103437'
        }
        create_promoter(**test_promoter)
        res = self.client.get(RETRIEVE_PROMOTER_URL)
        self.assertNotIn('email', res.data)
        self.assertNotIn('password', res.data)
        self.assertNotIn('phone', res.data)

    def test_list_promoters(self):
        """Test that promoters are listed."""
        test_promoter_1 = {
            'email': 'promoter1@test.com',
            'password': 'testpass',
            'name': 'test promoter 1',
            'is_verified': True,
            'phone': '+447546103437'
        }
        test_promoter_2 = {
            'email': 'promoter2@test.com',
            'password': 'testpass',
            'name': 'test promoter 2',
            'is_verified': True,
            'phone': '+447546103438'
        }
        create_promoter(**test_promoter_1)
        create_promoter(**test_promoter_2)
        res = self.client.get(LIST_PROMOTERS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_list_promoters_not_verified(self):
        """Test that unverified promoters are not listed."""
        test_promoter_1 = {
            'email': 'promoter1@test.com',
            'password': 'testpass',
            'name': 'test promoter 1',
            'is_verified': True,
            'phone': '+447546103437'
        }
        test_promoter_2 = {
            'email': 'promoter2@test.com',
            'password': 'testpass',
            'name': 'test promoter 2',
            'is_verified': False,
            'phone': '+447546103438'
        }
        create_promoter(**test_promoter_1)
        create_promoter(**test_promoter_2)
        res = self.client.get(LIST_PROMOTERS_URL)
        self.assertEqual(len(res.data), 1)
        name = res.data[0]['name']
        self.assertEqual(name, 'test promoter 1')


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
