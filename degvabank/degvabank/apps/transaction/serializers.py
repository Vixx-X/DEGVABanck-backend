from django.core import validators
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from degvabank.apps.account.models import Account
from degvabank.apps.card.models import CreditCard
from degvabank.apps.transaction.utils import is_our_number

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class UserTransactionSerializer(serializers.ModelSerializer):
    acc = card = dst = dst_not_our = None
    document_id = serializers.CharField(
        write_only=True,
        max_length=15,
        validators=[
            validators.RegexValidator(
                regex=r"^[eEvVjJ]\d+$",
                message=_("your document id is not well formatted"),
            ),
        ],
    )

    def validate_source(self, value):
        user = self.context["request"].user
        self.acc = user.accounts.filter(id=value, is_active=True).first()
        self.card = user.credit_cards.filter(number=value, is_active=True).first()
        if not (self.acc or self.card):
            raise serializers.ValidationError(_("Invalid source account or card"))
        return value

    def validate_target(self, value):
        # TODO: if value not ours: return value
        if not is_our_number(value):
            self.dst = value
            self.dst_not_our = True
            return value

        dst_acc = Account.objects.filter(id=value, is_active=True).first()
        dst_card = CreditCard.objects.filter(number=value, is_active=True).first()
        if not (dst_acc or dst_card):
            raise serializers.ValidationError(
                _("Target account or card does not exists")
            )
        self.dst = dst_card or dst_acc
        return value

    def validate_document_id(self, value):
        if not self.dst_not_our and self.dst and self.dst.user.document_id.lower() != str(value).lower():
            raise serializers.ValidationError(
                _("Target account or card is not associated with that document id")
            )
        return value

    def validate_amount(self, value):
        if self.acc and self.acc.balance < value:
            raise serializers.ValidationError(_("Insufficent balance"))
        if self.card and self.card.credit < value:
            raise serializers.ValidationError(_("Insufficent balance"))
        return value

    class Meta:
        model = Transaction
        fields = [
            "id",
            "source",
            "target",
            "document_id",
            "amount",
            "type",
            "status",
            "reason",
            "date",
        ]
        read_only_fields = ("type", "status", "date", "id")

    def create(self, validated_data):
        field_names = [field.name for field in self.Meta.model._meta.get_fields()]
        data = {a: b for a, b in validated_data.items() if a in field_names}
        kwargs = {
            "amount": data["amount"],
            "reason": data["reason"],
            "source": {
                "number": data["source"]
            },
            "target": {
                "number": data["target"],
                "document_id": validated_data["document_id"],
            }
        }
        return self.Meta.model.objects.create_any_transaction(**kwargs)


class TransactionCardSerializer(serializers.Serializer):
    number = serializers.CharField()
    security_code = serializers.CharField()
    expiration_date = serializers.DateTimeField()
    document_id = serializers.CharField(
        required=False,
        write_only=True,
        max_length=15,
        validators=[
            validators.RegexValidator(
                regex=r"^[eEvVjJ]\d+$",
                message=_("your document id is not well formatted"),
            ),
        ],
    )

class TransactionAccountSerializer(serializers.Serializer):
    number = serializers.CharField()
    document_id = serializers.CharField(
        required=True,
        write_only=True,
        max_length=15,
        validators=[
            validators.RegexValidator(
                regex=r"^[eEvVjJ]\d+$",
                message=_("your document id is not well formatted"),
            ),
        ],
    )

class ForeignTransactionSerializer(serializers.ModelSerializer):

    acc_src = TransactionAccountSerializer(required=False)
    acc_dst = TransactionAccountSerializer(required=False)
    card_src = TransactionCardSerializer(required=False)
    card_dst = TransactionCardSerializer(required=False)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "acc_src",
            "acc_dst",
            "card_src",
            "card_dst",
            "amount",
            "type",
            "status",
            "reason",
            "date",
        ]
        read_only_fields = ("type", "status", "date", "id")

    def create(self, validated_data):
        field_names = [field.name for field in self.Meta.model._meta.get_fields()]
        data = {a: b for a, b in validated_data.items() if a in field_names}
        kwargs = {
            "amount": data["amount"],
            "reason": data["reason"],
            "source": validated_data.get("acc_src") or validated_data.get("card_src"),
            "target": validated_data.get("acc_dst") or validated_data.get("card_dst")
        }
        return self.Meta.model.objects.create_any_transaction(from_foreign=True, **kwargs)
