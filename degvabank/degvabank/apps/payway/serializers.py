from typing import TypedDict
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from degvabank.apps.payway.utils import censor_key

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


class ApiKey(TypedDict):
    public : str
    private : str

class UserPayWayMetaSerializer(serializers.ModelSerializer):

    api_keys = serializers.SerializerMethodField()

    def get_api_keys(self, obj) -> ApiKey:
        keys = obj.keys.first()
        if not keys:
            return {"public":"", "private":""}
        return {
            "public":censor_key(keys.public),
            "private":censor_key(keys.private)
        }

    transactions = serializers.SerializerMethodField()

    def get_transactions(self, obj) -> int:
        return 0

    class Meta:
        model = PayWayMetaData
        exclude = ["id"]
        lookup_field="app_id"
