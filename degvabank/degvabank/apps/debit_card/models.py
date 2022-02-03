"""
Hereda de card
account (referencia)
"""
from django.db import models
from apps.card.models import Card
from apps.account.models import Account

class DebitCard(Card):
    user = models.ForeignKey(
        Account,
        to_field='account_num',
    )