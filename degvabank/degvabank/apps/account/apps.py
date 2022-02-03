from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountConfig(AppConfig):
    name = 'degvabank.apps.account'
    label = "account"
    verbose_name = _("account")
