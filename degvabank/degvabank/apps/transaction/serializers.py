from django.core import validators
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from degvabank.apps.account.models import Account
from degvabank.apps.card.models import CreditCard

from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class UserTransactionSerializer(serializers.ModelSerializer):
    acc = card = dst = None
    document_id = serializers.CharField(
            write_only=True,
            max_length=15,
            validators=[
                validators.RegexValidator(
                    regex=r"^[eEvVjJ]\d+$",
                    message=_("your document id is not well formatted"),
                    ),
                ]
            )

    def validate_source(self, value):
        user = self.context['request'].user
        self.acc = user.accounts.filter(id=value, is_active=True).first()
        self.card = user.credit_cards.filter(number=value, is_active=True).first()
        if not (self.acc or self.card):
            raise serializers.ValidationError(_("Invalid source account or card"))
        return value

    def validate_target(self, value):
        # TODO: if value not ours: return value

        dst_acc = Account.objects.filter(id=value, is_active=True).first()
        dst_card = CreditCard.objects.filter(number=value, is_active=True).first()
        if not (dst_acc or dst_card):
            raise serializers.ValidationError(_("Target account or card does not exists"))
        self.dst = dst_card or dst_acc
        return value

    def validate_document_id(self, value):
        if self.dst and self.dst.user.document_id.lower() != str(value).lower():
            raise serializers.ValidationError(_("Target account or card is not associated with that document id"))
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
        data = {a:b for  a, b in validated_data.items() if a in field_names }
        return self.Meta.model.objects.create(**data)
