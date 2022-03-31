from datetime import datetime
from django.db import models
from django.db.models.query_utils import Q
from rest_framework import serializers
from degvabank.apps.account.models import Account
from degvabank.apps.card.models import CreditCard
from django.utils.translation import gettext_lazy as _
import requests

from degvabank.apps.transaction.exceptions import TransactionError, get_error
from degvabank.apps.transaction.utils import is_card, is_our_card, is_our_number

DAKITI_CARD_URL = "https://dakiti-back.herokuapp.com/api/otherBankCards"
DAKITI_ACC_URL = "https://dakiti-back.herokuapp.com/api/otherBankTransfer"

class TransactionMixin:

    def check_acc_or_card_document_id(self, obj, document_id, code):
        if isinstance(obj, Account):
            if document_id and str(obj.user.document_id).lower() == str(document_id).lower():
                get_error(code)
        # if isinstance(obj, CreditCard):
        #     if document_id and str(obj.user.document_id).lower() == str(document_id).lower():
        #         get_error(code)

    def check_acc_or_card_funds(self, obj, ammount):
        if isinstance(obj, Account):
            if obj.balance < ammount:
                get_error(TransactionError.INSUFICIENT_FUNDS)
        if isinstance(obj, CreditCard):
            if obj.credit < ammount:
                get_error(TransactionError.INSUFICIENT_CREDITS)

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

    def check_cvc(self, obj, cvc, code):
        if obj.security_code != cvc:
            get_error(code)

    def check_exp_date(self, obj, date, is_source):
        now = datetime.today()
        if date < datetime.date(now.year, now.month, 1):
            get_error(
                TransactionError.EXP_DATE_EXPIRED_ORIGIN_CARD
                if is_source else
                TransactionError.EXP_DATE_EXPIRED_TARGET_CARD
            )

        if obj.expiration_date.date().year != date.year or obj.expiration_date.date().month != date.year:
            get_error(
                TransactionError.EXP_DATE_DID_NOT_MATCH_ORIGIN_CARD
                if is_source else
                TransactionError.EXP_DATE_DID_NOT_MATCH_TARGET_CARD
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
                "expirationDate": source["expiration_date"].strftime("%m%y"),
                "descripcion": reason,
                "monto": float(amount),
            }
            resp = requests.post(DAKITI_CARD_URL, json=data)
        else:
            data = {
                "cuentaDestino": target["number"],
                "cuentaOrigen": source["number"],
                "identificador": str(target["document_id"])[1:],
                "identificadorTipo": str(target["document_id"])[0].upper(),
                "descripcion": reason,
                "monto": float(amount),
            }
            resp = requests.post(DAKITI_ACC_URL, json=data)
        if not resp.ok:
            print(data)
            print(resp.json())
            get_error(resp.json().get("codigo", -1))

    def validated_transaction_data(self, **transaction_data):
        source=transaction_data["source"]
        target=transaction_data["target"]
        amount=transaction_data["amount"]

        if self.is_our_number(source["number"]):
            source_obj = self.get_account_or_creditcard(source["number"])
            card = is_card(source["number"])
            if not source_obj:
                get_error(
                    TransactionError.INVALID_ORIGIN_CARD
                    if card else
                    TransactionError.INVALID_ORIGIN_ACCOUNT
                )
            if card:
                self.check_cvc(
                    source_obj,
                    source["security_code"],
                    TransactionError.CVC_DID_NOT_MATCH_ORIGIN_CARD,
                )
                self.check_exp_date(
                    source_obj,
                    source["expiration_date"],
                    True,
                )
            else:
                self.check_acc_or_card_document_id(
                    source_obj,
                    source["document_id"],
                    TransactionError.DOCUMENT_ID_DID_NOT_MATCH_ORIGIN_ACCOUNT,
                )

            self.check_acc_or_card_funds(
                source_obj,
                amount,
            )

        if self.is_our_number(target["number"]):
            target_obj = self.get_account_or_creditcard(target["number"])
            card = is_card(target["number"])
            if not target_obj:
                raise serializers.ValidationError(
                    {"target": _("Invalid or non existent number")},
                    code=TransactionError.INVALID_TARGET_CARD if is_card(target["number"]) else TransactionError.INVALID_TARGET_ACCOUNT
                )
            if card:
                self.check_cvc(
                    target_obj,
                    target["security_code"],
                    TransactionError.CVC_DID_NOT_MATCH_ORIGIN_CARD,
                )
                self.check_exp_date(
                    target_obj,
                    source["expiration_date"],
                    False,
                )
            else:
                self.check_acc_or_card_document_id(
                    target,
                    target["document_id"],
                    TransactionError.DOCUMENT_ID_DID_NOT_MATCH_TARGET_ACCOUNT,
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
