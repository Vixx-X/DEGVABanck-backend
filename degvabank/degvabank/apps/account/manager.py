from django.db import models
from degvabank.apps.card.models import DebitCard
from degvabank.apps.petitions.models import Petition


class AccountManager(models.Manager):
    def get_queryset_by_user(self, user):
        return user.accounts.filter(is_active=True)

    def request_account(self, **kwargs):
        obj = self.create(**kwargs)
        DebitCard.objects.create(
            account=obj,
        )
        Petition.objects.create(
            content_object=obj,
            reason=Petition.ReasonType.OPEN_ACCOUNT,
            user=kwargs['user'],
        )
        return obj
