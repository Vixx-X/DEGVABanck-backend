""""
id
serial
security_code
date
"""
from credit_card.models import (
    CardNumberField, CardExpiryField, SecurityCodeField )
from django.db import models
from django.utils.translation import gettext_lazy as _

class Card(models.Model):
    card_num = CardNumberField(_("card number"))

    security_code = SecurityCodeField(_("security code"))

    expiration_date = CardExpiryField(_("expiration date"))