from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from degvabank.apps.card.serializers import UserDebitCardSerializer

from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class UserAccountSerializer(serializers.ModelSerializer):
    cards = UserDebitCardSerializer(many=True)
    class Meta:
        model = Account
        fields = [
            "type",
            "balance",
            "creation_date",
            "cards",
        ]

