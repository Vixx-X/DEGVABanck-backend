from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TransactionConfig(AppConfig):
    name = 'degvabank.apps.transaction'
    label = "transaction"
    verbose_name = _("transaction")
