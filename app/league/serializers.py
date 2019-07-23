from django.template.defaultfilters import slugify

from rest_framework import serializers

from core.models import Artist, Venue, Event, Tally, TicketType, Ticket, \
                        Voucher
from user.serializers import PublicArtistSerializer


class CreateVenueSerializer(serializers.ModelSerializer):
    """Serializer for creating a venue object."""

    class Meta:
        model = Venue
        fields = (
            'address_city', 'address_country', 'address_line1',
            'address_line2', 'address_state', 'address_zip',
            'description', 'name'
        )

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
            'description', 'name'
        )

    def update(self, instance, validated_data):
        """Update a venue and return it."""
        name = validated_data.pop('name', None)
        venue = super().update(instance, validated_data)
        if name:
            venue.slug = slugify(name)
        venue.save()
        return venue


class CreateEventSerializer(serializers.ModelSerializer):
    """Serializer for creating an event object."""
    id = serializers.ReadOnlyField(source='pk')
    promoter = serializers.ReadOnlyField(source='promoter.name')
    venue = serializers.SlugRelatedField(
        queryset=Venue.objects.all(), slug_field='name'
    )

    class Meta:
        model = Event
        fields = (
            'description', 'end_date', 'end_time', 'id',
            'name', 'start_date', 'start_time',
            'promoter', 'venue'
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create a new event and return it."""
        return Event.objects.create_event(**validated_data)


class TallySerializer(serializers.ModelSerializer):
    """Serializer for the tally object."""
    artist = serializers.SlugRelatedField(
        queryset=Artist.objects.all(), slug_field='name'
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
    artist = serializers.SlugRelatedField(
        queryset=Artist.objects.all(), slug_field='name'
    )
    votes = serializers.SerializerMethodField()

    class Meta:
        model = Tally
        fields = ('artist', 'event', 'votes')

    def get_votes(self, obj):
        return obj.tickets.count()


class LineupSerializer(serializers.ModelSerializer):
    """Serializer for the tally object when called from EventSerializer."""
    artist = serializers.SlugRelatedField(
        queryset=Artist.objects.all(), slug_field='name'
    )
    votes = serializers.SerializerMethodField()

    class Meta:
        model = Tally
        fields = ('artist', 'votes')

    def get_votes(self, obj):
        return obj.tickets.count()


class TicketTypeSerializer(serializers.ModelSerializer):
    """Serializer for the ticket type object."""

    class Meta:
        model = TicketType
        fields = ('event', 'name', 'price', 'tickets_remaining')

    def __init__(self, *args, **kwargs):
        super(TicketTypeSerializer, self).__init__(*args, **kwargs)
        promoter = kwargs['context']['request'].user.promoter
        self.fields['event'].queryset = Event.objects.filter(promoter=promoter)

    def create(self, validated_data):
        """Create a new ticket type and return it."""
        return TicketType.objects.create_ticket_type(**validated_data)


class TicketTypeEventSerializer(serializers.ModelSerializer):
    """
    Serializer for the ticket type object when called from EventSerializer.
    """

    class Meta:
        model = TicketType
        fields = ('name', 'price', 'tickets_remaining')


class CreateTicketSerializer(serializers.ModelSerializer):
    """Serializer for the ticket object."""
    id = serializers.ReadOnlyField(source='pk')
    owner = serializers.StringRelatedField()
    ticket_type = serializers.SlugRelatedField(
        queryset=TicketType.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Ticket
        fields = ('id', 'owner', 'ticket_type', 'vote')
        extra_kwargs = {
            'owner': {'read_only': True},
            'vote': {'read_only': True}
        }
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create a new ticket and return it."""
        return Ticket.objects.create_ticket(**validated_data)


class TicketSerializer(serializers.ModelSerializer):
    """Serializer for the ticket object."""
    id = serializers.ReadOnlyField(source='pk')
    owner = serializers.StringRelatedField()
    ticket_type = serializers.StringRelatedField()
    vote = serializers.SlugRelatedField(
        queryset=Tally.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Ticket
        fields = ('id', 'owner', 'ticket_type', 'vote')
        extra_kwargs = {
            'owner': {'read_only': True},
            'ticket_type': {'read_only': True},
        }
        read_only_fields = ('id',)


class CreateVoucherSerializer(serializers.ModelSerializer):
    """Serializer for the voucher object."""
    ticket_type = serializers.SlugRelatedField(
        queryset=TicketType.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Voucher
        fields = ('code', 'ticket_type')
        extra_kwargs = {
            'code': {'read_only': True},
        }

    def create(self, validated_data):
        """Create a new ticket and return it."""
        return Voucher.objects.create_voucher(**validated_data)


class VoucherSerializer(serializers.ModelSerializer):
    """Serializer for the voucher object."""
    owner = serializers.StringRelatedField()
    ticket_type = serializers.StringRelatedField()
    vote = serializers.SlugRelatedField(
        queryset=Tally.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Voucher
        fields = ('code', 'owner', 'ticket_type', 'vote')
        extra_kwargs = {
            'owner': {'read_only': True},
            'ticket_type': {'read_only': True},
        }


class EventSerializer(serializers.ModelSerializer):
    """Serializer for the event object."""
    id = serializers.ReadOnlyField(source='pk')
    lineup = LineupSerializer(many=True, read_only=True)
    promoter = serializers.ReadOnlyField(source='promoter.name')
    ticket_types = TicketTypeEventSerializer(many=True, read_only=True)
    tickets_sold = serializers.SerializerMethodField()
    venue = serializers.SlugRelatedField(
        queryset=Venue.objects.all(), slug_field='name'
    )

    class Meta:
        model = Event
        fields = (
            'description', 'end_date', 'end_time', 'id',
            'lineup', 'name', 'promoter', 'start_date', 'start_time',
            'ticket_types', 'tickets_sold', 'venue'
        )
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        """Update an event and return it."""
        name = validated_data.pop('name', None)
        event = super().update(instance, validated_data)
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
        fields = ('name', 'event_count', 'points')
