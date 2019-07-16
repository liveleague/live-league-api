import uuid
import os

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
     PermissionsMixin
from django.core.mail import send_mail
from phonenumber_field.modelfields import PhoneNumberField


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/recipe/', filename)


def signup_check(email, password, name):
    """Helper function to check emails and passwords."""
    if not email:
        raise ValueError('Enter an email address.')
    if not password:
        raise ValueError('Enter a password.')
    if not name:
        raise ValueError('Enter a name.')


class UserManager(BaseUserManager):

    def create_user(self, email, password, name, **extra_fields):
        """Creates and saves a new user."""
        signup_check(email, name, password)
        user = self.model(
            email=self.normalize_email(email), name=name, **extra_fields
        )
        user.set_password(password)
        user.slug = slugify(name)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """Creates and saves a new superuser."""
        user = self.create_user(email, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class ArtistManager(BaseUserManager):

    def create_artist(self, email, password, name, **extra_fields):
        """Creates and saves a new artist."""
        signup_check(email, name, password)
        artist = Artist.objects.create(
            email=self.normalize_email(email), name=name, **extra_fields
        )
        artist.set_password(password)
        artist.is_artist = True
        artist.slug = slugify(name)
        artist.save(using=self._db)
        return artist


class PromoterManager(BaseUserManager):

    def create_promoter(self, email, password, name, phone, **extra_fields):
        """Creates and saves a new promoter."""
        signup_check(email, name, password)
        if not phone:
            raise ValueError('Enter a phone number.')
        promoter = Promoter.objects.create(
            email=self.normalize_email(email),
            name=name,
            phone=phone,
            **extra_fields
        )
        promoter.set_password(password)
        promoter.is_promoter = True
        promoter.slug = slugify(name)
        promoter.save(using=self._db)
        return promoter


class MessageManager(BaseUserManager):

    def create_message(self, subject, text, **extra_fields):
        """Creates and saves a new message."""
        if not subject:
            raise ValueError('Enter a subject.')
        if not text:
            raise ValueError('Enter some text.')
        message = Message.objects.create(
            subject=subject,
            text=text,
            **extra_fields
        )
        message.save(using=self._db)
        return message


class ReadFlagManager(BaseUserManager):

    def create_readflag(self, message, recipient, **extra_fields):
        """Creates and saves a new read flag."""
        if not message:
            raise ValueError('Enter a message.')
        if not recipient:
            raise ValueError('Enter a recipient.')
        readflag = ReadFlag.objects.create(
            message=message,
            recipient=recipient,
            **extra_fields
        )
        readflag.save(using=self._db)
        return readflag


class VenueManager(BaseUserManager):

    def create_venue(self, address_line1, address_zip, name, **extra_fields):
        """Creates and saves a new venue."""
        if not address_line1:
            raise ValueError("Enter the first line of the venue's address.")
        if not address_zip:
            raise ValueError("Enter the venue's postcode.")
        if not name:
            raise ValueError('Enter a name.')
        venue = Venue.objects.get_or_create(
            address_line1=address_line1,
            address_zip=address_zip,
            name=name,
            **extra_fields
        )
        venue[0].slug = slugify(name)
        venue[0].save(using=self._db)
        return venue[0]


class EventManager(BaseUserManager):

    def create_event(self, end_date, end_time, name,
                     start_date, start_time, venue, **extra_fields):
        """Creates and saves a new event."""
        if not end_date:
            raise ValueError('Enter an end date.')
        if not end_time:
            raise ValueError('Enter an end time.')
        if not name:
            raise ValueError('Enter a name.')
        if not start_date:
            raise ValueError('Enter a start date.')
        if not start_time:
            raise ValueError('Enter a start time.')
        if not venue:
            raise ValueError('Enter a venue.')
        event = Event.objects.get_or_create(
            end_date=end_date,
            end_time=end_time,
            name=name,
            start_date=start_date,
            start_time=start_time,
            venue=venue,
            **extra_fields
        )
        event[0].save(using=self._db)
        return event[0]


class TallyManager(BaseUserManager):

    def create_tally(self, artist, event, **extra_fields):
        """Creates and saves a new tally."""
        if not artist:
            raise ValueError('Enter an artist.')
        if not event:
            raise ValueError('Enter an event.')
        tally = Tally.objects.get_or_create(
            artist=artist,
            event=event,
            **extra_fields
        )
        tally[0].slug = slugify(str(artist) + '-' + str(event.pk))
        tally[0].save(using=self._db)
        return tally[0]


class TicketTypeManager(BaseUserManager):

    def create_ticket_type(self, event, name, price, **extra_fields):
        """Creates and saves a new ticket type."""
        if not event:
            raise ValueError('Enter an event.')
        if not name:
            raise ValueError('Enter a name.')
        if not price:
            raise ValueError('Enter a price.')
        ticket_type = TicketType.objects.get_or_create(
            event=event,
            name=name,
            price=price,
            **extra_fields
        )
        ticket_type[0].slug = slugify(name + '-' + str(event.pk))
        ticket_type[0].save(using=self._db)
        return ticket_type[0]


class TicketManager(BaseUserManager):

    def create_ticket(self, owner, ticket_type, **extra_fields):
        """Creates and saves a new ticket."""
        if not owner:
            raise ValueError('Enter an owner.')
        if not ticket_type:
            raise ValueError('Enter a ticket type.')
        if ticket_type.tickets_remaining >= 1:
            ticket_type.tickets_remaining -= 1
            ticket = Ticket.objects.create(
                owner=owner,
                ticket_type=ticket_type,
                **extra_fields
            )
            ticket_type.save(using=self._db)
            ticket.save(using=self._db)
        else:
            raise ValueError(
                'Enter a ticket type that still has tickets remaining.'
            )
        return ticket


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses an email address to log in.
    Supports the 'basic' user type as well as artists and promoters.
    """
    # Main
    email = models.EmailField(max_length=255, unique=True)
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    # Billing
    address_city = models.CharField(max_length=255, blank=True)
    address_country = models.CharField(max_length=255, blank=True)
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    address_state = models.CharField(max_length=255, blank=True)
    address_zip = models.CharField(max_length=255, blank=True)

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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = ArtistManager()

    def __str__(self):
        return self.name

    def total_events(self):
        """Count the number of events featuring this artist."""
        return Tally.objects.filter(artist=self).count()

    def total_points(self):
        """Count the number of votes for this artist."""
        return Ticket.objects.filter(vote__artist=self).count()


class Promoter(User, PermissionsMixin):
    """Promoter model. (better description needed)"""
    description = models.CharField(max_length=1000, blank=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']
    objects = PromoterManager()

    def __str__(self):
        return self.name


class Message(models.Model):
    """
    Message model.
    Messages are 'sent' once read flags are created.
    Can be sent by a user or generated by the system (i.e. no sender).
    """
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    sender = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='messages', null=True
    )
    subject = models.CharField(max_length=255)
    text = models.CharField(max_length=1000)

    REQUIRED_FIELDS = ['subject', 'text']

    objects = MessageManager()

    def __str__(self):
        return self.subject


class ReadFlag(models.Model):
    """
    ReadFlag model.
    Every time a message is read by a user, they are added to 'opened_by'.
    """
    message = models.ForeignKey(
        'Message', on_delete=models.CASCADE, related_name='readflags'
    )
    opened = models.BooleanField(default=False)
    recipient = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='readflags'
    )

    REQUIRED_FIELDS = ['message', 'recipient']

    objects = ReadFlagManager()


class Venue(models.Model):
    """Venue model. (better description needed)"""
    address_city = models.CharField(max_length=255, blank=True)
    address_country = models.CharField(max_length=255, blank=True)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    address_state = models.CharField(max_length=255, blank=True)
    address_zip = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    REQUIRED_FIELDS = ['address_line1', 'address_zip', 'name']
    objects = VenueManager()

    def __str__(self):
        return self.name


class Event(models.Model):
    """Event model. (better description needed)"""
    description = models.CharField(max_length=1000)
    end_date = models.DateField()
    end_time = models.TimeField()
    name = models.CharField(max_length=255)
    promoter = models.ForeignKey(
        'Promoter', on_delete=models.CASCADE, related_name='events'
    )
    start_date = models.DateField()
    start_time = models.TimeField()
    venue = models.ForeignKey(
        'Venue', on_delete=models.CASCADE, related_name='events'
    )

    REQUIRED_FIELDS = [
        'end_date', 'end_time', 'name', 'start_date', 'start_time', 'venue'
    ]
    objects = EventManager()

    def __str__(self):
        return self.name


class Tally(models.Model):
    """Tally model. (better description needed)"""
    artist = models.ForeignKey(
        'Artist', on_delete=models.CASCADE, related_name='tallies'
    )
    event = models.ForeignKey(
        'Event', on_delete=models.CASCADE, related_name='lineup'
    )
    slug = models.SlugField()

    REQUIRED_FIELDS = ['artist', 'event']
    objects = TallyManager()

    def __str__(self):
        return self.slug


class TicketType(models.Model):
    """Ticket type model. (better description needed)"""
    event = models.ForeignKey(
        'Event', on_delete=models.CASCADE, related_name='ticket_types'
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    slug = models.SlugField()
    tickets_remaining = models.IntegerField(blank=True, null=True)

    REQUIRED_FIELDS = ['event', 'name', 'price']
    objects = TicketTypeManager()

    def __str__(self):
        return self.slug


class Ticket(models.Model):
    """Ticket model. (better description needed)"""
    owner = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='tickets'
    )
    ticket_type = models.ForeignKey(
        'TicketType', on_delete=models.CASCADE, related_name='tickets'
    )
    vote = models.ForeignKey(
        'Tally',
        on_delete=models.CASCADE,
        related_name='tickets',
        null=True,
        blank=True
    )

    REQUIRED_FIELDS = ['owner', 'ticket_type']
    objects = TicketManager()

    def __str__(self):
        return str(self.pk)
