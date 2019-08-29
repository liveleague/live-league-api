from django.contrib.auth import get_user_model

from rest_framework import generics, authentication, permissions

from superuser.permissions import IsSuperuserAndStaff
from superuser.serializers import CreditSerializer


class ManageCreditView(generics.RetrieveUpdateAPIView):
    """Manage a user's credit."""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsSuperuserAndStaff,)
    serializer_class = CreditSerializer

    def get_queryset(self):
        return get_user_model().objects.filter(pk=self.kwargs['pk'])
