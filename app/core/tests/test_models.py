import pytz
from datetime import date, time

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class UserManagerTests(TestCase):

    def test_create_user(self):
        """Test creating a new user."""
        email = 'test@test.com'
        password = 'testpass'
        name = 'test user'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name=name
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_email_normalized(self):
        """Test that the email address for a new user is normalized."""
        email = 'test@TEST.com'
        user = get_user_model().objects.create_user(
            email=email,
            password='testpass',
            name='test user'
        )
        self.assertEqual(user.email, email.lower())

    def test_create_user_without_email(self):
        """Test that an error is raised if a new user has no email address."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testpass', 'test user')

    def test_create_user_without_password(self):
        """Test that an error is raised if a new user has no password."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                'test@test.com', None, name='test user'
            )

    def test_create_superuser(self):
        """Test creating a new superuser."""
        user = get_user_model().objects.create_superuser(
            email='test@test.com',
            password='testpass',
            name='test user'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class ArtistManagerTests(TestCase):

    def test_create_artist(self):
        """Test creating a new artist."""
        email = 'artist@test.com'
        password = 'testpass'
        artist = models.Artist.objects.create_artist(
            email=email,
            password=password,
            name='test artist'
        )
        self.assertEqual(artist.email, email)
        self.assertTrue(artist.check_password(password))

    def test_create_artist_email_normalized(self):
        """Test that the email address for a new artist is normalized."""
        email = 'artist@TEST.com'
        artist = models.Artist.objects.create_artist(
            email=email,
            password='testpass',
            name='test artist'
        )
        self.assertEqual(artist.email, email.lower())

    def test_create_artist_without_email(self):
        """
        Test that an error is raised if a new artist has no email address.
        """
        with self.assertRaises(ValueError):
            models.Artist.objects.create_artist(
                None, 'testpass', 'test artist'
            )

    def test_create_artist_without_password(self):
        """Test that an error is raised if a new artist has no password."""
        with self.assertRaises(ValueError):
            models.Artist.objects.create_artist(
                'artist@test.com', None, 'test artist'
            )

    def test_create_artist_without_name(self):
        """Test that an error is raised if a new artist has no name."""
        with self.assertRaises(ValueError):
            models.Artist.objects.create_artist(
                'artist@test.com', 'testpass', None
            )


class PromoterManagerTests(TestCase):

    def test_create_promoter(self):
        """Test creating a new promoter."""
        email = 'promoter@test.com'
        password = 'testpass'
        promoter = models.Promoter.objects.create_promoter(
            email=email,
            password=password,
            name='test promoter'
        )
        self.assertEqual(promoter.email, email)
        self.assertTrue(promoter.check_password(password))

    def test_create_promoter_email_normalized(self):
        """Test that the email address for a new promoter is normalized."""
        email = 'promoter@TEST.com'
        promoter = models.Promoter.objects.create_promoter(
            email=email,
            password='testpass',
            name='test promoter'
        )
        self.assertEqual(promoter.email, email.lower())

    def test_create_promoter_without_email(self):
        """
        Test that an error is raised if a new promoter has no email address.
        """
        with self.assertRaises(ValueError):
            models.Promoter.objects.create_promoter(
                None, 'testpass', 'test promoter'
            )

    def test_create_promoter_without_password(self):
        """Test that an error is raised if a new promoter has no password."""
        with self.assertRaises(ValueError):
            models.Promoter.objects.create_promoter(
                'promoter@test.com', None, 'test promoter'
            )

    def test_create_promoter_without_name(self):
        """Test that an error is raised if a new promoter has no name."""
        with self.assertRaises(ValueError):
            models.Promoter.objects.create_promoter(
                'promoter@test.com', 'testpass', None
            )


class StringRepresentationTests(TestCase):

    def test_str_user(self):
        """Test the string representation of the User model."""
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass',
            name='test user'
        )
        self.assertEqual(str(user), user.name)

    def test_str_artist(self):
        """Test the string representation of the Artist model."""
        artist = models.Artist.objects.create_artist(
            email='artist@test.com',
            password='testpass',
            name='test artist'
        )
        self.assertEqual(str(artist), artist.name)

    def test_str_promoter(self):
        """Test the string representation of the Promoter model."""
        promoter = models.Promoter.objects.create_promoter(
            email='promoter@test.com',
            password='testpass',
            name='test promoter'
        )
        self.assertEqual(str(promoter), promoter.name)

    def test_str_venue(self):
        """Test the string representation of the Venue model."""
        venue = models.Venue.objects.create(name='test venue')
        self.assertEqual(str(venue), venue.name)

    def test_str_event(self):
        """Test the string representation of the Event model."""
        event = models.Event.objects.create(
            end_date=datetime.date(2020, 1, 1).replace(tzinfo=pytz.utc),
            end_time=datetime.time(2, 0, 0).replace(tzinfo=pytz.utc),
            start_date=datetime.date(2019, 12, 31).replace(tzinfo=pytz.utc),
            start_time=datetime.time(20, 0, 0).replace(tzinfo=pytz.utc),
            name='test event',
            promoter=models.Promoter.objects.create_promoter(
                email='promoter@test.com',
                password='testpass',
                name='test promoter'
            ),
            venue=models.Venue.objects.create(name='test venue')
        )
        self.assertEqual(str(event), event.name)
