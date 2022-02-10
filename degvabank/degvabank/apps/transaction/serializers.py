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
        self.acc = user.accounts.get(id=value, is_active=True)
        self.card = user.credits.get(number=value, is_active=True)
        if not (self.acc or self.card):
            raise serializers.ValidationError(_("You are not allowd to use that account"))
        return value

    def validate_target(self, value):
        dst_acc = Account.objects.get(id=value, is_active=True)
        dst_card = CreditCard.objects.get(number=value, is_active=True)
        if not (dst_card or dst_card):
            raise serializers.ValidationError(_("Target account or card does not exists"))
        self.dst = dst_card or dst_acc
        return value

    def validate_document_id(self, value):
        if self.dst and self.dst.user.document_id != value:
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
            "source",
            "target",
            "document_id",
            "amount",
            "type",
            "status",
            "reason",
            "date",
        ]
        read_only_fields = ("type", "status", "date")
