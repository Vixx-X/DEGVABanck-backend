from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from .models import CreditCard, DebitCard

class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = "__all__"


class UserCreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = "__all__"


class DebitCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebitCard
        fields = "__all__"


class UserDebitCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebitCard
        fields = "__all__"

