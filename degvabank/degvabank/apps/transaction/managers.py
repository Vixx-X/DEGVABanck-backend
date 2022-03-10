from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.query_utils import Q
from rest_framework import serializers
from degvabank.apps.account.models import Account
from degvabank.apps.card.models import CreditCard


class TransactionMixin:
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

    def process_in_house_transaction(self, transaction):
        source = self.get_account_or_creditcard(transaction.source)
        target = self.get_account_or_creditcard(transaction.target)

        if not source:
            raise ValidationError("This source account or credit card is not valid")
        if not target:
            raise ValidationError("This target account or credit card is not valid")

        self.charge_acc_or_card(target, transaction.amount)
        self.charge_acc_or_card(source, -transaction.amount)

        source.save()
        target.save()
        return transaction

    def process_outside_transaction(self, data):
        raise serializers.ValidationError({"msg": "Todo bien"})
        pass

    def process_transaction(self, transaction):
        transaction = self.process_in_house_transaction(transaction)
        transaction.status = transaction.TransactionStatus.ACCEPTED
        transaction.save()
        return transaction


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
        return self.process_transaction(transaction)

    def create1(self, data):
        return self.process_outside_transaction(data)
