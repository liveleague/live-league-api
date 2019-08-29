from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class CreditSerializer(serializers.ModelSerializer):
    """Serializer for the credit object."""

    class Meta:
        model = get_user_model()
        fields = ('credit',)
