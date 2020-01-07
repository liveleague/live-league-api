import random
from hashlib import sha256

from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import generics, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, \
                                      permission_classes
from rest_framework.response import Response

from core.email import Email
from core.models import Promoter
from superuser.permissions import IsSuperuserAndStaff
from superuser.serializers import PasswordSerializer, CreditSerializer, \
                                  IsVerifiedSerializer, StripeSerializer

@api_view(['POST'])
@authentication_classes((authentication.TokenAuthentication,))
@permission_classes((permissions.IsAuthenticated, IsSuperuserAndStaff,))
def create_secret(request):
    """
    Create a secret and send it to the user's email address.
    A hash of the secret is returned to the client to be checked against
    the user's email link.
    """
    secret_code = sha256(str(random.random())[2:].encode()).hexdigest()
    secret_hash = sha256(secret_code.encode()).hexdigest()
    try:
        get_user_model().objects.get(email=request.data['email'])
        dynamic_template_data = {'secret_code': secret_code}
        Email(
            'password_reset', request.data['email'], dynamic_template_data
        ).send()
        return Response({'secret_hash': secret_hash})
    except get_user_model().DoesNotExist:
        return Response({'error': 'User does not exist.'})


class ManagePassword(generics.RetrieveUpdateAPIView):
    """Manage a user's password."""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsSuperuserAndStaff,)
    serializer_class = PasswordSerializer
    lookup_field = 'email'

    def get_queryset(self):
        return get_user_model().objects.filter(email=self.kwargs['email'])


class ManageCreditView(generics.RetrieveUpdateAPIView):
    """Manage a user's credit."""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsSuperuserAndStaff,)
    serializer_class = CreditSerializer

    def get_queryset(self):
        return get_user_model().objects.filter(pk=self.kwargs['pk'])


class ManageVerificationView(generics.RetrieveUpdateAPIView):
    """Manage a promoter's verification status."""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsSuperuserAndStaff,)
    serializer_class = IsVerifiedSerializer

    def get_queryset(self):
        return Promoter.objects.filter(pk=self.kwargs['pk'])


class ManageStripeView(generics.RetrieveUpdateAPIView):
    """Retrieve a user's Stripe IDs."""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsSuperuserAndStaff,)
    serializer_class = StripeSerializer

    def get_queryset(self):
        return get_user_model().objects.filter(pk=self.kwargs['pk'])
