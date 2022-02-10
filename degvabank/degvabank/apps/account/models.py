"""
id
type (corriente, ahorro)
balance
date
user (reference)
"""
from random import randint
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.fields import AutoFieldMixin, CharField

class AutoAccountIDField(AutoFieldMixin, CharField):
    pass

class Account(models.Model):

    id = AutoAccountIDField(
        primary_key=True,
        editable=False,
        max_length=20,
        validators=[
            validators.RegexValidator(
                regex=r"00691337\d{11}[0|1]$",
                message=_("not a valid account"),
            ),
        ]
    )

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

    is_active = models.BooleanField(
        _("account is active"),
        default=True,
        db_index=True,
        help_text=_("account should be used by owner?")
    )
    status = models.CharField(
        _("status of account creation petition"),
        max_length=10,
        choices=AccountStatus.choices,
        default=AccountStatus.PENDING
    )

    balance = models.DecimalField(
        _("account balance"),
        default=0,
        max_digits=12,
        decimal_places=2,
    )

    date_created = models.DateField(
        _("date created"),
        auto_now_add=True,
        db_index=True,
    )

    user = models.ForeignKey(
        "user.User",
        on_delete=models.RESTRICT,
        related_name="accounts"
    )

    @property
    def pretty_account_number(self):
        """
        return 'xxxx xxxx xxxxxx xxxxx x'
        """
        return self.id

    @property
    def account_number(self):
        return self.id


    def generate_account_number(self):
        rnum = randint(1, 99_999_999_999)
        acc_type = 1 if self.type == __class__.AccountType.CHECKING else 0
        return f"00691337{rnum:011}{acc_type}"


    def save(self, *args, **kwargs):
        self.id = self.id or self.generate_account_number()
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "account"
        db_table = "accounts"
        verbose_name = _("account")
        verbose_name_plural = _("accounts")

    def __str__(self):
        return f"Account {self.id:018} of {self.user}"
