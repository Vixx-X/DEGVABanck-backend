from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserConfig(AppConfig):
    name = "degvabank.apps.user"
    label = "user"
    verbose_name = _("user")
