from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model
from django.db.models import Count

from rest_framework import filters as rest_filters
from rest_framework import generics, authentication, serializers
from rest_framework.permissions import IsAuthenticated

from core.models import Artist, Promoter, Venue, Event, Tally, TicketType, \
                        Ticket
from league.permissions import IsVerifiedPromoter, IsPromoterOrReadOnly, \
                               IsOwner
from league.serializers import CreateVenueSerializer, VenueSerializer, \
                               CreateEventSerializer, CreateTicketSerializer, \
                               EventSerializer, TallySerializer, \
                               PublicTallySerializer, TicketTypeSerializer, \
                               TicketSerializer, TableRowSerializer


class CreateVenueView(generics.CreateAPIView):
    """Create a new venue."""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsVerifiedPromoter,)
    serializer_class = CreateVenueSerializer


class CreateEventView(generics.CreateAPIView):
    """Create a new event."""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsVerifiedPromoter,)
    serializer_class = CreateEventSerializer

    def perform_create(self, serializer):
        serializer.save(promoter=self.request.user.promoter)


class CreateTallyView(generics.CreateAPIView):
    """Create a new tally."""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsVerifiedPromoter)
    serializer_class = TallySerializer


class CreateTicketTypeView(generics.CreateAPIView):
    """Create a new ticket type."""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsVerifiedPromoter,)
    serializer_class = TicketTypeSerializer


class CreateTicketView(generics.CreateAPIView):
    """Create a new ticket."""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateTicketSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EditVenueView(generics.RetrieveUpdateDestroyAPIView):
    """Edit a venue."""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsVerifiedPromoter,)
    serializer_class = VenueSerializer
    queryset = Venue.objects.all()
    lookup_field = 'slug'


class EditEventView(generics.RetrieveUpdateDestroyAPIView):
    """Edit an event."""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (
        IsAuthenticated, IsVerifiedPromoter, IsPromoterOrReadOnly,
    )
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class DeleteTallyView(generics.RetrieveDestroyAPIView):
    """Delete a tally."""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (
        IsAuthenticated, IsVerifiedPromoter, IsPromoterOrReadOnly,
    )
    serializer_class = TallySerializer
    queryset = Tally.objects.all()
    lookup_field = 'slug'


class EditTicketTypeView(generics.RetrieveUpdateDestroyAPIView):
    """Edit a ticket type."""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (
        IsAuthenticated, IsVerifiedPromoter, IsPromoterOrReadOnly,
    )
    serializer_class = TicketTypeSerializer
    queryset = TicketType.objects.all()
    lookup_field = 'slug'


class VoteTicketView(generics.RetrieveUpdateAPIView):
    """Edit a ticket (vote)."""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOwner,)
    queryset = Ticket.objects.all()

    def get_serializer_class(self):
        event = Ticket.objects.get(pk=self.kwargs['pk']).ticket_type.event

        class VoteSerializer(serializers.ModelSerializer):
            """Serializer for the ticket object when voting."""
            ticket_id = serializers.ReadOnlyField(source='pk')
            owner = serializers.StringRelatedField()
            ticket_type = serializers.StringRelatedField()
            vote = serializers.SlugRelatedField(
                queryset=Tally.objects.filter(
                    event=event
                ), slug_field='slug'
            )

            class Meta:
                model = Ticket
                fields = ('owner', 'ticket_id', 'ticket_type', 'vote')
                extra_kwargs = {
                    'owner': {'read_only': True},
                    'ticket_type': {'read_only': True},
                }

        return VoteSerializer


class RetrieveVenueView(generics.RetrieveAPIView):
    """Retrieve a venue."""
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    lookup_field = 'slug'


class RetrieveEventView(generics.RetrieveAPIView):
    """Retrieve an event."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class RetrieveTallyView(generics.RetrieveAPIView):
    """Retrieve a tally."""
    queryset = Tally.objects.all()
    serializer_class = PublicTallySerializer
    lookup_field = 'slug'


class RetrieveTicketView(generics.RetrieveAPIView):
    """Retrieve a ticket."""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOwner,)
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class RetrieveTableRowView(generics.RetrieveAPIView):
    """Retrieve a table row."""
    serializer_class = TableRowSerializer
    queryset = Artist.objects.all()
    lookup_field = 'slug'


class VenueFilter(filters.FilterSet):
    """Defines the filter fields for ListVenueView."""
    address_city = filters.CharFilter(
        field_name='address_city', lookup_expr='icontains'
    )
    address_country = filters.CharFilter(
        field_name='address_country', lookup_expr='icontains'
    )
    address_line1 = filters.CharFilter(
        field_name='address_line1', lookup_expr='icontains'
    )
    address_line2 = filters.CharFilter(
        field_name='address_line2', lookup_expr='icontains'
    )
    address_state = filters.CharFilter(
        field_name='address_state', lookup_expr='icontains'
    )
    address_zip = filters.CharFilter(
        field_name='address_zip', lookup_expr='icontains'
    )
    description = filters.CharFilter(
        field_name='description', lookup_expr='icontains'
    )
    events = filters.ModelChoiceFilter(queryset=Event.objects.all())
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Venue
        fields = [
            'address_city', 'address_country', 'address_line1',
            'address_line2', 'address_state', 'address_zip',
            'description', 'events', 'name'
        ]


class EventFilter(filters.FilterSet):
    """Defines the filter fields for ListEventView."""
    description = filters.CharFilter(
        field_name='description', lookup_expr='icontains'
    )
    end_date = filters.DateFilter(
        field_name='end_date', lookup_expr='exact'
    )
    end_date__gt = filters.DateFilter(
        field_name='end_date', lookup_expr='gt'
    )
    end_date__lt = filters.DateFilter(
        field_name='end_date', lookup_expr='lt'
    )
    end_date__range = filters.DateFilter(
        field_name='end_date', lookup_expr='range'
    )
    end_time = filters.TimeFilter(
        field_name='end_time', lookup_expr='exact'
    )
    end_time__gt = filters.TimeFilter(
        field_name='end_time', lookup_expr='gt'
    )
    end_time__lt = filters.TimeFilter(
        field_name='end_time', lookup_expr='lt'
    )
    end_time__range = filters.TimeFilter(
        field_name='end_time', lookup_expr='range'
    )
    lineup = filters.ModelChoiceFilter(queryset=Tally.objects.all())
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    promoter = filters.ModelChoiceFilter(queryset=Promoter.objects.all())
    start_date = filters.DateFilter(
        field_name='start_date', lookup_expr='exact'
    )
    start_date__gt = filters.DateFilter(
        field_name='start_date', lookup_expr='gt'
    )
    start_date__lt = filters.DateFilter(
        field_name='start_date', lookup_expr='lt'
    )
    start_date__range = filters.DateFilter(
        field_name='start_date', lookup_expr='range'
    )
    start_time = filters.TimeFilter(
        field_name='start_time', lookup_expr='exact'
    )
    start_time__gt = filters.TimeFilter(
        field_name='start_time', lookup_expr='gt'
    )
    start_time__lt = filters.TimeFilter(
        field_name='start_time', lookup_expr='lt'
    )
    start_time__range = filters.TimeFilter(
        field_name='start_time', lookup_expr='range'
    )
    ticket_types = filters.ModelChoiceFilter(queryset=TicketType.objects.all())
    venue = filters.ModelChoiceFilter(queryset=Venue.objects.all())

    class Meta:
        model = Event
        fields = [
            'description', 'end_date', 'end_time', 'lineup', 'name',
            'promoter', 'start_date', 'start_time', 'ticket_types', 'venue'
        ]


class TallyFilter(filters.FilterSet):
    """Defines the filter fields for ListTallyView."""
    artist = filters.ModelChoiceFilter(queryset=Artist.objects.all())
    event = filters.ModelChoiceFilter(queryset=Event.objects.all())

    class Meta:
        model = Tally
        fields = ['artist', 'event']


class TicketTypeFilter(filters.FilterSet):
    """Defines the filter fields for ListTicketTypeView."""
    event = filters.ModelChoiceFilter(queryset=Event.objects.all())
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    price = filters.NumberFilter(field_name='price', lookup_expr='exact')
    price__gt = filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = filters.NumberFilter(field_name='price', lookup_expr='lt')
    price__range = filters.NumberFilter(
        field_name='price', lookup_expr='range'
    )
    tickets = filters.ModelChoiceFilter(queryset=Ticket.objects.all())
    tickets_remaining = filters.NumberFilter(
        field_name='tickets_remaining', lookup_expr='exact'
    )
    tickets_remaining__gt = filters.NumberFilter(
        field_name='tickets_remaining', lookup_expr='gt'
    )
    tickets_remaining__lt = filters.NumberFilter(
        field_name='tickets_remaining', lookup_expr='lt'
    )
    tickets_remaining__range = filters.NumberFilter(
        field_name='tickets_remaining', lookup_expr='range'
    )


    class Meta:
        model = TicketType
        fields = ['event', 'name', 'price', 'tickets', 'tickets_remaining']


class TicketFilter(filters.FilterSet):
    """Defines the filter fields for ListTicketView."""
    ticket_type = filters.ModelChoiceFilter(queryset=TicketType.objects.all())
    vote = filters.ModelChoiceFilter(queryset=Tally.objects.all())

    class Meta:
        model = Ticket
        fields = ['ticket_type', 'vote']


class TableRowFilter(filters.FilterSet):
    """Defines the filter fields for ListTableRowView."""
    event_count = filters.NumberFilter(
        field_name='event_count', lookup_expr='exact'
    )
    event_count__gt = filters.NumberFilter(
        field_name='event_count', lookup_expr='gt'
    )
    event_count__lt = filters.NumberFilter(
        field_name='event_count', lookup_expr='lt'
    )
    event_count__range = filters.NumberFilter(
        field_name='event_count', lookup_expr='range'
    )
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    points = filters.NumberFilter(
        field_name='points', lookup_expr='exact'
    )
    points__gt = filters.NumberFilter(
        field_name='points', lookup_expr='gt'
    )
    points__lt = filters.NumberFilter(
        field_name='points', lookup_expr='lt'
    )
    points__range = filters.NumberFilter(
        field_name='points', lookup_expr='range'
    )

    class Meta:
        model = Artist
        fields = ['event_count', 'name', 'points']


class ListVenueView(generics.ListAPIView):
    """List venues."""
    queryset = Venue.objects.all().order_by('name')
    serializer_class = VenueSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    )
    filterset_class = VenueFilter
    search_fields = (
        'address_city', 'address_country', 'address_line1', 'address_line2',
        'address_state', 'address_zip', 'description', 'name'
    )
    ordering_fields = (
        'address_city', 'address_country', 'address_line1', 'address_line2',
        'address_state', 'address_zip', 'description', 'name'
    )


class ListEventView(generics.ListAPIView):
    """List events."""
    queryset = Event.objects.all().order_by('pk')
    serializer_class = EventSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    )
    filterset_class = EventFilter
    search_fields = (
        'description', 'end_date', 'end_time', 'name', 'start_date',
        'start_time'
    )
    ordering_fields = (
        'description', 'end_date', 'end_time', 'name', 'start_date',
        'start_time'
    )


class ListTallyView(generics.ListAPIView):
    """List tallies."""
    queryset = Tally.objects.all().order_by('slug')
    serializer_class = PublicTallySerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    )
    filterset_class = TallyFilter


class ListTicketTypeView(generics.ListAPIView):
    """List ticket types."""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsVerifiedPromoter,)
    serializer_class = TicketTypeSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    )
    filterset_class = TicketTypeFilter
    search_fields = ('name', 'price', 'tickets_remaining')
    ordering_fields = ('name', 'price', 'tickets_remaining')

    def get_queryset(self):
        return TicketType.objects.filter(
            event__promoter=self.request.user.promoter
        )


class ListTicketView(generics.ListAPIView):
    """List tickets."""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TicketSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    )
    filterset_class = TicketFilter

    def get_queryset(self):
        return Ticket.objects.filter(owner=self.request.user)


class ListTableRowView(generics.ListAPIView):
    """List table rows."""
    serializer_class = TableRowSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    )
    filterset_class = TableRowFilter
    search_fields = ('event_count', 'name', 'points')
    ordering_fields = ('event_count', 'name', 'points')

    def get_queryset(self):
        return Artist.objects.all().annotate(
            event_count=Count('tallies', distinct=True),
            points=Count('tallies__tickets', distinct=True)
        )