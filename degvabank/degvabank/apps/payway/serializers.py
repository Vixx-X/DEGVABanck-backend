from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from .models import PayWayKeys

class PayWayKeysSerializer(serializers.ModelSerializer):
    class meta:
        model = PayWayKeys
        fields = "__all__"


class UserPayWayKeysSerializer(serializers.ModelSerializer):
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
