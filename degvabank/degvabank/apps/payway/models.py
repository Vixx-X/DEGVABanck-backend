from django.db import models
from django.utils.translation import gettext_lazy as _

from .utils import decrypt, encrypt, gen_key_pair

class PayWayMetaData(models.Model):

    account = models.OneToOneField(
        "account.Account",
        verbose_name=_("owner account"),
        on_delete=models.CASCADE,
    )

    backend = models.URLField(
        _("backend endpoint"),
    )

    success = models.URLField(
        _("success url"),
    )

    fail = models.URLField(
        _("fail url"),
    )

    def __str__(self):
        return f"Bussiness pay way of {self.account}"

    class Meta:
        app_label = "payway"
        db_table = "payway_metadata"
        verbose_name = _("pay way meta data")
        verbose_name_plural = _("pay way meta data")


class PayWayKeys(models.Model):

    meta_data = models.ForeignKey(
        PayWayMetaData,
        on_delete=models.CASCADE,
    )

    owner = models.OneToOneField(
        "user.User",
        verbose_name=_("key pair owner"),
        on_delete=models.CASCADE,
        related_name="key_pair",
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
        self.meta_data = PayWayMetaData.objects.filter(
                account__owner_id=self.owner).first()
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


