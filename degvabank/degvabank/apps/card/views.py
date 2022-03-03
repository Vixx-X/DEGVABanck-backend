from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from degvabank.apps.petitions.models import Petition

from .serializers import (
    CreditCardSerializer,
    UserCreditCardSerializer,
    DebitCardSerializer,
    UserDebitCardSerializer,
)
from .models import CreditCard, DebitCard

# credit


class CreditCardViewSet(viewsets.ModelViewSet):
    """
    Entrypoint for credit cards
    """

    permission_classes = (IsAdminUser,)
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer


class UserCreditCardListCreateView(generics.ListCreateAPIView):
    """
    List user credit cards
    """

    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = UserCreditCardSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.credit_cards.filter(is_active=True)

    def perform_create(self, serializer):
        obj = serializer.save()
        Petition.objects.create(
            content_object=obj,
            reason=Petition.ReasonType.CREATE_CREDIT_CARD,
            user=self.request.user,
        )
        return obj


class UserCreditCardView(generics.RetrieveAPIView):
    """
    Retrieve user credit card
    """

    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = UserCreditCardSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.credit_cards.filter(is_active=True)


# debit


class DebitCardViewSet(viewsets.ModelViewSet):
    """
    Entrypoint for debit cards
    """

    permission_classes = (IsAdminUser,)
    queryset = DebitCard.objects.all()
    serializer_class = DebitCardSerializer


class UserDebitCardListCreateView(generics.ListCreateAPIView):
    """
    List and create user debit cards
    """

    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = UserDebitCardSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return DebitCard.objects.filter(account__user=self.request.user, is_active=True)

    def perform_create(self, serializer):
        obj = serializer.save()
        Petition.objects.create(
            content_object=obj,
            reason=Petition.ReasonType.CREATE_DEBIT_CARD,
            user=self.request.user,
        )
        return obj


class UserDebitCardView(generics.RetrieveAPIView):
    """
    Retrieve user debit card
    """

    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = UserDebitCardSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return DebitCard.objects.filter(account__user=self.request.user, is_active=True)
