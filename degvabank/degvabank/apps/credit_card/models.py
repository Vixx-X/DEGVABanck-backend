"""
Hereda de card
user (referencia)
"""
from django.db import models
from apps.card.models import Card
from apps.user.models import User

class CreditCard(Card):
    user = models.ForeignKey(
        User,
        to_field='document_id',
    )