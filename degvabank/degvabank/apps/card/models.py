from django.db import models

# Create your models here.
from creditcards.models import (
    CardNumberField, CardExpiryField, SecurityCodeField )
from django.db import models
from django.utils.translation import gettext_lazy as _

class Card(models.Model):
    number = CardNumberField(_("card number"))

    security_code = SecurityCodeField(_("security code"))

    expiration_date = CardExpiryField(_("expiration date"))

    def __str__(self):
        return f"{self.number} {self.expiration_date}"

    class Meta:
        abstract = True
        app_label = "card"
        verbose_name = _("card")
        verbose_name_plural = _("cards")


class CreditCard(Card):

    user = models.ForeignKey(
        "user.User",
        verbose_name=_("card owner"),
        on_delete=models.RESTRICT,
        related_name="credit_cards",
    )

    class Meta:
        app_label = "card"
        db_table = "credit_cards"
        verbose_name = _("credit card")
        verbose_name_plural = _("credit cards")

    def __str__(self):
        return "CreditCard - " + super().__str__()


class DebitCard(Card):

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


    def __str__(self):
        return "DebitCard - " + super().__str__()

