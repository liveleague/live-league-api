from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """Creates and saves a new user."""
        if not email:
            raise ValueError('Enter an email address.')
        if not password:
            raise ValueError('Enter a password.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        contacts = Contact.objects.create(user=user)
        contacts.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    def create_artist(self, email, password):
        """Creates and saves a new artist."""
        user = self.create_user(email, password)
        user.is_artist = True
        user.save(using=self._db)
        artist = Artist.objects.create(points=0, user=user)
        artist.save(using=self._db)

        return artist

    def create_promoter(self, email, password):
        """Creates and saves a new promoter."""
        user = self.create_user(email, password)
        user.is_promoter = True
        user.save(using=self._db)
        promoter = Promoter.objects.create(user=user)
        promoter.save(using=self._db)

        return promoter


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses an email address to log in.
    Supports the 'basic' user type as well as artists and promoters.
    """
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_artist = models.BooleanField(default=False)
    is_promoter = models.BooleanField(default=False)
    name = models.CharField(max_length=255)

    objects = UserManager()
    USERNAME_FIELD = 'email'


class Contact(models.Model):
    """Collection of external links belonging to the user."""
    facebook = models.URLField()
    instagram = models.URLField()
    phone = PhoneNumberField(blank=True)
    soundcloud = models.URLField()
    spotify = models.URLField()
    twitter = models.URLField()
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contacts'
    )
    website = models.URLField()
    youtube = models.URLField()


class Artist(models.Model):
    """Artist model. (better description needed)"""
    events = models.ManyToManyField('Event', related_name='artists')
    points = models.IntegerField()
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='artist'
    )


class Promoter(models.Model):
    """Promoter model. (better description needed)"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='promoter'
    )
    is_verified = models.BooleanField(default=False)


class Venue(models.Model):
    """Venue model. (better description needed)"""
    address = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Event(models.Model):
    """Event model. (better description needed)"""
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
