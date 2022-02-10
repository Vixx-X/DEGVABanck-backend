from django.db.models.query_utils import Q
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

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
    credit_cards = user.credits.values_list("number", flat=True)
    user_related_ids = accounts + credit_cards
    from_filter = Q(source__in=user_related_ids)
    to_filter = Q(target=user_related_ids)
    user_filter = from_filter | to_filter
    return Transaction.objects.filter(user_filter)


class UserTransactionListCreateView(generics.ListCreateAPIView):
    """
    List user transactions
    """
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = UserTransactionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return get_transactions_by_user(self.request.user)

class UserTransactionView(generics.RetrieveAPIView):
    """
    Retrieve user transaction
    """
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = UserTransactionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return get_transactions_by_user(self.request.user)
