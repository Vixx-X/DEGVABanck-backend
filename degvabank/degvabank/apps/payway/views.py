from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response

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

    def create(self, request):
        meta_data = generics.get_object_or_404(PayWayMetaData, app_id=self.kwargs.get("app_id"))
        try:
            # may not exist
            request.user.key_pairs.get(meta_data_id=meta_data.id).delete()
        except:
            pass
        data = {"meta_data": meta_data.id, **request.data}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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


