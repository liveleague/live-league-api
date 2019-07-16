from django_filters import rest_framework as filters

from rest_framework import filters as rest_filters
from rest_framework import generics, authentication, permissions, viewsets, \
                           mixins, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Artist, Promoter, Event, Tally
from user.serializers import UserSerializer, TokenSerializer, \
                             ArtistSerializer, PromoterSerializer, \
                             PublicArtistSerializer, \
                             PublicPromoterSerializer, MessageSerializer, \
                             ReadFlagSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new authentication token."""
    serializer_class = TokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class CreateUserView(generics.CreateAPIView):
    """Create a new user."""
    serializer_class = UserSerializer


class CreateArtistView(generics.CreateAPIView):
    """Create a new user."""
    serializer_class = ArtistSerializer


class CreatePromoterView(generics.CreateAPIView):
    """Create a new user."""
    serializer_class = PromoterSerializer


class CreateMessageView(generics.CreateAPIView):
    """Create a new message."""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class CreateReadFlagView(generics.CreateAPIView):
    """Create a new read flag."""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ReadFlagSerializer


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    """Manage the authenticated user."""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.user.is_artist:
            serializer_class = ArtistSerializer
        elif self.request.user.is_promoter:
            serializer_class = PromoterSerializer
        else:
            serializer_class = UserSerializer
        return serializer_class

    def get_object(self):
        if self.request.user.is_artist:
            return self.request.user.artist
        elif self.request.user.is_promoter:
            return self.request.user.promoter
        else:
            return self.request.user


class RetrieveArtistView(generics.RetrieveAPIView):
    """Retrieve an artist."""
    queryset = Artist.objects.all()
    serializer_class = PublicArtistSerializer
    lookup_field = 'slug'


class RetrievePromoterView(generics.RetrieveAPIView):
    """Retrieve a promoter."""
    queryset = Promoter.objects.filter(is_verified=True)
    serializer_class = PublicPromoterSerializer
    lookup_field = 'slug'


class ArtistFilter(filters.FilterSet):
    """Defines the filter fields for ListArtistView."""
    description = filters.CharFilter(
        field_name='description', lookup_expr='icontains'
    )
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    tallies = filters.ModelChoiceFilter(queryset=Tally.objects.all())

    class Meta:
        model = Artist
        fields = ['description', 'name', 'tallies']


class PromoterFilter(filters.FilterSet):
    """Defines the filter fields for ListPromoterView."""
    description = filters.CharFilter(
        field_name='description', lookup_expr='icontains'
    )
    events = filters.ModelChoiceFilter(queryset=Event.objects.all())
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Promoter
        fields = ['description', 'name', 'events']


class ListArtistView(generics.ListAPIView):
    """List artists."""
    queryset = Artist.objects.all().order_by('name')
    serializer_class = PublicArtistSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    )
    filterset_class = ArtistFilter
    search_fields = ('description', 'name')
    ordering_fields = ('description', 'name')


class ListPromoterView(generics.ListAPIView):
    """List promoters."""
    queryset = Promoter.objects.filter(is_verified=True).order_by('name')
    serializer_class = PublicPromoterSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    )
    filterset_class = PromoterFilter
    search_fields = ('description', 'name')
    ordering_fields = ('description', 'name')
