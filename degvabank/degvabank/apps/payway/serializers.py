from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from .models import PayWayKeys, PayWayMetaData

class PayWayKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayWayKeys
        fields = "__all__"


class UserPayWayKeysSerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        write_only=True,
    )

    class Meta:
        model = PayWayKeys
        read_only_fields = [
            "public",
            "private",
        ]
        fields = [
            "public",
            "private",
            "owner",
        ]

class PayWayMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayWayMetaData
        fields = "__all__"


class UserPayWayMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayWayKeys
        fields = "__all__"

    def create(self, validated_data):
        instance, _ = self.Meta.model.objects.get_or_create(**validated_data)
        return instance
