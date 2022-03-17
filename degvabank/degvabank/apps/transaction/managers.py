from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.query_utils import Q
from rest_framework import serializers
from degvabank.apps.account.models import Account
from degvabank.apps.card.models import CreditCard
from django.utils.translation import gettext_lazy as _
import requests

from degvabank.apps.transaction.utils import is_card, is_our_card, is_our_number

DAKITI_CARD_URL = "https://dakiti-back.herokuapp.com/api/otherBankCards"
DAKITI_ACC_URL = "https://dakiti-back.herokuapp.com/api/otherBankTransfer"

class TransactionMixin:

    def check_acc_or_card_document_id(self, obj, document_id, msg):
        if isinstance(obj, Account):
            if False:
                raise serializers.ValidationError(msg)
        if isinstance(obj, CreditCard):
            if False and document_id:
                raise serializers.ValidationError(msg)

    def check_acc_or_card_funds(self, obj, ammount, msg):
        if isinstance(obj, Account):
            if obj.balance < ammount:
                raise serializers.ValidationError(msg)
        if isinstance(obj, CreditCard):
            if obj.credit < ammount:
                raise serializers.ValidationError(msg)

    def charge_acc_or_card(self, obj, ammount):
        if isinstance(obj, Account):
            obj.balance += ammount
        else:
            obj.credit += ammount

    def get_account_or_creditcard(self, code):
        return (
            Account.objects.filter(id=code, is_active=True).first()
            or CreditCard.objects.filter(number=code, is_active=True).first()
        )

    def process_transaction(self, transaction):
        source = self.get_account_or_creditcard(transaction.source)
        target = self.get_account_or_creditcard(transaction.target)

        if source:
            self.charge_acc_or_card(source, -transaction.amount)
            source.save()
        if target:
            self.charge_acc_or_card(target, transaction.amount)
            target.save()

        transaction.status = transaction.TransactionStatus.ACCEPTED
        return transaction

    def send_transaction(self, **transaction_data):
        source = transaction_data["source"]
        target = transaction_data["target"]
        amount = transaction_data["amount"]
        reason = transaction_data["reason"]

        if is_card(source["number"]) and not is_our_card(source["number"]):
            data = {
                "card": source["number"],
                "cvc": source["security_code"],
                "expirationDate": source["expiration_date"].strftime("%m%Y"),
                "descripcion": reason,
                "monto": float(amount),
            }
            resp = requests.post(DAKITI_CARD_URL, json=data)
        else:
            data = {
                "cuentaDestino": target["number"],
                "cuentaOrigen": source["number"],
                "identificador": str(target["document_id"]).lower(),
                "descripcion": reason,
                "monto": float(amount),
            }
            resp = requests.post(DAKITI_ACC_URL, json=data)
        if not resp.ok:
            print(data)
            print(resp.json())
            raise serializers.ValidationError({"non_field_error": [_("Error with other bank")]})

    def validated_transaction_data(self, **transaction_data):
        source=transaction_data["source"]
        target=transaction_data["target"]
        amount=transaction_data["amount"]

        if self.is_our_number(source["number"]):
            source_obj = self.get_account_or_creditcard(source["number"])
            if not source_obj:
                raise serializers.ValidationError(
                    {"source": _("Invalid or non existent number")}
                )
            self.check_acc_or_card_funds(
                source_obj,
                amount,
                {"source": _("Does not have enough funds")}
            )

        if self.is_our_number(target["number"]):
            target_obj = self.get_account_or_creditcard(target["number"])
            if not target_obj:
                raise serializers.ValidationError(
                    {"target": _("Invalid or non existent number")}
                )
            self.check_acc_or_card_document_id(
                target_obj,
                target["document_id"],
                {"target": _("Document id did not match")}
            )

    def is_our_number(self, number):
        return is_our_number(number)

    def is_inhouse(self, transaction):
        src = str(transaction.source)
        dst = str(transaction.target)
        return self.is_our_number(src) and self.is_our_number(dst)


class TransactionManager(TransactionMixin, models.Manager):
    def get_queryset_by_user(self, user):
        accounts = user.accounts.values_list("id", flat=True)
        credit_cards = user.credit_cards.values_list("number", flat=True)
        from_filter = Q(source__in=accounts) | Q(source__in=credit_cards)
        to_filter = Q(target__in=accounts) | Q(target__in=credit_cards)
        user_filter = from_filter | to_filter
        return self.model.objects.filter(user_filter)

    def create(self, **kwargs):
        transaction = self.model(**kwargs)
        transaction = self.process_transaction(transaction)
        transaction.save()
        return transaction

    def create_any_transaction(self, from_foreign=False, **transaction_data):
        transaction = self.model(
            source=transaction_data["source"]["number"],
            target=transaction_data["target"]["number"],
            amount=transaction_data["amount"],
            reason=transaction_data["reason"],
        )

        try:
            self.validated_transaction_data(**transaction_data)

            if not from_foreign and not self.is_inhouse(transaction):
                self.send_transaction(**transaction_data)

            transaction = self.process_transaction(transaction)
            transaction.save()
        except serializers.ValidationError as e:
            transaction.status = transaction.TransactionStatus.REJECTED
            transaction.save()
            raise e

        return transaction
