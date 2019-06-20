from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from core.models import Artist, Promoter
from user.serializers import UserSerializer, TokenSerializer, \
                             ArtistSerializer, PromoterSerializer, \
                             PublicArtistSerializer, PublicPromoterSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new authentication token."""
    serializer_class = TokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class CreateUserView(generics.CreateAPIView):
    """Create a new user."""
    # Needs a 'DRY' makeover
    serializer_class = UserSerializer


class CreateArtistView(generics.CreateAPIView):
    """Create a new user."""
    # Needs a 'DRY' makeover
    serializer_class = ArtistSerializer


class CreatePromoterView(generics.CreateAPIView):
    """Create a new user."""
    # Needs a 'DRY' makeover
    serializer_class = PromoterSerializer


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
    queryset = Artist.objects.all().order_by('name')
    serializer_class = PublicArtistSerializer
    lookup_field = 'slug'


class RetrievePromoterView(generics.RetrieveAPIView):
    """Retrieve a promoter."""
    queryset = Promoter.objects.filter(is_verified=True).order_by('name')
    serializer_class = PublicPromoterSerializer
    lookup_field = 'slug'


class ListArtistView(generics.ListAPIView):
    """List artists."""
    queryset = Artist.objects.all()
    serializer_class = PublicArtistSerializer


class ListPromoterView(generics.ListAPIView):
    """List promoters."""
    queryset = Promoter.objects.filter(is_verified=True)
    serializer_class = PublicPromoterSerializer
