"""
id
amount
reason
date
target_account (reference)
source_account (reference)
"""
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from degvabank.degvabank.apps.account.models import Account

class Transaction(models.Model):
    id = models.UUIDField(
        _("transaction id"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    amount = models.DecimalField(
        decimal_places=2,
    )

    reason = models.CharField(
        _("reason why the transaction is being carried out"),
        max_length=50,
    )

    date = models.DateField()

    target_account = models.ForeignKey(
        Account,
        to_field='account_num'
    )

    source_account = models.ForeignKey(
        Account,
        to_field='account_num'
    )