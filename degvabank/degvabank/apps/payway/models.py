from django.db import models
from django.utils.translation import gettext_lazy as _

from .utils import decrypt, encrypt, gen_key_pair

class PayWayKeys(models.Model):

    owner = models.ForeignKey(
        "user.User",
        verbose_name=_("key pair owner"),
        on_delete=models.CASCADE,
        related_name="key_pairs",
        unique=True,
    )

    public = models.CharField(
        _("publishable key"),
        max_length=64,
        primary_key=True,
        editable=False
    )

    private = models.CharField(
        _("secret key"),
        max_length=64,
    )

    def __str__(self):
        return f"key pair {self.public} of {self.owner}"

    def save(self, *args, **kwargs):
        if not self.public or not self.private:
            self.public, self.private = gen_key_pair()
        return super().save(*args, **kwargs)

    def encrypt(self, msg):
        return encrypt(self.private, msg)

    def decrypt(self, msg):
        return decrypt(self.private, msg)

    class Meta:
        app_label = "payway"
        db_table = "payway_keys"
        verbose_name = _("pay way key")
        verbose_name_plural = _("pay way keys")
