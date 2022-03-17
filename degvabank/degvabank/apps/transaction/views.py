from django.db.models.query_utils import Q
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response

from degvabank.apps.transaction.filters import TransaccionFilter

from .serializers import TransactionSerializer, UserTransactionSerializer, ForeignTransactionSerializer
from .models import Transaction


class TransactionViewSet(viewsets.ModelViewSet):
    """
    Entrypoint for transactions
    """

    permission_classes = (IsAdminUser,)
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class UserTransactionListCreateView(generics.ListCreateAPIView):
    """
    List user transactions
    """

    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = UserTransactionSerializer
    permission_classes = (IsAuthenticated,)
    ordering_fields = "__all__"
    filterset_class = TransaccionFilter
    search_fields = ['reason', 'target', 'source', 'amount']

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


class ForeignTransactionView(generics.CreateAPIView):
    """
    Create foreign transaction
    """

    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = ForeignTransactionSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()
        headers = self.get_success_headers(serializer.data)
        tran_ser = TransactionSerializer(instance=transaction)
        return Response(tran_ser.data, status=status.HTTP_201_CREATED, headers=headers)
