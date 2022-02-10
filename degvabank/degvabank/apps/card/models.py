from random import randint
from types import NotImplementedType
from django.db import models
from datetime import datetime

# Create your models here.
from creditcards.models import (
    CardNumberField, CardExpiryField, SecurityCodeField )
from creditcards.utils import luhn
from django.db import models
from django.utils.translation import gettext_lazy as _

CREDIT_CARD = "CC"
DEBIT_CARD = "DC"

def gen_card_number(card_type):
    card_t = 1 if card_type == CREDIT_CARD else 0
    while True:
        rnum = randint(1, 999_999_999)
        snum = f"1337{card_t}{rnum:09}"
        if luhn(snum):
            return snum


class Card(models.Model):
    number = CardNumberField(
        _("card number"),
        primary_key=True,
        editable=False
    )

    is_active = models.BooleanField(
        _("card is active"),
        default=True,
        db_index=True,
        help_text=_("card should be used by owner?")
    )

    security_code = SecurityCodeField(_("security code"))

    expiration_date = CardExpiryField(_("expiration date"))

    date_created = models.DateField(
        _("date created"),
        auto_now_add=True,
        db_index=True,
    )

    type = None

    @property
    def pretty_card_number(self):
        """
        return 'xxxx xxxx xxxx xxxx'
        """
        return self.number

    @property
    def card_number(self):
        return self.number

    def generate_card_number(self):
        if not self.type:
            raise NotImplementedType("Children class need to implement self.type, in order to use this gen")
        return gen_card_number(self.type)

    def save(self, *args, **kwargs):
        now = datetime.now()
        self.number = self.number or self.generate_card_number()
        self.security_code = self.security_code or randint(1, 9999)
        self.expiration_date = self.expiration_date or now.replace(now.year + 5)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.number} {self.expiration_date}"

    class Meta:
        abstract = True
        app_label = "card"
        verbose_name = _("card")
        verbose_name_plural = _("cards")


class CreditCard(Card):
    type = CREDIT_CARD

    user = models.ForeignKey(
        "user.User",
        verbose_name=_("card owner"),
        on_delete=models.RESTRICT,
        related_name="credit_cards",
    )

    credit = models.DecimalField(
        verbose_name=_("credits"),
        max_digits=12,
        decimal_places=2,
    )

    class Meta:
        app_label = "card"
        db_table = "credit_cards"
        verbose_name = _("credit card")
        verbose_name_plural = _("credit cards")

    def __str__(self):
        return "CreditCard - " + super().__str__()


class DebitCard(Card):
    type = DEBIT_CARD

    account = models.ForeignKey(
        "account.Account",
        verbose_name=_("account"),
        on_delete=models.RESTRICT,
        related_name="cards",
    )

    class Meta:
        app_label = "card"
        db_table = "debit_cards"
        verbose_name = _("debit card")
        verbose_name_plural = _("debit cards")

    def generate_card_number(self):
        return gen_card_number(DEBIT_CARD)

    def __str__(self):
        return "DebitCard - " + super().__str__()

