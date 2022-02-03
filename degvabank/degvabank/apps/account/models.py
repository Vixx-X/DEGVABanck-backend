"""
id
type (corriente, ahorro)
balance
date
user (reference)
"""
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.user.models import User


class Account(models.Model):

    class AccountType(models.TextChoices):
        CHECKING = "CHECKING", _("Checking")
        SAVING = "SAVING", _("Saving")

    account_num = models.UUIDField(
        _("account id"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    type = models.CharField(
        _("type of account (checking, saving)"),
        max_length=10,
        choices=AccountType.choices,
    )

    balance = models.DecimalField(
        decimal_places=2,
    )

    creation_date = models.DateField()

    user = models.ForeignKey(
        User,
        to_field='document_id',
    )