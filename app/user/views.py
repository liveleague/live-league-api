from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer, \
                             ArtistSerializer, PromoterSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new authentication token."""
    serializer_class = AuthTokenSerializer
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


class ManageUserView(generics.RetrieveUpdateAPIView):
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
