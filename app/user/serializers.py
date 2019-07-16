from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from core.models import Artist, Promoter, Message, ReadFlag, Ticket


class TokenSerializer(serializers.Serializer):
    """Serializer for the authentication token object."""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = (
            'email', 'password', 'name', 'address_city', 'address_country',
            'address_line1', 'address_line2', 'address_state', 'address_zip',
            'facebook', 'instagram', 'phone', 'soundcloud', 'spotify',
            'twitter', 'website', 'youtube', 'image'
        )
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user and return it."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user and return it."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class ArtistSerializer(serializers.ModelSerializer):
    """Serializer for the artist object."""

    class Meta:
        model = Artist
        fields = (
            'email', 'password', 'name', 'description', 'facebook',
            'instagram', 'phone', 'soundcloud', 'spotify', 'twitter',
            'website', 'youtube', 'image'
        )
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5},
        }

    def create(self, validated_data):
        """Create a new artist and return it."""
        return Artist.objects.create_artist(**validated_data)

    def update(self, instance, validated_data):
        """Update an artist and return it."""
        password = validated_data.pop('password', None)
        artist = super().update(instance, validated_data)
        if password:
            artist.set_password(password)
            artist.save()
        return artist


class PublicArtistSerializer(serializers.ModelSerializer):
    """Public serializer for the artist object."""
    events = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = (
            'name', 'description', 'events', 'points', 'facebook', 'instagram',
            'soundcloud', 'spotify', 'twitter', 'website', 'youtube', 'image'
        )

    def get_events(self, obj):
        return obj.tallies.count()

    def get_points(self, obj):
        tickets = Ticket.objects.filter(vote__artist=obj)
        return tickets.count()


class PromoterSerializer(serializers.ModelSerializer):
    """Serializer for the promoter object."""

    class Meta:
        model = Promoter
        fields = (
            'email', 'password', 'name', 'description', 'is_verified',
            'facebook', 'instagram', 'phone', 'soundcloud', 'spotify',
            'twitter', 'website', 'youtube', 'image'
        )
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5},
            'is_verified': {'read_only': True},
        }

    def create(self, validated_data):
        """Create a new promoter and return it."""
        return Promoter.objects.create_promoter(**validated_data)

    def update(self, instance, validated_data):
        """Update a promoter and return it."""
        password = validated_data.pop('password', None)
        promoter = super().update(instance, validated_data)
        if password:
            promoter.set_password(password)
            promoter.save()
        return promoter


class PublicPromoterSerializer(serializers.ModelSerializer):
    """Public serializer for the promoter object."""

    class Meta:
        model = Promoter
        fields = (
            'name', 'description', 'facebook', 'instagram', 'soundcloud',
            'spotify', 'twitter', 'website', 'youtube', 'image'
        )


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for the message object."""
    sender = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ('created_date', 'created_time', 'sender', 'subject', 'text')
        extra_kwargs = {
            'sender': {'read_only': True},
        }

    def create(self, validated_data):
        """Create a new message and return it."""
        return Message.objects.create_message(**validated_data)


class ReadFlagSerializer(serializers.ModelSerializer):
    """Serializer for the read flag object."""

    class Meta:
        model = ReadFlag
        fields = ('message', 'opened', 'recipient')
        extra_kwargs = {
            'opened': {'read_only': True},
        }

    def __init__(self, *args, **kwargs):
        super(ReadFlagSerializer, self).__init__(*args, **kwargs)
        user = kwargs['context']['request'].user
        self.fields['message'].queryset = Message.objects.filter(sender=user)

    def create(self, validated_data):
        """Create a new read flag and return it."""
        return ReadFlag.objects.create_readflag(**validated_data)
