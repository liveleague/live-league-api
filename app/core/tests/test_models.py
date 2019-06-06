from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


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
        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(None, 'testpass')

    def test_create_user_invalid_email(self):
        """
        Test that an error is raised if a new user
        has an invalid email address.
        """
        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user('test', 'testpass')

    def test_create_user_without_password(self):
        """Test that an error is raised if a new user has no password."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('test@test.com', None)

    def test_create_user_with_short_password(self):
        """Test that an error is raised if a new user has a short password."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('test@test.com', 'test')
