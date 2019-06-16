from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Artist


CREATE_ARTIST_URL = reverse('user:create-artist')
ME_URL = reverse('user:me')


def create_artist(**params):
    """Helper function to create a new artist."""
    return Artist.objects.create_artist(**params)


class PublicArtistApiTests(TestCase):
    """Test the artist API (public)."""

    def setUp(self):
        self.client = APIClient()

    def test_create_artist(self):
        """Test creating a new artist."""
        payload = {
            'email': 'artist@test.com',
            'password': 'testpass',
            'name': 'test artist',
        }
        res = self.client.post(CREATE_ARTIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        artist = Artist.objects.get(**res.data)
        self.assertTrue(artist.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_artist_short_password(self):
        """
        Test that an error is raised if a new artist has a short password.
        """
        payload = {'email': 'artist@test.com', 'password': 'test'}
        res = self.client.post(CREATE_ARTIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        artist_exists = Artist.objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(artist_exists)

    def test_create_artist_already_exists(self):
        """
        Test that an error is raised if a new artist tries to
        use an email address that has already been registered.
        """
        payload = {
            'email': 'artist@test.com',
            'password': 'testpass',
            'name': 'test artist'
        }
        create_artist(**payload)
        res = self.client.post(CREATE_ARTIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateArtistApiTests(TestCase):
    """Test the artist API (private)."""

    def setUp(self):
        self.artist = create_artist(
            email='artist@test.com',
            password='testpass',
            name='test artist',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.artist)

    def test_retrieve_profile_success(self):
        """Test retrieving the profile of a logged in artist."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.artist.email,
            'name': self.artist.name,
            'description': self.artist.description,
            'points': self.artist.points,
            'facebook': self.artist.facebook,
            'instagram': self.artist.instagram,
            'phone': self.artist.phone,
            'soundcloud': self.artist.soundcloud,
            'spotify': self.artist.spotify,
            'twitter': self.artist.twitter,
            'website': self.artist.website,
            'youtube': self.artist.youtube
        })

    def test_update_artist_profile(self):
        """Test updating the artist profile of an authenticated artist."""
        payload = {'name': 'new name', 'password': 'newpass'}
        res = self.client.patch(ME_URL, payload)
        self.artist.refresh_from_db()
        self.assertEqual(self.artist.name, payload['name'])
        self.assertTrue(self.artist.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
