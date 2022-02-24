from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from .models import PayWayKeys

class PaywayKeysSerializer(serializers.ModelSerializer):
    class meta:
        model = PayWayKeys
        fields = "__all__"


class UserPaywayKeysSerializer(serializers.ModelSerializer):
    class meta:
        model = PayWayKeys
        read_only_fields = [
            "public",
            "private",
        ]
        fields = [
            "public",
            "private",
        ]
