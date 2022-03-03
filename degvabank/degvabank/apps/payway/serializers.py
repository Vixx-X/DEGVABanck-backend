from typing import TypedDict
from django.db.utils import ProgrammingError
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from degvabank.apps.payway.utils import censor_key

from degvabank.apps.transaction.models import Transaction
from degvabank.apps.card.models import CreditCard
from degvabank.apps.account.models import Account

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
    public: str
    private: str


class UserPayWayMetaSerializer(serializers.ModelSerializer):

    api_keys = serializers.SerializerMethodField()

    def get_api_keys(self, obj) -> ApiKey:
        keys = obj.keys.first()
        if not keys:
            return {"public": "", "private": ""}
        return {"public": censor_key(keys.public), "private": censor_key(keys.private)}

    transactions = serializers.SerializerMethodField()

    def get_transactions(self, obj) -> int:
        return obj.transactions.count()

    class Meta:
        model = PayWayMetaData
        exclude = ["id"]
        lookup_field = "app_id"


class PayWayTransaction(serializers.ModelSerializer):
    key = serializers.CharField()

    def validate_key(self, value):
        self.key_obj = PayWayKeys.objects.filter(public=value).first()
        if not self.key_obj:
            raise serializers.ValidationError(_("public key does not exist"))

        return value

    def get_transaction_source(self) -> str:
        raise NotImplementedError(_("this is only for subclasses"))

    def get_transaction_kwargs(self):
        data = self.validated_data
        if not data:
            raise ProgrammingError(_("make sure to use get_transaction_kwargs on save"))
        return {
            "amount": data["amount"],
            "reason": data["reason"],
            "target": self.key_obj.meta_data.account.id,
            "source": self.get_transaction_source(),
        }

    class Meta:
        model = Transaction
        fields = ["key", "amount", "reason"]


class PayWayTransactionFromAccount(serializers.ModelSerializer):
    number = serializers.CharField(source="id")

    class Meta:
        model = Account
        fields = ["number"]


class PayWayTransactionAccount(PayWayTransaction):
    account = PayWayTransactionFromAccount()

    class Meta(PayWayTransaction.Meta):
        fields = PayWayTransaction.Meta.fields + ["account"]

    def get_transaction_source(self) -> str:
        data = self.validated_data
        if not data:
            raise ProgrammingError(_("make sure to use get_transaction_kwargs on save"))
        return data["account"]["id"]

    def save(self):
        tran = Transaction.objects.create(**self.get_transaction_kwargs())
        self.key_obj.meta_data.transactions.add(tran)
        return tran


class PayWayTransactionFromCreditCard(serializers.ModelSerializer):
    number = serializers.CharField()

    class Meta:
        model = CreditCard
        fields = ["number", "security_code", "expiration_date"]


class PayWayTransactionCreditCard(PayWayTransaction):
    card = PayWayTransactionFromCreditCard()

    class Meta(PayWayTransaction.Meta):
        fields = PayWayTransaction.Meta.fields + ["card"]

    def get_transaction_source(self) -> str:
        data = self.validated_data
        if not data:
            raise ProgrammingError(_("make sure to use get_transaction_kwargs on save"))
        return data["card"]["number"]

    def save(self):
        tran = Transaction.objects.create(**self.get_transaction_kwargs())
        self.key_obj.meta_data.transactions.add(tran)
        return tran
