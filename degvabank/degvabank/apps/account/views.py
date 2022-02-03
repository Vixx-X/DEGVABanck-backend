from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

from .serializers import AccountSerializer, UserAccountSerializer
from .models import Account


class AccountViewSet(viewsets.ModelViewSet):
    """
    Entrypoint for accounts
    """

    permission_classes = (IsAdminUser,)
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class UserAccountListView(generics.ListAPIView):
    """
    List user accounts
    """
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = UserAccountSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.accounts.all()

class UserAccountView(generics.RetrieveAPIView):
    """
    Retrieve user account
    """
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = UserAccountSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.accounts.all()
