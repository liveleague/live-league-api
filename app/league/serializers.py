
# -------------------- Old API -------------------- #
'''
from django.contrib.auth import get_user_model

from rest_framework import serializers

from core.models import Venue, Event


class VenueSerializer(serializers.ModelSerializer):
    """Serializer for the venue object."""

    class Meta:
        model = Venue
        fields = ('address', 'description', 'name')


class EventSerializer(serializers.ModelSerializer):
    """Serializer for the event object."""
    artists = serializers.StringRelatedField(many=True)

    class Meta:
        model = Event
        fields = (
            'artists', 'description', 'end_time','name', 'promoter',
            'start_time', 'venue'
        )


# class TableSerializer(
#   """
#   Lists artists, their total number of events played and points this season.
#   """


# class ArtistDetailSerializer(
#   """Displays the public details of artist(s)."""


# class PromoterDetail(
#   """Displays the public details of promoter(s)."""


# class ArtistEventsList(
#   """Lists the events of artist(s)."""


# class PromoterEventsList(
#   """Lists the events of promoter(s)."""


# class ArtistPointsList(
#   """"Returns historical points data of artist(s)."""


# class PromoterPointsList(
#   """"Returns historical points data of artist(s)."""
'''
