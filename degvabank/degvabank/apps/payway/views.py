from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

from .serializers import PayWayKeysSerializer, UserPayWayKeysSerializer
from .models import PayWayKeys

class PaywayKeysViewSet(viewsets.ModelViewSet):
    """
    Entrypoint for payway keys
    """

    permission_classes = (IsAdminUser,)
    queryset = PayWayKeys.objects.all()
    serializer_class = PayWayKeysSerializer

class UserPaywayKeysCreateView(generics.CreateAPIView):

    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = UserPayWayKeysSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request.user.key_pairs.all().delete()
        return super().create(request, *args, **kwargs)

