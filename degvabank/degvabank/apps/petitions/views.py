from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

from .models import Petition
from .serializers import PetitionSerializer, UserPetitionSerializer

class PetitionViewSet(viewsets.ModelViewSet):
    """
    Entrypoint for petitions
    """

    permission_classes = (IsAdminUser,)
    queryset = Petition.objects.all()
    serializer_class = PetitionSerializer

class UserPetitionListView(generics.ListAPIView):
    """
    List user petitions
    """
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = UserPetitionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.petitions.all()
