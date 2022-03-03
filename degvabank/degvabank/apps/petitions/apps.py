from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PetitionsConfig(AppConfig):
    name = "degvabank.apps.petitions"
    label = "petitions"
    verbose_name = _("petitions")
