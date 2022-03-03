from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Petition(models.Model):
    class ReasonType(models.TextChoices):
        OPEN_ACCOUNT = "+ACCOUNT", _("open a new account")
        CREATE_CREDIT_CARD = "+CC", _("create a credit card")
        CREATE_DEBIT_CARD = "+DC", _("create a dedit card")

    reason = models.CharField(
        _("reason"),
        max_length=15,
        choices=ReasonType.choices,
    )

    class PetitionStatus(models.TextChoices):
        APPROVED = "APPROVED", _("Approved")
        PENDING = "PENDING", _("Pending")
        DENIED = "DENIED", _("Denied")

    status = models.CharField(
        _("status"),
        max_length=10,
        choices=PetitionStatus.choices,
        default=PetitionStatus.PENDING,
        help_text=_("status (approved, pending, denied)"),
    )

    date_processed = models.DateField(
        _("date processed"),
        auto_now=True,
        db_index=True,
    )

    date_created = models.DateField(
        _("date created"),
        auto_now_add=True,
        db_index=True,
    )

    user = models.ForeignKey(
        "user.User", on_delete=models.RESTRICT, related_name="petitions"
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=20)
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        app_label = "petitions"
        db_table = "petitions"
        verbose_name = _("petition")
        verbose_name_plural = _("petitions")

    def __str__(self):
        return f"Petition {self.id:018} to {self.get_reason_display()} of {self.user}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == self.PetitionStatus.APPROVED:
            self.content_object.is_active = True
            self.content_object.save()
