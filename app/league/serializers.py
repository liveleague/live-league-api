from django.template.defaultfilters import slugify

from rest_framework import serializers

from core.models import Artist, Venue, Event, Tally, TicketType, Ticket
from user.serializers import PublicArtistSerializer


class CreateVenueSerializer(serializers.ModelSerializer):
    """Serializer for creating a venue object."""

    class Meta:
        model = Venue
        fields = (
            'address_city', 'address_country', 'address_line1',
            'address_line2', 'address_state', 'address_zip',
            'description', 'google_maps', 'name', 'image'
        )
        extra_kwargs = {
            'slug': {'read_only': True},
        }

    def create(self, validated_data):
        """Create a new venue and return it."""
        return Venue.objects.create_venue(**validated_data)


class VenueSerializer(serializers.ModelSerializer):
    """Serializer for the venue object."""

    class Meta:
        model = Venue
        fields = (
            'address_city', 'address_country', 'address_line1',
            'address_line2', 'address_state', 'address_zip',
            'description', 'google_maps', 'image', 'name', 'slug'
        )

    def update(self, instance, validated_data):
        """Update a venue and return it."""
        venue = super().update(instance, validated_data)
        if 'name' in validated_data:
            venue.slug = slugify(validated_data['name'])
        venue.save()
        return venue


class CreateEventSerializer(serializers.ModelSerializer):
    """Serializer for creating an event object."""
    id = serializers.ReadOnlyField(source='pk')
    promoter = serializers.ReadOnlyField(source='promoter.name')
    venue = serializers.SlugRelatedField(
        queryset=Venue.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Event
        fields = (
            'description', 'end_date', 'end_time', 'id',
            'name', 'start_date', 'start_time',
            'promoter', 'venue', 'image'
        )
        read_only_fields = ('id',)
        extra_kwargs = {
            'slug': {'read_only': True},
        }

    def create(self, validated_data):
        """Create a new event and return it."""
        return Event.objects.create_event(**validated_data)


class TallySerializer(serializers.ModelSerializer):
    """Serializer for the tally object."""
    artist = serializers.SlugRelatedField(
        queryset=Artist.objects.all(), slug_field='slug'
    )
    votes = serializers.SerializerMethodField()

    class Meta:
        model = Tally
        fields = ('artist', 'event', 'votes')

    def __init__(self, *args, **kwargs):
        promoter = kwargs['context']['request'].user.promoter
        super(TallySerializer, self).__init__(*args, **kwargs)
        self.fields['event'].queryset = Event.objects.filter(promoter=promoter)

    def get_votes(self, obj):
        return obj.tickets.count()

    def create(self, validated_data):
        """Create a new tally and return it."""
        return Tally.objects.create_tally(**validated_data)


class PublicTallySerializer(serializers.ModelSerializer):
    """Serializer for the tally object when publicly retrieved or listed."""
    artist = serializers.ReadOnlyField(source='artist.name')
    artist_slug = serializers.ReadOnlyField(source='artist.slug')
    event = serializers.ReadOnlyField(source='event.name')
    event_id = serializers.ReadOnlyField(source='event.pk')
    event_start_date = serializers.ReadOnlyField(source='event.start_date')
    event_start_time = serializers.ReadOnlyField(source='event.start_time')
    event_end_date = serializers.ReadOnlyField(source='event.end_date')
    event_end_time = serializers.ReadOnlyField(source='event.end_time')
    points = serializers.IntegerField(read_only=True)
    votes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tally
        fields = (
            'artist', 'artist_slug', 'event', 'event_id', 'event_end_date',
            'event_end_time', 'event_start_date', 'event_start_time',
            'points', 'slug', 'votes'
        )


class LineupSerializer(serializers.ModelSerializer):
    """Serializer for the tally object when called from EventSerializer."""
    artist = serializers.ReadOnlyField(source='artist.name')
    artist_slug = serializers.ReadOnlyField(source='artist.slug')
    tally = serializers.ReadOnlyField(source='slug')

    class Meta:
        model = Tally
        fields = ('artist', 'artist_slug', 'tally')


class TicketTypeSerializer(serializers.ModelSerializer):
    """Serializer for the ticket type object."""
    event_name = serializers.ReadOnlyField(source='event.name')
    event_start_date = serializers.ReadOnlyField(source='event.start_date')
    event_start_time = serializers.ReadOnlyField(source='event.start_time')
    event_end_date = serializers.ReadOnlyField(source='event.end_date')
    event_end_time = serializers.ReadOnlyField(source='event.end_time')

    class Meta:
        model = TicketType
        fields = (
            'event', 'event_name', 'event_start_date', 'event_start_time',
            'event_end_date', 'event_end_time', 'name', 'price',
            'tickets_remaining', 'slug'
        )
        extra_kwargs = {
            'slug': {'read_only': True},
        }

    def __init__(self, *args, **kwargs):
        super(TicketTypeSerializer, self).__init__(*args, **kwargs)
        promoter = kwargs['context']['request'].user.promoter
        self.fields['event'].queryset = Event.objects.filter(promoter=promoter)

    def create(self, validated_data):
        """Create a new ticket type and return it."""
        return TicketType.objects.create_ticket_type(**validated_data)

    def update(self, instance, validated_data):
        """Update a ticket type and return it."""
        ticket_type = super().update(instance, validated_data)
        event_id = str(instance).split('-', 1)[0]
        if 'name' in validated_data:
            ticket_type.slug = event_id + '-' + slugify(validated_data['name'])
        ticket_type.save()
        return ticket_type


class TicketTypeEventSerializer(serializers.ModelSerializer):
    """
    Serializer for the ticket type object when called from EventSerializer.
    """

    class Meta:
        model = TicketType
        fields = ('name', 'price', 'tickets_remaining', 'slug')


class CreateTicketSerializer(serializers.ModelSerializer):
    """Serializer for the ticket object."""
    owner = serializers.StringRelatedField()
    ticket_type = serializers.SlugRelatedField(
        queryset=TicketType.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Ticket
        fields = ('code', 'owner', 'ticket_type', 'vote')
        extra_kwargs = {
            'code': {'read_only': True},
            'owner': {'read_only': True},
            'vote': {'read_only': True},
        }
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create a new ticket and return it."""
        return Ticket.objects.create_ticket(**validated_data)


class TicketSerializer(serializers.ModelSerializer):
    """Serializer for the ticket object."""
    event = serializers.ReadOnlyField(source='ticket_type.event.name')
    event_id = serializers.ReadOnlyField(source='ticket_type.event.id')
    event_end_date = serializers.ReadOnlyField(
        source='ticket_type.event.end_date'
    )
    event_end_time = serializers.ReadOnlyField(
        source='ticket_type.event.end_time'
    )
    event_start_date = serializers.ReadOnlyField(
        source='ticket_type.event.start_date'
    )
    event_start_time = serializers.ReadOnlyField(
        source='ticket_type.event.start_time'
    )
    owner = serializers.StringRelatedField()
    ticket_type = serializers.ReadOnlyField(source='ticket_type.name')
    ticket_type_slug = serializers.ReadOnlyField(source='ticket_type.slug')
    vote = serializers.SlugRelatedField(
        slug_field='slug', read_only=True
    )
    vote_artist = serializers.ReadOnlyField(source='vote.artist.name')
    vote_slug = serializers.ReadOnlyField(source='vote.artist.slug')

    class Meta:
        model = Ticket
        fields = (
            'created_date', 'created_time', 'code', 'event', 'event_id',
            'event_end_date', 'event_end_time', 'event_start_date',
            'event_start_time', 'id', 'owner', 'ticket_type',
            'ticket_type_slug', 'vote', 'vote_artist', 'vote_slug'
        )
        extra_kwargs = {
            'code': {'read_only': True},
            'id': {'read_only': True},
            'owner': {'read_only': True},
            'ticket_type': {'read_only': True},
            'vote': {'read_only': True},
        }


class EventSerializer(serializers.ModelSerializer):
    """Serializer for the event object."""
    id = serializers.ReadOnlyField(source='pk')
    lineup = LineupSerializer(many=True, read_only=True)
    promoter = serializers.ReadOnlyField(source='promoter.name')
    promoter_slug = serializers.ReadOnlyField(source='promoter.slug')
    ticket_types = TicketTypeEventSerializer(many=True, read_only=True)
    tickets_sold = serializers.SerializerMethodField()
    venue = serializers.SlugRelatedField(
        queryset=Venue.objects.all(), slug_field='slug'
    )
    venue_city = serializers.ReadOnlyField(source='venue.address_city')
    venue_google_maps = serializers.ReadOnlyField(
        source='venue.google_maps'
    )
    venue_name = serializers.ReadOnlyField(source='venue.name')

    class Meta:
        model = Event
        fields = (
            'description', 'end_date', 'end_time', 'id', 'image', 'lineup',
            'name', 'promoter', 'promoter_slug', 'start_date', 'start_time',
            'ticket_types', 'tickets_sold', 'venue', 'venue_city',
            'venue_google_maps', 'venue_name'
        )
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        """Update an event and return it."""
        event = super().update(instance, validated_data)
        if 'name' in validated_data:
            event.slug = slugify(validated_data['name'])
        event.save()
        return event

    def get_tickets_sold(self, obj):
        tickets = Ticket.objects.filter(ticket_type__event=obj)
        return tickets.count()


class TableRowSerializer(serializers.ModelSerializer):
    """
    Serializer for the artist, tally and ticket objects -
    organized in a table format.
    - [Artist] Artist.name
    - [Events] Artist.tallies.count()
    - [Points] Tickets(where votes went to artist).count()
    """
    event_count = serializers.IntegerField(read_only=True)
    points = serializers.IntegerField(read_only=True)

    class Meta:
        model = Artist
        fields = ('event_count', 'name', 'points', 'slug')
