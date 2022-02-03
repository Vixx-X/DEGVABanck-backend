from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

from .serializers import CreditCardSerializer, UserCreditCardSerializer, DebitCardSerializer, UserDebitCardSerializer
from .models import CreditCard, DebitCard

# credit

class CreditCardViewSet(viewsets.ModelViewSet):
    """
    Entrypoint for credit cards
    """

    permission_classes = (IsAdminUser,)
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer

class UserCreditCardListView(generics.ListAPIView):
    """
    List user credit cards
    """
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = UserCreditCardSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.cards.all()

class UserCreditCardView(generics.RetrieveAPIView):
    """
    Retrieve user credit card
    """
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = UserCreditCardSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.cards.all()


# debit

class DebitCardViewSet(viewsets.ModelViewSet):
    """
    Entrypoint for debit cards
    """

    permission_classes = (IsAdminUser,)
    queryset = DebitCard.objects.all()
    serializer_class = DebitCardSerializer

class UserDebitCardListView(generics.ListAPIView):
    """
    List user debit cards
    """

    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = UserDebitCardSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.cards.all()

class UserDebitCardView(generics.RetrieveAPIView):
    """
    Retrieve user debit card
    """
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = UserDebitCardSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return DebitCard.objects.filter(account__user=self.request.user)
