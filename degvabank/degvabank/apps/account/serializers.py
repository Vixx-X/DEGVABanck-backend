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
    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.pretty_account_number

    class Meta:
        model = Account
        fields = [
            "id",
            "type",
            "balance",
            "date_created",
            "cards",
        ]

