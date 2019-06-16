from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
     PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField


def signup_check(email, password):
    """Helper function to check emails and passwords."""
    if not email:
        raise ValueError('Enter an email address.')
    if not password:
        raise ValueError('Enter a password.')


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """Creates and saves a new user."""
        signup_check(email, password)
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class ArtistManager(BaseUserManager):

    def create_artist(self, email, password, name, **extra_fields):
        """Creates and saves a new artist."""
        signup_check(email, password)
        if not name:
            raise ValueError('Enter a name.')
        artist = Artist.objects.create(
            email=self.normalize_email(email), name=name, **extra_fields
        )
        artist.set_password(password)
        artist.is_artist = True
        artist.save(using=self._db)
        return artist


class PromoterManager(BaseUserManager):

    def create_promoter(self, email, password, name, **extra_fields):
        """Creates and saves a new promoter."""
        signup_check(email, password)
        if not name:
            raise ValueError('Enter a name.')
        promoter = Promoter.objects.create(
            email=self.normalize_email(email), name=name, **extra_fields
        )
        promoter.set_password(password)
        promoter.is_promoter = True
        promoter.save(using=self._db)
        return promoter


# class VenueManager(BaseUserManager):


# class EventManager(BaseUserManager):


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses an email address to log in.
    Supports the 'basic' user type as well as artists and promoters.
    """
    # Main
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    name = models.CharField(max_length=255)

    # Contact
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    phone = PhoneNumberField(blank=True)
    soundcloud = models.URLField(blank=True)
    spotify = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    website = models.URLField(blank=True)
    youtube = models.URLField(blank=True)

    # Groups
    is_artist = models.BooleanField(default=False)
    is_promoter = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = UserManager()

    def __str__(self):
        return self.name


class Artist(User, PermissionsMixin):
    """Artist model. (better description needed)"""
    description = models.CharField(max_length=1000, blank=True)
    points = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = ArtistManager()

    def __str__(self):
        return self.name


class Promoter(User, PermissionsMixin):
    """Promoter model. (better description needed)"""
    description = models.CharField(max_length=1000, blank=True)
    is_verified = models.BooleanField(default=False)
    points = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = PromoterManager()

    def __str__(self):
        return self.name


class Venue(models.Model):
    """Venue model. (better description needed)"""
    address = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Event(models.Model):
    """Event model. (better description needed)"""
    artists = models.ManyToManyField(
        'Artist', related_name='events'
    )
    description = models.CharField(max_length=1000)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    name = models.CharField(max_length=255)
    promoter = models.ForeignKey(
        'Promoter', on_delete=models.CASCADE, related_name='events'
    )
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    venue = models.ForeignKey(
        'Venue', on_delete=models.CASCADE, related_name='events'
    )

    def __str__(self):
        return self.name


# class Ticket(models.Model):
