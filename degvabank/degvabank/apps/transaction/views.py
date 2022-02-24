from django.db.models.query_utils import Q
from django_filters import rest_framework as filters
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

from degvabank.apps.transaction.filters import TransaccionFilter

from .serializers import TransactionSerializer, UserTransactionSerializer
from .models import Transaction


class TransactionViewSet(viewsets.ModelViewSet):
    """
    Entrypoint for transactions
    """
    permission_classes = (IsAdminUser,)
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

def get_transactions_by_user(user):
    accounts = user.accounts.values_list("id", flat=True)
    credit_cards = user.credit_cards.values_list("number", flat=True)
    from_filter = Q(source__in=accounts) | Q(source__in=credit_cards)
    to_filter = Q(target__in=accounts) | Q(target__in=credit_cards)
    user_filter = from_filter | to_filter
    return Transaction.objects.filter(user_filter)

class UserTransactionListCreateView(generics.ListCreateAPIView):
    """
    List user transactions
    """
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = UserTransactionSerializer
    permission_classes = (IsAuthenticated,)
    ordering_fields = "__all__"
    filterset_class = TransaccionFilter

    def get_queryset(self):
        return Transaction.objects.get_queryset_by_user(self.request.user)

class UserTransactionView(generics.RetrieveAPIView):
    """
    Retrieve user transaction
    """
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = UserTransactionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Transaction.objects.get_queryset_by_user(self.request.user)
