from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from degvabank.apps.card.models import DebitCard

from degvabank.apps.petitions.models import Petition

from .serializers import AccountSerializer, UserAccountSerializer
from .models import Account


class AccountViewSet(viewsets.ModelViewSet):
    """
    Entrypoint for accounts
    """

    permission_classes = (IsAdminUser,)
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class UserAccountListCreateView(generics.ListCreateAPIView):
    """
    List and create user accounts
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
