from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

from .serializers import PayWayKeysSerializer, UserPayWayKeysSerializer, PayWayMetaSerializer, UserPayWayMetaSerializer
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

    def create(self, request, *args, **kwargs):
        try:
            # may not exist
            request.user.key_pairs.get(pk=request.data["meta_data"]).delete()
        except:
            pass
        return super().create(request, *args, **kwargs)


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
    lookup_field = 'app_name'

    def get_queryset(self):
        return super().get_queryset().filter(account__user_id=self.request.user.id)


