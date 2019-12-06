from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class PasswordSerializer(serializers.ModelSerializer):
    """Serializer for a user's password."""

    class Meta:
        model = get_user_model()
        fields = ('password',)

    def update(self, instance, validated_data):
        """Update a password and return it."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class CreditSerializer(serializers.ModelSerializer):
    """Serializer for a user's credit."""

    class Meta:
        model = get_user_model()
        fields = ('credit',)


class StripeSerializer(serializers.ModelSerializer):
    """Serializer for a user's Stripe ID."""

    class Meta:
        model = get_user_model()
        fields = ('stripe_id',)
