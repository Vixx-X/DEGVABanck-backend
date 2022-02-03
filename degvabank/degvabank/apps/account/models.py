"""
id
type (corriente, ahorro)
balance
date
user (reference)
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Account(models.Model):

    class AccountType(models.TextChoices):
        CHECKING = "CHECKING", _("Checking")
        SAVING = "SAVING", _("Saving")

    type = models.CharField(
        _("type of account (checking, saving)"),
        max_length=10,
        choices=AccountType.choices,
    )

    class AccountStatus(models.TextChoices):
        APPROVED = "APPROVED", _("Approved")
        PENDING = "PENDING", _("Pending")
        DENIED = "DENIED", _("Denied")

    status = models.CharField(
        _("status of account creation petition"),
        max_length=10,
        choices=AccountStatus.choices,
        default=AccountStatus.PENDING
    )

    balance = models.DecimalField(
        _("account balance"),
        max_digits=12,
        decimal_places=2,
    )

    creation_date = models.DateField(_("creation date"), auto_now=True)

    user = models.ForeignKey(
        "user.User",
        on_delete=models.RESTRICT,
        related_name="accounts"
    )
