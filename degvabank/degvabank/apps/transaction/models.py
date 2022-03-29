"""
id
amount
reason
date
target_account (reference)
source_account (reference)
"""

from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from degvabank.apps.card.utils import is_valid_credit_card
from degvabank.apps.transaction.managers import TransactionManager

def validate_positive(value):
    if value < 0:
        raise ValidationError(
            _('Amount %(value)s, should not be negative'),
            params={'value': value},
        )


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        ERROR = "C2C", _("error (credit card to credit card)")
        FROM_CREDIT_CARD = "C2A", _("from credit card to account")
        TO_CREDIT_CARD = "A2C", _("from account to credit card")
        ACCOUNTS = "A2A", _("from account to account")

    type = models.CharField(
        _("transaction type"), choices=TransactionType.choices, max_length=4
    )

    class TransactionStatus(models.TextChoices):
        ERROR = "ERR", _("error")
        PENDING = "PEN", _("pending")
        ACCEPTED = "ACC", _("accepted")
        REJECTED = "REJ", _("rejected")

    status = models.CharField(
        _("transaction status"),
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
        max_length=4,
    )

    amount = models.DecimalField(
        _("amount of money"),
        max_digits=12,
        decimal_places=2,
        validators=[validate_positive],
    )

    reason = models.CharField(
        _("reason why the transaction is being carried out"),
        max_length=50,
    )

    date = models.DateTimeField(
        _("transaction date"),
        auto_now=True,
    )

    target = models.CharField(
        verbose_name=_("target account or credit card number"),
        max_length=20,
        validators=[
            validators.RegexValidator(
                regex=r"^(\d{16}|\d{20})$",
                message=_("not a valid account or credit card"),
            ),
        ],
    )

    source = models.CharField(
        verbose_name=_("source account or credit card number"),
        max_length=20,
        validators=[
            validators.RegexValidator(
                regex=r"^(\d{16}|\d{20})$",
                message=_("not a valid account or credit card"),
            ),
        ],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = self.type or self.generate_type()

    def generate_type(self):
        cc_src = is_valid_credit_card(self.source)
        cc_dst = is_valid_credit_card(self.target)
        if cc_dst and cc_src:
            return __class__.TransactionType.ERROR
        if cc_src:
            return __class__.TransactionType.FROM_CREDIT_CARD
        if cc_dst:
            return __class__.TransactionType.TO_CREDIT_CARD
        return __class__.TransactionType.ACCOUNTS

    objects = TransactionManager()

    @classmethod
    def get_dommy(cls):
        return cls(
            type=cls.TransactionType.ACCOUNTS,
            status=cls.TransactionStatus.ACCEPTED,
            amount=100,
            reason="Transaction TEST",
            target="1234567890123456",
            source="1234567890123456",
        )

    class Meta:
        app_label = "transaction"
        db_table = "transactions"
        verbose_name = _("transaction")
        verbose_name_plural = _("transactions")

    def __str__(self):
        return f"Transaction {self.id:018}"
