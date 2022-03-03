from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

from degvabank.apps.transaction.serializers import UserTransactionSerializer

from .serializers import PayWayKeysSerializer, PayWayTransactionAccount, PayWayTransactionCreditCard, UserPayWayKeysSerializer, PayWayMetaSerializer, UserPayWayMetaSerializer
from .models import PayWayKeys, PayWayMetaData

class PayWayKeysViewSet(viewsets.ModelViewSet):
    """
    Entrypoint for payway keys
    """

    permission_classes = (IsAdminUser,)
    queryset = PayWayKeys.objects.all()
    serializer_class = PayWayKeysSerializer


class UserPayWayKeysCreateView(generics.CreateAPIView):

    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = UserPayWayKeysSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(meta_data=self.meta_data)

    def create(self, request, **kwargs):
        self.meta_data = generics.get_object_or_404(PayWayMetaData, app_id=kwargs.get("app_id"))
        try:
            # may not exist
            request.user.key_pairs.get(meta_data_id=self.meta_data.id).delete()
        except:
            pass
        return super().create(request)


class PayWayMetaViewSet(viewsets.ModelViewSet):
    """
    Entrypoint for payway keys
    """

    permission_classes = (IsAdminUser,)
    queryset = PayWayMetaData.objects.all()
    serializer_class = PayWayMetaSerializer


class UserPayWayMetaViewSet(viewsets.ModelViewSet):

    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = UserPayWayMetaSerializer
    permission_classes = (IsAuthenticated,)
    queryset = PayWayMetaData.objects.all().order_by("date_created")
    lookup_field="app_id"

    def get_queryset(self):
        return super().get_queryset().filter(account__user_id=self.request.user.id)

class UserPayWayMetaTransactionList(generics.ListAPIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = UserTransactionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return super().get_queryset().filter(account__user_id=self.request.user.id)


class PayGateWayAccount(generics.CreateAPIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = PayWayTransactionAccount
    permission_classes = (IsAuthenticated,)

class PayGateWayCard(generics.CreateAPIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = PayWayTransactionCreditCard

