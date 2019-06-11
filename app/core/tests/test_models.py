import pytz
from datetime import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class UserManagerTests(TestCase):

    def test_create_user(self):
        """Test creating a new user."""
        email = 'test@test.com'
        password = 'testpass'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_email_normalized(self):
        """Test that the email address for a new user is normalized."""
        email = 'test@TEST.com'
        user = get_user_model().objects.create_user(
            email=email,
            password='testpass'
        )
        self.assertEqual(user.email, email.lower())

    def test_create_user_without_email(self):
        """Test that an error is raised if a new user has no email address."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testpass')

    def test_create_user_without_password(self):
        """Test that an error is raised if a new user has no password."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('test@test.com', None)

    def test_create_superuser(self):
        """Test creating a new superuser."""
        user = get_user_model().objects.create_superuser(
            email='test@test.com',
            password='testpass'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_artist(self):
        """Test creating a new artist."""
        artist = get_user_model().objects.create_artist(
            email='test@test.com',
            password='testpass'
        )
        self.assertTrue(artist.user.is_artist)

    def test_create_promoter(self):
        """Test creating a new promoter."""
        promoter = get_user_model().objects.create_promoter(
            email='test@test.com',
            password='testpass'
        )
        self.assertTrue(promoter.user.is_promoter)


class StringRepresentationTests(TestCase):

    def test_str_venue(self):
        """Test the string representation of the Venue model."""
        venue = models.Venue.objects.create(name='test venue')
        self.assertEqual(str(venue), venue.name)

    def test_str_event(self):
        """Test the string representation of the Event model."""
        event = models.Event.objects.create(
            end_time=datetime(
                2020, 1, 1, 2, 0, 0, 0
            ).replace(tzinfo=pytz.utc),
            start_time=datetime(
                2019, 12, 31, 19, 0, 0, 0
            ).replace(tzinfo=pytz.utc),
            name='test event',
            promoter=get_user_model().objects.create_promoter(
                email='test@test.com',
                password='testpass'
            ),
            venue=models.Venue.objects.create(name='test venue')
        )
        self.assertEqual(str(event), event.name)
