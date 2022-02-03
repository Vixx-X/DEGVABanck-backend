"""
id
amount
reason
date
target_account (reference)
source_account (reference)
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

class Transaction(models.Model):
    amount = models.DecimalField(
        _("ammount of money"),
        max_digits=12,
        decimal_places=2,
    )

    reason = models.CharField(
        _("reason why the transaction is being carried out"),
        max_length=50,
    )

    date = models.DateField(
        _("transaction date"),
        auto_now=True,
    )

    target_account = models.CharField(
        verbose_name=_("target account"),
        max_length=20,
    )

    source_account = models.CharField(
        verbose_name=_("source account"),
        max_length=20,
    )
