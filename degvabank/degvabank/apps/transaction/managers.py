from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.query_utils import Q
from degvabank.apps.account.models import Account
from degvabank.apps.card.models import CreditCard

class TransactionMixin:
    def rest_source(self, source, ammount, is_account):
        if is_account:
            source.balance -= ammount
        else:
            source.credit -= ammount

    def add_target(self, target, ammount, is_account):
        if is_account:
            target.balance += ammount
        else:
            target.credit += ammount

    def get_account_or_creditcard(self, code):
        return Account.objects.filter(id=code, is_active=True).first() or CreditCard.objects.filter(number=code, is_active=True).first()


    def process_in_house_transaction(self, transaction):
        source = self.get_account_or_creditcard(transaction.source)
        target = self.get_account_or_creditcard(transaction.target)

        if not source:
            raise ValidationError("This source account or credit card is not valid")
        if not target:
            raise ValidationError("This target account or credit card is not valid")

        self.add_target(target, transaction.amount, is_account=isinstance(target, Account))
        self.rest_source(source, transaction.amount, is_account=isinstance(source, Account))

        source.save()
        target.save()
        transaction.status = transaction.TransactionStatus.ACCEPTED
        transaction.save()
        return transaction


class TransactionManager(TransactionMixin, models.Manager):
    def create(self,**kwargs):
        transaction = self.model(**kwargs)
        return self.process_transaction(transaction)
