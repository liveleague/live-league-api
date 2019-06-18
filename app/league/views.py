from rest_framework import viewsets, mixins, status, authentication
from rest_framework.permissions import IsAuthenticated

from core.models import Venue, Event
from .serializers import VenueSerializer, EventSerializer
from .permissions import IsVerifiedPromoter


class BasePromoterAttrViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Base viewset for promoter to create/edit venues and events."""
    authentication_classes = (authentication.TokenAuthentication,)

    def get_queryset(self):
        """Return objects for the current authenticated promoter only."""
        if (
            self.request.user.is_promoter and
            self.request.user.promoter.is_verified
        ):
            pass

    def perform_create(self, serializer):
        """Create a new venue or event."""
        serializer.save(promoter=self.request.user.promoter)


class VenueViewSet(BasePromoterAttrViewSet):
    """Venue management for promoters."""
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class EventViewSet(BasePromoterAttrViewSet):
    """Event management for promoters."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
