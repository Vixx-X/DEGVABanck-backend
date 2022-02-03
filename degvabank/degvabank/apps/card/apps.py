from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CardConfig(AppConfig):
    name = 'degvabank.apps.card'
    label = "card"
    verbose_name = _("card")
