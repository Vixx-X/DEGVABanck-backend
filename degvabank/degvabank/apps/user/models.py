from django.core import validators
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    class UserType(models.TextChoices):
        NATURAL = "NATURAL", _("Natural")
        JURIDIC = "JURIDIC", _("Juridic")

    type = models.CharField(
        _("type of user (natural/juridic)"),
        max_length=50,
        choices=UserType.choices,
    )

    document_id = models.CharField(
        _("document id (cedula/rif)"),
        max_length=15,
        validators=[
            validators.RegexValidator(
                regex=r"^[eEvVjJ]\d+$",
                message=_("your document id is not well formatted"),
            ),
        ],
    )

    def get_full_name(self):
        # Returns the first_name and the last_name
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        # Returns the short name for the user.
        return self.first_name

    def get_pretty_document(self):
        # Returns document_id prettier
        document_id = str(self.document_id)
        letter = document_id[0].upper()
        number = document_id[1:]
        return f"{letter}-{number}"
